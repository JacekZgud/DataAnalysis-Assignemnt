import unittest

from assignment.functions import file_opener


class MyTestCase(unittest.TestCase):
    def file_checker(self):
        file1 = file_opener('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562')
        file2 = file_opener('API_SP.POP.TOTL_DS2_en_csv_v2_4751604')
        file3 = file_opener('co2-fossil-by-nation_zip')
        self.assertIsNotNone(file1, "Upload correct gdp file!")
        self.assertIsNotNone(file2, "Upload correct pop file!")
        self.assertIsNotNone(file3, "Upload correct emissions file!")

    def correct_date_format(self):
        self.assertTrue()


if __name__ == '__main__':
    unittest.main()
