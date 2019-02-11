# Web Components Swarming UI


This is the Web Components based UI. It aims to be lighter-weight and more
future-proof than the current Polymer v1 UI, but functionally identical.

## Prerequisites

You will need to install a recent version of node.js and npm (they usually
come together). You can either install it through `bash` or manually download
and extract it somewhere (e.g. `~/bin`) from the web site https://nodejs.org/en/download/.

The version available via apt-get is likely way way way too old.

### npm via bash

To install in the local user (as `~/nodejs` in this example), use:

    echo prefix = ~/nodejs >> ~/.npmrc
    mkdir ~/nodejs
    cd ~/nodejs
    curl https://nodejs.org/dist/v8.11.2/node-v8.11.2-linux-x64.tar.xz | tar xJ --strip-components=1
    export PATH="$PATH:$HOME/nodejs/bin"

## Building

To build the pages for deploying, run:

    make release

The output of the dist/ folder will have the bundled HTML, JS and CSS files.
This should be checked in so as to fit with the App Engine deployment setup.

## Using the demo pages

To build the pages locally for demoing/developing, run:

    make serve

Then, navigate to <http://localhost:8080/newres/swarming-index.html> to see
one of the demo pages.  You can navigate to newres/[foo] where foo is one
of the modules (found in ./modules/) or one of the top level HTML files
(found in ./pages/). The pages in ./modules have mock data, so those are
generally more useful.

The list of all demo pages so far (for easy clicking):

  - [bot-list](http://localhost:8080/newres/bot-list.html)
  - [bot-mass-delete](http://localhost:8080/newres/bot-mass-delete.html)
  - [sort-toggle](http://localhost:8080/newres/sort-toggle.html)
  - [swarming-app](http://localhost:8080/newres/swarming-app.html)
  - [swarming-index](http://localhost:8080/newres/swarming-index.html)
  - [task-list](http://localhost:8080/newres/task-list.html)
  - [task-mass-cancel](http://localhost:8080/newres/task-mass-cancel.html)

By default, the login is mocked so it works w/o an internet connection,
but if testing the real OAuth 2.0 flow is desired, a client_id may be
specified (see `swarming-index-demo.html` for an example). Be sure to also
whitelist `localhost:8080` for that client_id.

## Running the tests

Any file matching `modules/**/*_test.js` will automatically be added to the test suite.
When developing tests, it is easiest to put the tests in "automatically rebuild and run"
mode, which can be done with `make continuous_test`.

To run all tests exactly once on Firefox and Chrome (assuming those browsers are present):

    make test

## Generating the docs

We use [JSDoc](http://usejsdoc.org/) to document the modules. While the documentation is readable
inline, it can be easier to browse in a web browser.

To generate the HTML docs, run

    make docs

which will open docs/index.html after build.

## Misc

If `make *` is calling `npm install` every time, try `touch package-lock.json`. This should tell
Makefile that the "built" `package-lock.json` file is older than the "source"
`package.json` and thus does not require to be "rebuilt".