# Copyright 2016 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import collections
import contextlib
import logging
import threading
import time

import six

from utils import auth_server

from bot_code import file_reader
from bot_code import remote_client


class AuthSystemError(Exception):
  """Fatal errors raised by AuthSystem class."""


# Parsed value of JSON at path specified by --auth-params-file task_runner arg.
AuthParams = collections.namedtuple(
    'AuthParams',
    [
        # Bot name.
        'bot_id',

        # The task the bot is running.
        'task_id',

        # Dict with HTTP headers to use when calling Swarming backend
        # (specifically). They identify the bot to the Swarming backend.
        # Ultimately generated by 'get_authentication_headers' in
        # bot_config.py. May be empty if the bot is not using headers
        # for authentication.
        'swarming_http_headers',

        # Unix timestamp of when swarming_http_headers expire, or 0 if unknown
        # or None if auth headers are disabled completely.
        # (e.g. when the bot is using IP allowlist for auth)
        'swarming_http_headers_exp',

        # An email of a service account used by the bot itself or 'none'
        # if the bot is not using OAuth for authentication.
        'bot_service_account',

        # Indicates the service account to use for internal bot processes.
        # One of:
        #   - 'none' to not use authentication at all.
        #   - 'bot' to use whatever bot is using to authenticate itself to
        #      Swarming.
        #   - <email> to get tokens through API calls to Swarming.
        'system_service_account',

        # Indicates the service account the task runs as. Same range of values
        # as for 'system_service_account'.
        #
        # It is distinct from 'system_service_account' to allow user-supplied
        # payloads to use a service account also supplied by the user (and not
        # the one used internally by the bot).
        'task_service_account',
    ])


def prepare_auth_params_json(bot, manifest):
  """Returns a dict to put into JSON file passed to task_runner.

  This JSON file contains various tokens and configuration parameters that allow
  task_runner to make HTTP calls authenticated by bot's own credentials.

  The file is managed by bot_main.py (main Swarming bot process) and consumed by
  task_runner.py.

  It lives it the task work directory.

  Args:
    bot: instance of bot.Bot.
    manifest: dict with the task manifest, as generated by the backend in /poll.
  """
  # This is "<kind>:<id>", e.g. "user:abc@example.com" or "bot:abc.example.com".
  # Service accounts appear as "user:<account-email>" strings.
  bot_ident = manifest.get('bot_authenticated_as', '')
  bot_service_account = 'none'
  if bot_ident.startswith('user:'):
    bot_service_account = bot_ident[len('user:'):]

  def account(acc_id):
    acc = (manifest.get('service_accounts') or {}).get(acc_id) or {}
    return acc.get('service_account') or 'none'

  return {
      'bot_id':
          bot.id,
      'task_id':
          manifest['task_id'],
      'swarming_http_headers':
          bot.remote.get_authentication_headers(),
      'swarming_http_headers_exp':
          bot.remote.authentication_headers_expiration,
      'bot_service_account':
          bot_service_account,
      'system_service_account':
          account('system'),
      'task_service_account':
          account('task'),
  }


def process_auth_params_json(val):
  """Takes a dict loaded from auth params JSON file and validates it.

  Args:
    val: decoded JSON value read from auth params JSON file.

  Returns:
    AuthParams tuple.

  Raises:
    ValueError if val has invalid format.
  """
  if not isinstance(val, dict):
    raise ValueError('Expecting dict, got %r' % (val,))

  bot_id = val.get('bot_id')
  if not isinstance(bot_id, six.string_types):
    raise ValueError('Expecting "bot_id" to be a string, got %r' % (bot_id,))

  task_id = val.get('task_id')
  if not isinstance(task_id, six.string_types):
    raise ValueError('Expecting "task_id" to be a string, got %r' % (task_id,))

  headers = val.get('swarming_http_headers') or {}
  if not isinstance(headers, dict):
    raise ValueError(
        'Expecting "swarming_http_headers" to be dict, got %r' % (headers,))

  exp = val.get('swarming_http_headers_exp')
  if not (exp is None or isinstance(exp, six.integer_types)):
    raise ValueError(
        'Expecting "swarming_http_headers_exp" to be int or None, got %r'
        % (exp,))

  # The headers must be ASCII for sure, so don't bother with picking the
  # correct unicode encoding, default would work. If not, it'll raise
  # UnicodeEncodeError, which is subclass of ValueError.
  headers = {str(k): str(v) for k, v in headers.items()}

  def read_account(key):
    acc = val.get(key) or 'none'
    if not isinstance(acc, six.string_types):
      raise ValueError('Expecting "%s" to be a string, got %r' % (key, acc))
    return str(acc)

  return AuthParams(
      bot_id=str(bot_id),
      task_id=str(task_id),
      swarming_http_headers=headers,
      swarming_http_headers_exp=exp,
      bot_service_account=read_account('bot_service_account'),
      system_service_account=read_account('system_service_account'),
      task_service_account=read_account('task_service_account'))


