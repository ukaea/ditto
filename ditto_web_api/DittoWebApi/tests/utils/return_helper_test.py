import unittest
from DittoWebApi.src.utils.return_helper import return_dict


class TestReturnHelper(unittest.TestCase):
    def test_correct_return_when_message_is_added_for_return_dict(self):
        message = "Some text"
        test_dict = return_dict(files_transferred=5,
                                files_skipped=2,
                                files_updated=4,
                                data_transferred=102,
                                message=message)
        self.assertEqual(test_dict, {"Message": message,
                                     "Files transferred": 5,
                                     "Files updated": 4,
                                     "Files skipped": 2,
                                     "Data transferred (bytes)": 102})

    def test_correct_return_when__no_message_is_added_for_return_dict(self):
        test_dict = return_dict(files_transferred=6,
                                files_skipped=3,
                                files_updated=1,
                                data_transferred=2532,)
        self.assertEqual(test_dict, {"Message": "",
                                     "Files transferred": 6,
                                     "Files updated": 1,
                                     "Files skipped": 3,
                                     "Data transferred (bytes)": 2532})

    def test_default_dict_returned_when_return_dict_called_with_no_args(self):
        test_dict = return_dict()
        self.assertEqual(test_dict, {"Message": "",
                                     "Files transferred": 0,
                                     "Files updated": 0,
                                     "Files skipped": 0,
                                     "Data transferred (bytes)": 0})
