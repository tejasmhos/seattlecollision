"""
This module is used to perform unit testing on the table_builder.py
module. It is to be eventually added to a single file that will
perform unit testing on all our modules.
"""
import unittest
import sys
from io import StringIO
sys.path.append('seattlecollision/build_data_libraries/')
sys.path.append('seattlecollision/data')
#pylint: disable=wrong-import-position
#pylint: disable=import-error
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

    def test_print_message(self):
        """
        Testing if a message is printed once the database
        is constructed.
        :param: self
        :return pass if correct message is printed, fail otherwise
        """
        _saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        table_builder.create_table('seattlecollision/data/test_db_for_unittest.db',
                                   'seattlecollision/data/collidium_data.csv')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Dataprocessing: sqlite database constructed. (Woohoo!)')

if __name__ == '__main__':
    unittest.main()
