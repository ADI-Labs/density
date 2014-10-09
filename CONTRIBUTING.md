
#Contributing

1. Fork the [adicu repository](https://github.com/adicu/density)
2. Make your changes
3. Write the corresponding tests in the `density/tests/` directory
4. Submit a pull request to master


##Setting up your fork

1. Use the fork button on the [website](https://github.com/adicu/density)
2. Clone the repo
  - `git clone git@github.com:< USERNAME >/density.git`
3. Configure the remote repo
  - `git remote add git@github.com:adicu/density`
4. Activate [Travis-CI](https://travis-ci.org/) on your fork.


##Pull Requests

If you are unsure of how to implement a feature you are working on ore are looking for feedback, please keep an open pull request as you go.
It's then easy to monitor and comment on how you're going about your implementation.
We will not merge your pull request until the build is passing and you signal that it is ready.


##Syntax

We will use [PEP8](http://www.python.org/dev/peps/pep-0008/) syntax for all Python files.
There are a variety of linters installable for vim and sublime that will check this as you code.
Travis-CI will check with a linter everytime the build is executed.


##Pulling in changes

1. `git fetch upstream`
2. `git merge upstream/master`


##Using Travis-CI

Travis will automatically run all defined tests as well as a [PEP8](http://www.python.org/dev/peps/pep-0008/) linter.
Travis-CI will email you with the build status every time you push code to your fork.
The tests will also be run on every pull request opened on [adicu repo](https://github.com/adicu/data.adicu.com)


##Testing

All tests for the API are located in the `density/tests/` directory.
Each file has a correpsonding tests file.

Every method should have 1-3 tests depending on it's functionality options.
There should be a test for every possible exception as well as every possible parameter option.

For testing endpoints please examine the `density/tests/template.py` to lessen the amount of boilerplate for each test.

