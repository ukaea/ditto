import unittest
from DittoWebApi.src.utils.return_helper import return_transfer_summary


class TestReturnHelper(unittest.TestCase):
    def test_correct_return_when_message_is_added_for_return_dict(self):
        message = "Some text"
        test_dict = return_transfer_summary(new_files_uploaded=5,
                                            files_skipped=2,
                                            files_updated=4,
                                            data_transferred=102,
                                            message=message)
        self.assertEqual(test_dict, {"message": message,
                                     "new files uploaded": 5,
                                     "files updated": 4,
                                     "files skipped": 2,
                                     "data transferred (bytes)": 102})

    def test_correct_return_when__no_message_is_added_for_return_dict(self):
        test_dict = return_transfer_summary(new_files_uploaded=6,
                                            files_skipped=3,
                                            files_updated=1,
                                            data_transferred=2532, )
        self.assertEqual(test_dict, {"message": "",
                                     "new files uploaded": 6,
                                     "files updated": 1,
                                     "files skipped": 3,
                                     "data transferred (bytes)": 2532})

    def test_default_dict_returned_when_return_dict_called_with_no_args(self):
        test_dict = return_transfer_summary()
        self.assertEqual(test_dict, {"message": "",
                                     "new files uploaded": 0,
                                     "files updated": 0,
                                     "files skipped": 0,
                                     "data transferred (bytes)": 0})