class _LockMap(object):
  """A map of locks."""

  class _LockWithRC(object):
    def __init__(self):
      self.lock = threading.Lock()
      self.ref_count = 0

  def __init__(self):
    self._global_lock = threading.Lock()
    self._individual_locks = collections.defaultdict(_LockMap._LockWithRC)

  @contextlib.contextmanager
  def lock(self, key):
    """Executes the body under a lock associated with the given key."""
    with self._global_lock:
      lock = self._individual_locks[key]
      lock.ref_count += 1
    try:
      with lock.lock:
        yield
    finally:
      with self._global_lock:
        lock.ref_count -= 1
        if not lock.ref_count:
          del self._individual_locks[key]


class AuthSystem(object):
  """Authentication subsystem used by task_runner.

  Contains two threads:
    * One thread periodically rereads the file with bots own authentication
      information (auth_params_file). This file is generated by bot_main.
    * Another thread hosts local HTTP server that servers authentication tokens
      to local processes. This is enabled only if the task is running in a
      context of some service account (as specified by 'service_account'
      parameter supplied when the task was created).

  The local HTTP server exposes /rpc/LuciLocalAuthService.GetOAuthToken
  endpoint that the processes running inside Swarming tasks can use to request
  an OAuth access token associated with the task.

  They can discover the port to connect to by looking at LUCI_CONTEXT
  environment variable. This variables is only set if the task is running in
  the context of some service account.
  """

  def __init__(self, auth_params_file):
    self._auth_params_file = auth_params_file
    self._auth_params_reader = None
    self._local_server = None
    self._lock = threading.Lock()
    self._remote_client = None
    self._rpc_locks = _LockMap()

  def set_remote_client(self, client):
    """Sets an RPC client to use when calling Swarming.

    Note that there can be a circular dependency between the RPC client and
    the auth system (the client may be using AuthSystem's get_bot_headers).

    That's the reason we allow it to be set after 'start'.

    Args:
      client: instance of remote_client.RemoteClient.
    """
    with self._lock:
      self._remote_client = client

  def start(self):
    """Grabs initial bot auth headers and starts all auth related threads.

    If the task is configured to use service accounts (based on data in
    'auth_params_file'), launches the local auth service and returns a dict that
    contains its parameters. It can be placed into LUCI_CONTEXT['local_auth']
    slot.

    Sets default service account (to be used by Swarming internal processes,
    like run_isolated.py) to 'system' (or unsets it if the bot has no associated
    service account). run_isolated.py eventually switches the default account to
    'task' before launching the actual user-supplied code.

    If task is not using service accounts, returns None (meaning, there's no
    need to setup LUCI_CONTEXT['local_auth'] at all).

    Format of the returned dict:
    {
      'rpc_port': <int with port number>,
      'secret': <str with a random string to send with RPCs>,
      'accounts': [{'id': <str>}, ...],
      'default_account_id': <str> or None
    }

    Raises:
      AuthSystemError on fatal errors.
    """
    assert not self._auth_params_reader, 'already running'
    try:
      # Read headers more often than bot_main writes them (which is 15 sec), to
      # reduce maximum possible latency between header updates and reads.
      #
      # TODO(vadimsh): Replace this with real IPC, like local sockets.
      reader = file_reader.FileReaderThread(
          self._auth_params_file, interval_sec=10)
      reader.start()
    except file_reader.FatalReadError as e:
      raise AuthSystemError('Cannot start FileReaderThread: %s' % e)

    # Initial validation.
    try:
      params = process_auth_params_json(reader.last_value)
    except ValueError as e:
      reader.stop()
      raise AuthSystemError('Cannot parse bot_auth_params.json: %s' % e)

    logging.info('Using following service accounts:')
    logging.info('  system: %s', params.system_service_account)
    logging.info('  task:   %s', params.task_service_account)

    bot_email = '-'
    if params.bot_service_account != 'none':
      logging.info('The bot itself runs as %s', params.bot_service_account)
      bot_email = params.bot_service_account

    available_accounts = []
    def add_account(account_id, email):
      if email == 'bot':
        email = bot_email
      available_accounts.append(auth_server.Account(id=account_id, email=email))

    # Expose all defined accounts (if any) to subprocesses via LUCI_CONTEXT.
    #
    # Use 'system' logical account as default for internal Swarming processes.
    # It is specified by 'system_service_account' field in bots.cfg. Swarming
    # will eventually switch to 'task' logical account before launching
    # user-supplied code. 'task' account is specified in the task definition.
    # This happens in run_isolated.py.
    #
    # If 'system_service_account' is not defined, then do not set default
    # account at all! It means internal Swarming processes will use
    # non-authenticated calls (which is precisely the meaning of un-set
    # system account).
    default_account_id = None
    if params.system_service_account != 'none':
      default_account_id = 'system'
      add_account('system', params.system_service_account)
    if params.task_service_account != 'none':
      add_account('task', params.task_service_account)

    # If using service accounts, launch local HTTP server that serves tokens
    # (let OS assign the port).
    server = None
    local_auth_context = None
    if available_accounts:
      server = auth_server.LocalAuthServer()
      local_auth_context = server.start(
          token_provider=self,
          accounts=available_accounts,
          default_account_id=default_account_id)

    # Good to go.
    with self._lock:
      self._auth_params_reader = reader
      self._local_server = server
    return local_auth_context

  def stop(self):
    """Shuts down all the threads if they are running."""
    with self._lock:
      reader, self._auth_params_reader = self._auth_params_reader, None
      server, self._local_server = self._local_server, None
    if server:
      server.stop()
    if reader:
      reader.stop()

  def get_bot_headers(self):
    """HTTP headers that contain bots own credentials and their expiration time.

    Such headers can be sent to Swarming server's /bot/* API. Must be used only
    after 'start' and before 'stop'.

    Returns:
      Pair (headers dict, expiry_timestamp), where expiry_timestamp is
        int unix timestamp in seconds, if the expiration time is known
        0, if the expiration time is not known
        None, if the bot is not using auth headers at all

    Raises:
      AuthSystemError if auth_params_file is suddenly no longer valid.
    """
    with self._lock:
      assert self._auth_params_reader, '"start" was not called'
      raw_val = self._auth_params_reader.last_value
    try:
      val = process_auth_params_json(raw_val)
      return val.swarming_http_headers, val.swarming_http_headers_exp
    except ValueError as e:
      raise AuthSystemError('Cannot parse bot_auth_params.json: %s' % e)

  def generate_token(self, account_id, scopes):
    """Generates a new access token with given scopes.

    Called by LocalAuthServer from some internal thread whenever new token is
    needed. It happens infrequently, approximately once per hour per combination
    of scopes (when the previously cached token expires).

    See TokenProvider for more details.

    Args:
      account_id: logical account name (e.g 'system' or 'task').
      scopes: list of OAuth scopes.

    Returns:
      AccessToken.

    Raises:
      RPCError, TokenError, AuthSystemError.
    """
    # Grab AuthParams supplied by the main bot process.
    with self._lock:
      if not self._auth_params_reader:
        raise auth_server.RPCError(503, 'Stopped already.')
      val = self._auth_params_reader.last_value
      rpc_client = self._remote_client
    auth_params = process_auth_params_json(val)

    # Note: 'account_id' here is "task" or "system", it's checked below.
    logging.info('Getting %r token, scopes %r', account_id, scopes)

    # Grab service account email (or 'none'/'bot' placeholders) of requested
    # logical account. This is part of the task manifest.
    service_account = None
    if account_id == 'task':
      service_account = auth_params.task_service_account
    elif account_id == 'system':
      service_account = auth_params.system_service_account
    else:
      raise auth_server.RPCError(404, 'Unknown account %r' % account_id)

    # Note: correctly behaving clients aren't supposed to hit this, since they
    # should use only accounts specified in 'accounts' section of LUCI_CONTEXT.
    if service_account == 'none':
      raise auth_server.TokenError(
          1, 'The task has no %r account associated with it' % account_id)

    if service_account == 'bot':
      # This works only for bots that use OAuth for authentication (e.g. GCE
      # bots). It will raise TokenError if the bot is not using OAuth.
      tok = self._grab_bot_token(auth_params)
    else:
      # Ask Swarming server to generate a new token for us.
      if not rpc_client:
        raise auth_server.RPCError(500, 'No RPC client, can\'t fetch token')
      tok, service_account = self._grab_token_via_rpc(
          auth_params, rpc_client, account_id, scopes)

    if tok.expiry - time.time() < 0:
      raise auth_server.RPCError(
          500, ('The new %r token (belonging to %r) has already expired (%d vs '
                '%d). Check the system clock.' % (
                    account_id, service_account, tok.expiry, time.time())))

    logging.info('Got %r token (belongs to %r), expires in %d sec', account_id,
                 service_account, tok.expiry - time.time())
    return tok

  def _grab_bot_token(self, auth_params):
    """Extracts OAuth token from 'Authorization' header used by the bot itself.

    This works only for bots that use OAuth for authentication (e.g. GCE bots).
    Also it totally ignores scopes. It relies on bot_main to keep the bot OAuth
    token sufficiently fresh. See remote_client.AUTH_HEADERS_EXPIRATION_SEC.

    Args:
      auth_params: AuthParams tuple with configuration.

    Returns:
      auth_server.AccessToken.
    """
    bot_auth_hdr = auth_params.swarming_http_headers.get('Authorization') or ''
    if not bot_auth_hdr.startswith('Bearer '):
      raise auth_server.TokenError(2, 'The bot is not using OAuth')
    tok = bot_auth_hdr[len('Bearer '):]

    # Default to some safe small expiration in case bot_main doesn't report it
    # to us. This may happen if get_authentication_header bot hook is not
    # reporting expiration time.
    exp = auth_params.swarming_http_headers_exp or (time.time() + 4*60)

    # TODO(vadimsh): For GCE bots specifically we can pass a list of OAuth
    # scopes granted to the GCE token and verify it contains all the requested
    # scopes.
    return auth_server.AccessToken(tok, exp)

  def _grab_token_via_rpc(self, auth_params, rpc_client, account_id, scopes):
    """Makes RPC to Swarming to mint a token.

    Args:
      auth_params: AuthParams tuple with configuration.
      rpc_client: instance of remote_client.RemoteClient to use for RPC.
      account_id: logical account name (e.g 'system' or 'task').
      scopes: list of OAuth scopes.

    Returns:
      (auth_server.AccessToken, <service account email>).
    """
    # Clients of AuthSystem can bombard it with parallel requests for the exact
    # same OAuth token (imagine a task launching N subprocesses in parallel,
    # each one requesting a token). We stop this concurrency here with a battery
    # of locks keyed by (account_id, sorted(scopes)). So the Swarming will see
    # only one request at a time.
    with self._rpc_locks.lock(key=(account_id, tuple(sorted(scopes)))):
      try:
        # WARNING: This call may indirectly call 'get_bot_headers', so we have
        # to use a different lock here (not self._lock).
        resp = rpc_client.mint_oauth_token(
            task_id=auth_params.task_id,
            account_id=account_id,
            scopes=scopes)
      except remote_client.InternalError as exc:
        # Raising RPCError propagates transient error status to clients, so that
        # they can decide to retry later.
        raise auth_server.RPCError(500, str(exc))
      except remote_client.MintOAuthTokenError as exc:
        # Raising fatal TokenError makes LocalAuthServer cache the error, so
        # that retrying clients get the error reply right away, without hitting
        # Swarming server.
        raise auth_server.TokenError(4, str(exc))

    # This is <email>, 'bot' or 'none'. We should handle all cases, since
    # the configuration on the server can change while the bot is running
    # the task. This is bad, but possible.
    service_account = resp.get('service_account') or 'unknown'
    if service_account == 'none':
      raise auth_server.TokenError(
          1, 'The task has no %r account associated with it' % account_id)
    if service_account == 'bot':
      return self._grab_bot_token(auth_params), 'bot'

    # Should have a real token here now. Double check and return. It will be
    # cached by LocalAuthServer until it expires.
    access_token = resp.get('access_token')
    expiry = resp.get('expiry')
    if not access_token or not isinstance(access_token, six.string_types):
      raise auth_server.RPCError(500, 'Bad server reply, no valid token given')
    if not expiry or not isinstance(expiry, six.integer_types):
      raise auth_server.RPCError(500, 'Bad server reply, no token expiry given')

    # Normalize types (unicode -> str, long -> int).
    tok = auth_server.AccessToken(str(access_token), int(expiry))
    return tok, str(service_account)