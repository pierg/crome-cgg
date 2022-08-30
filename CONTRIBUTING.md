# Contributing

Contributions are welcome, and they are greatly appreciated!

## Tasks

This project uses [duty](https://github.com/pawamoy/duty) to run tasks.
A Makefile is also provided.

## Development

As usual:

1. create a new branch: `git checkout -b feature-or-bugfix-name`
1. edit the code and/or the documentation

**Before committing:**

1. run `make format` to auto-format the code
1. run `make check` to check everything (fix any warning)
1. run `make test` to run the tests (fix any issue)
1. if you updated the documentation or the project dependencies:
    1. run `make docs-serve`
    1. go to http://localhost:8000 and check that everything looks good
