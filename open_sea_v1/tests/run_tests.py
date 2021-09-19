from unittest import TestLoader, TextTestRunner


SKIP_SLOW_TESTS = True

def discover_and_run_tests() -> None:
    loader = TestLoader()
    tests = loader.discover('..', pattern='test_*')
    test_runner = TextTestRunner(verbosity=1)
    test_runner.run(tests)


if __name__ == '__main__':
    discover_and_run_tests()
