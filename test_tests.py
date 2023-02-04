import unittest
from assignment.d_preparation import years_range


class MyTestCase(unittest.TestCase):
    def test_years_checker(self):
        years_range()
        years_range()

    if __name__ == '__main__':
        unittest.main()
