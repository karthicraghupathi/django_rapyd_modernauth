#!/usr/bin/env python

import os
import sys

# set Django root folder here
APP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "testproject")
sys.path.insert(0, APP_DIR)

# specify the Django settings module
os.environ["DJANGO_SETTINGS_MODULE"] = "testproject.settings"


def main():
    # initialize Django
    import django

    django.setup()

    # instantiate the test runner
    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)

    # run tests
    test_runner = TestRunner(verbosity=1, interactive=False)
    failures = test_runner.run_tests(["modernauth"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
