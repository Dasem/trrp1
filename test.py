import unittest
import os
from main import *


class FullTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global service
        service = auth()

    # body of the constructor

    def test_list(self):
        test = show_list()
        self.assertEqual('oracle_11gR2' in test, True)

    def test_download(self):
        download_file('1YTnBVA7GFlCnWm8yDiCPahpKSlcFeK0I', 'test_file')
        for file in os.listdir("")
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
