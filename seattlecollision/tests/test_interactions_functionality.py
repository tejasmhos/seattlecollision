"""
Module to test interactions_functionality module


TODO comolete doctrsing
"""
import sys
import unittest
sys.path.append('seattlecollision/')
sys.path.append('seattlecollsion/data')
import interactions_functionality as int_func #pylint: disable=wrong-import-position

<<<<<<< HEAD
TEST_CONNECTION = int_func.generate_connection("../data/Collidium")
TEST_DF = int_func.generate_table("select * from collidium_data", data_directory="../data/Collidium") #pylint: disable=line-too-long
=======
TEST_DB = int_func.generate_connection("seattlecollision/data/Collidium")
TEST_DB.execute("select * from collidium_data")
TEST_DF = TEST_DB.fetchall()
>>>>>>> c8f06aa5d8295f6b7522eb5cc6d4b274d05c1055



class TestGenerateConnections(unittest.TestCase):
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
        '''Tests whether function connects to DB with the correct column names.'''
        true_cols = set(['b_category', 'b_end_dt', 'b_id', 'b_lat', 'b_long', 'b_start_dt', 'base_year', 'c_dt', 'c_id', 'c_lat', 'c_long', 'c_severity', 'c_type', 'coll_after', 'coll_before', 'coll_days_from_build', 'coll_during', 'radius']) #pylint: disable=line-too-long
        TEST_CONNECTION.execute('PRAGMA TABLE_INFO({})'.format('collidium_data'))
        test_cols = TEST_CONNECTION.execute('PRAGMA TABLE_INFO({})'.format('collidium_data'))
        test_cols = set([tup[1] for tup in TEST_CONNECTION.fetchall()])
        test_cols = set(test_cols)
        self.assertTrue(test_cols == true_cols)

    def test_data_table_size(self):
        '''Ensures function connects to DB with at least 10,000 rows.'''
        TEST_CONNECTION.execute('select count(*) from collidium_data')
        table_size = TEST_CONNECTION.fetchall()[0][0]
        self.assertTrue(table_size > 10000)


    def test_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(Exception, int_func.generate_connection, 'badPath')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGenerateConnections)
_ = unittest.TextTestRunner().run(SUITE)

class TestGenerateCategories(unittest.TestCase):
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

    def test_cols_needed(self):
        """Tests that invalid input raises an IndexError"""
        bad_cols_needed = ["bad_category", "base_year", "c_severity", "c_type"]
        self.assertRaises(IndexError, int_func.generate_categories, bad_cols_needed, data_directory="../data/Collidium") #pylint: disable=line-too-long

    def test_output(self):
        '''Ensures function outputs the correct lists.'''
        cols_needed = ["b_category", "base_year", "c_severity", "c_type"]
        test_categories = int_func.generate_categories(cols_needed, data_directory="../data/Collidium") #pylint: disable=line-too-long
        true_output = (['All', 'COMMERCIAL', 'MULTIFAMILY', 'INDUSTRIAL', 'INSTITUTIONAL', 'SINGLE FAMILY / DUPLEX'], ['All', 2016, 2015, 2017, 2014, 2013], ['All', 'Property Damage Only', 'Injury', 'Serious Injury', 'Fatality'], ['All', 'Vehicle Only', 'Bike/Pedestrian']) #pylint: disable=line-too-long
        self.assertTrue(test_categories == true_output)


    def test_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(Exception, int_func.generate_categories, 'badPath')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGenerateCategories)
_ = unittest.TextTestRunner().run(SUITE)


class TestGenerateTable(unittest.TestCase):
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
        self.assertTrue(len(list(TEST_DF)) > 0)

    def test_data_frame_size(self):
        '''Ensures function returns output with at least 100 rows.'''
        self.assertTrue(TEST_DF.shape[0] > 10000)

    def test_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(Exception, int_func.generate_table, 'badPath')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGenerateTable)
_ = unittest.TextTestRunner().run(SUITE)
