# Eqator

Checking the Django project for quality. It can be convenient if you include it in CI.

Used packages: 

* [django unittest](https://docs.djangoproject.com/en/3.1/topics/testing/overview/) - unit testing in Django.
* [flake8](https://pypi.org/project/flake8/) - linter of source code.
* [radon](https://pypi.org/project/radon/) - tool that computes various metrics from the source code.
* [bandit](https://pypi.org/project/bandit/) - a security linter from PyCQA.
* [coverage](https://pypi.org/project/coverage/) - a test coverage for unittest.

## Quickstart

Install with pip:

```bash
pip install eqator
```

Add the `eqator` to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'eqator',
]
```

To use Lighthouse scoring, install `Lighthouse CI` with `npm`:

```bash
npm install -g @lhci/cli
```

Check your project:

```bash
python manage.py qa
```


Check your project by separate options.

Run checking style guide with flake8:

```bash
python manage.py qa -f
```

```bash
python manage.py qa --flake
```

Run checking cyclomatic complexity with radon

```bash
python manage.py qa -r
```

```bash
python manage.py qa --radon
```

Run security lint with bandit

```bash
python manage.py qa -l
```

```bash
python manage.py qa --linter
```

Run django project migrations check

```bash
python manage.py qa -m
```

```bash
python manage.py qa --migrations
```

Run django unittest

```bash
python manage.py qa -t
```

```bash
python manage.py qa --tests
```

Run django unit tests for garpix_page

```bash
python manage.py qa -p
```

```bash
python manage.py qa --garpix_page
```

Lighthouse CI check:

(requires Lighthouse CI installed)

```bash
python manage.py qa -lh
```

```bash
python manage.py qa --lighthouse
```

Run test coverage check

```bash
python manage.py qa -c
```

```bash
python manage.py qa --test_coverage
```

Note, that you need to add `TEST_COVERAGE_RATE` variable to your `settings.py` file (default value is 70):

```python
TEST_COVERAGE_RATE = 70
```

Optionally, do not save Lighthouse CI report files:

```bash
python manage.py qa --all --clear-reports
```

Check your project with all logs:

```bash
python manage.py qa --verbose
```

You can also add add `SENTRY_CHECK_METHOD` and `LIGHTHOUSE_CHECK_METHOD` variables to your `settings.py` file to controle the sentry SDK and lighthouse CI checking methods:

```python
# settings.py
SENTRY_CHECK_METHOD = 'error'
LIGHTHOUSE_CHECK_METHOD = 'warning'
```


### Example output with OK

```
Input

  Directory: /Users/aleksejkuznecov/projects/garpix_packages/eqator/backend
  Start at: 2021-02-27 12:09:30.999142

Checking

  Checking style guide with flake8 (see ".flake8") OK
  Django unit tests OK
  Cyclomatic complexity with radon (see "radon.cfg") OK
  Security lint with bandit (only high-severity issues, see ".bandit") OK

Result

  Problems found: 0
  End at: 2021-02-27 12:09:33.789880
  Duration: 0:00:02.790738

```

### Example output with problems

```
Input

  Directory: /Users/aleksejkuznecov/projects/garpix_packages/eqator/backend
  Start at: 2021-02-27 12:23:41.066752

Checking

  Checking style guide with flake8 (see ".flake8") ERROR
/Users/aleksejkuznecov/projects/garpix_packages/eqator/backend/eqator/constants.py:18:4: W292 no newline at end of file
/Users/aleksejkuznecov/projects/garpix_packages/eqator/backend/eqator/helpers.py:38:1: E302 expected 2 blank lines, found 1
/Users/aleksejkuznecov/projects/garpix_packages/eqator/backend/eqator/colors.py:9:1: W391 blank line at end of file

  Django unit tests OK
  Cyclomatic complexity with radon (see "radon.cfg") OK
  Security lint with bandit (only high-severity issues, see ".bandit") ERROR
[main]  INFO    Found project level .bandit file: /Users/aleksejkuznecov/projects/garpix_packages/eqator/backend/.bandit
[main]  INFO    profile include tests: None
[main]  INFO    cli include tests: None
[main]  INFO    cli exclude tests: None
[main]  INFO    running on Python 3.8.2
Run started:2021-02-27 12:23:45.044503

Test results:
>> Issue: [B602:subprocess_popen_with_shell_equals_true] subprocess call with shell=True identified, security issue.
   Severity: High   Confidence: High
   Location: /Users/aleksejkuznecov/projects/garpix_packages/eqator/backend/eqator/helpers.py:39
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b602_subprocess_popen_with_shell_equals_true.html
38      def shell_run(cmd):
39          ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
40          lines = ps.communicate()[0]

--------------------------------------------------
Code scanned:
        Total lines of code: 285
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0.0
                Low: 1.0
                Medium: 0.0
                High: 1.0
        Total issues (by confidence):
                Undefined: 0.0
                Low: 0.0
                Medium: 0.0
                High: 2.0
Files skipped (0):


Result

  Problems found: 2
  End at: 2021-02-27 12:23:45.098015
  Duration: 0:00:04.031263

```

## Configure Lighthouse CI
Edit `lighthouserc.json` to set URL and configure assertions. 

Reference: https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md

## Configure TestCase unit tests
Edit `testcaserc.json` to add configure options.

All available configurations:

- `apps` - list of apps must be tested;
- `keepdb` - preserves the test DB between runs;
- `top_level` - top level of project for unittest discovery;
- `pattern` - the test matching pattern. Defaults to test*.py;
- `reverse` - reverses test cases order;
- `debug_sql` - sets settings.DEBUG to True;
- `parallel` - run tests using up to N parallel processes;
- `tags` - run only tests with the specified tag;
- `exclude_tags` - do not run tests with the specified tag;
- `pdb` - runs a debugger (pdb, or ipdb if installed) on error or failure;
- `buffer` - discard output from passing tests;
- `test_name_patterns` - Only run test methods and classes that match the pattern or substring

Example:

```json
{
    "apps": ["app"],
}
```

## Send report

To send statistics you need to add `EQATOR_SEND_HOST`:
```python
# settings.py

EQATOR_SEND_HOST = 'http://example.com/analytics/eqator/:project_name/'
```

```bash
python manage.py qa --send
```

Data format

```json
{
  "duration": "0:00:01.557757",
  "start_at": "2022-09-20 11:56:41.230550",
  "error_count": 4,
  "flake_count": 2,
  "radon_count": 1,
  "sentry_count": 0,
  "coverage_value": 8,
  "coverage_result": 0,
  "lighthouse_count": 0,
  "migrations_count": 1,
  "unit_tests_count": 0,
  "security_linter_count": 0,
  "garpix_page_tests_count": 0
}
```
