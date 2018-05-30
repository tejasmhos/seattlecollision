"""
This module is used to perform unit testing on the table_builder.py
module. It is to be eventually added to a single file that will
perform unit testing on all our modules.
"""
import unittest
import sys
sys.path.append('seattlecollision/build_data_libraries/')
import table_builder


class TestTableBuilder(unittest.TestCase):
    """
    This class subclasses unittest.TestCase to define a testcase. Each
    test case method starts with the word test followed by a description
    of what the test case does.
    """

    def test_invalid_path(self):
        """
        Testing if value error is raised.
        :param: self
        :return: pass if correct exception is raised, fail otherwise.
        """
        self.assertRaises(
            ValueError, table_builder.create_table,
            'Sample.db', 'some_fake_path')

    def test_no_csv(self):
        """
        Testing if no CSV files in a folder raises a value error.

        :param: self
        :return: pass if correct exception is raised, fail otherwise
        """
        self.assertRaises(
            ValueError, table_builder.create_table,
            'Sample.db', '/empty_folder')


if __name__ == '__main__':
    unittest.main()
