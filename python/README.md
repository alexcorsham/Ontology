# Python

We've used [Pipenv](https://pypi.org/project/pipenv/) for dependency and virtual environment management. If you've not
used Pipenv before, a TLDR is:

- Use `pipenv shell` to enter the virtual environment. Your dependencies will be present in the Python path
- After cloning, run `pipenv sync --dev` to install everything specified in the lockfile
- Use `pipenv install <dependency>` to install a regular dependency
- Use `pipenv install --dev <dev-dependency>` to install a development-only dependency (e.g. testing libraries)

## Testing

Tests have been pre-set up in this directory. To run the tests, use `pipenv run test`.

Tests are run using `pytest`. You can pass command line options to `pipenv run test` exactly as you would to `pytest` -
perhaps the most useful one is `-k <pattern>`, which selects a subset of tests to run. For example,
`pipenv run test -k "is_ginger_an_animal"` will run the one test with a matching function name. See more CLI options
[here](https://docs.pytest.org/en/6.2.x/usage.html).

## Linting

Linting has been set up in this directory. To lint your code, use `pipenv run fmt`. This command runs both the
[Black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) formatters with default settings.
