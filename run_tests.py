import unittest


if __name__ == '__main__':
    test_suite = unittest.TestLoader().discover('./tests')
    result = unittest.TextTestRunner().run(test_suite)
    exit(0) if result.wasSuccessful() else exit(1)
