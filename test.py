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
        for file in os.listdir("."):
            if file == 'test_file':
                os.remove("test_file")
                return
        self.assertEqual(True, False)

    def test_upload_delete(self):
        upload_file('test.py', 'test_remote')

        test = show_list()
        self.assertEqual('test_remote' in test, True)

        delete_file(get_id_by_name('test_remote'))

        test = show_list()
        self.assertEqual('test_remote' in test, False)

    def test_update(self):
        upload_file('test.py', 'test_remote')
        change_file_name(get_id_by_name('test_remote'), 'test_renamed_remote')

        test = show_list()
        self.assertEqual('test_renamed_remote' in test, True)
        delete_file(get_id_by_name('test_renamed_remote'))


if __name__ == '__main__':
    unittest.main()
