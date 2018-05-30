"""
Module to test interactions_functionality module


TODO comolete doctrsing
"""
import sys
import unittest
sys.path.append('seattlecollision/')
sys.path.append('seattlecollsion/data')
import interactions_functionality as int_func #pylint: disable=wrong-import-position

TEST_DB = int_func.generate_connection("seattlecollision/data/Collidium")
TEST_DB.execute("select * from collidium_data")
TEST_DF = TEST_DB.fetchall()

class ConnectionTests(unittest.TestCase):
    '''Conducts test on the performance of the generate_connections function.
    
    This class tests three functions in the interactions_functionality module.
    These include the generate_connection function, the generate_categories 
    function and the generate_table function. The other functions in this module 
    (those ending in _interact) are not tested in this module because they generate
    elements of the user interface that cannot be tested by unit tests.

    This class conducts three tests, for the pupose of validating the functionality
    of the interactions_functionality module. Each test is conducted within a function, as
    follows:

    Functions:
       TO DO:

    Returns: A human readable string that provides a summary of results of the five tests
        conducted within this class.
    '''

    def test_col_names(self):
        '''Tests whether function output has correct column names.'''
        true_cols = set(['b_category', 'b_end_dt', 'b_id', 'b_lat', 'b_long', 'b_start_dt', 'base_year', 'c_dt', 'c_id', 'c_lat', 'c_long', 'c_severity', 'c_type', 'coll_after', 'coll_before', 'coll_days_from_build', 'coll_during', 'radius']) #pylint: disable=line-too-long
        TEST_DB.execute('PRAGMA TABLE_INFO({})'.format('collidium_data'))
        test_cols = TEST_DB.execute('PRAGMA TABLE_INFO({})'.format('collidium_data'))
        test_cols = set([tup[1] for tup in TEST_DB.fetchall()])
        test_cols = set(test_cols)
        self.assertTrue(test_cols == true_cols)

    def test_data_table_size(self):
        '''Ensures function returns output with at least 10,000 rows.'''
        self.assertTrue(len(TEST_DF) > 10000)


    def test_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(Exception, int_func.generate_connection, 'badPath')


SUITE = unittest.TestLoader().loadTestsFromTestCase(ConnectionTests)
_ = unittest.TextTestRunner().run(SUITE)
