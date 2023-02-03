import unittest
from assignment.d_preparation import file_opener


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.file1 = file_opener('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562')
        self.file2 = file_opener('API_SP.POP.TOTL_DS2_en_csv_v2_4751604')
        self.file3 = file_opener('co2-fossil-by-nation_zip')

    def test_file_checker(self):
        self.assertIsNotNone(self.file1, "Upload correct gdp file!")
        self.assertIsNotNone(self.file2, "Upload correct pop file!")
        self.assertIsNotNone(self.file3, "Upload correct emissions file!")


if __name__ == '__main__':
    unittest.main()
