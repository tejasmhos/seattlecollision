"""
Module to test interactions_functionality module

Module summary:
    This module tests the functionality of the interactions_functionality module. It
    includes five classes, each aimed at testing a different portion of the module. These
    classes include the following:

Classes:
    TestGenerateConnections: This class conducts three tests on the generate_connection
        function. It uses a sample connection called TEST_CONNECTION and validates that
        the sample connection connects to a table with the required column names, and
        that is at least a minimum of 10,000 rows long. Additionally the class validates
        that the function will raise a ValueError if it is connected to an invalid
        directory.

    TestGenerateCategories: This class conducts three tests on the generate_categories
        function. The first test, validates that an IndexError is raised if the user
        enters invalid input. The second validates that the output generated is correct,
        and the third validates that the function will raise a ValueError if it is
        connected to an invalid directory.

    TestGenerateTable: This class conducts three tests on the generate_table function.
        The first test alidates that the function assigns column names to the table.
        The next test ensures function returns output with at least 100 rows and the
        final test validates that an invalid path raises a ValueError exception.

    TestInteractPath: This class conducts a test on each of the "*_interact" functions in
        the interactions_functionality module. It validates a ValueError is raised if
        any of those functions is passed a bath path.

    TestInteractFunctions: This class conducts a test on each of the "*_interact"
        functions in the interactions_functionality module. It validates that the
        those functions execute when none of the functions or classes
        that compose them throw an error, and raises an assertion error if the function
        throws an error.

Exceptions:
    AssertionError: If a test fails the class will raise an assertion error, and describe
        which test failed

Attributes:
    TEST_DF: This is a sample dataframe that was createdy by the function generate_table
        in the module interactions_functionality. It's used to conduct tests throughout this module.

    TEST_CONNECTION: This is a sample dataframe createdy by the function generate_connection in
        the module interactions_functionality. It is used to conduct tests throughout this module.

    DATA_DIRECTORY: Is the location of the data. There directory "seattlecollision/data/Collidium"
        should be used when uploading to git hub to ensure testing is possible through travis and
        coveralls. The directory "../data/Collidium" should be selected when running on a
        local machine.

"""
import sys
import unittest

sys.path.append('../')
sys.path.append('seattlecollision/')
sys.path.append('seattlecollision/data')
sys.path.append('seattlecollision/tests')
#pylint: disable=import-error
#pylint: disable=wrong-import-position
import interactions_functionality as int_func

DATA_DIRECTORY = "seattlecollision/data/Collidium" # Select if running on Travis, else comment out
# DATA_DIRECTORY = "../data/Collidium" # Select this if running on local machine, else comment out.

TEST_CONNECTION = int_func.generate_connection(DATA_DIRECTORY)
TEST_DF = int_func.generate_table("select * from collidium_data",
                                  data_directory=DATA_DIRECTORY)

class TestGenerateConnections(unittest.TestCase):
    '''Conducts test on the performance of the generate_connections function.

    This class tests the generate_connections function. It conducts three tests, for
    the pupose of validating the functionality of the function.

    Functions:
        test_col_names: Tests whether function connects to a database with the correct column names.
            Parameters: self
            Returns: Pass if column names are same as prescribed column names, and fail otherwise.

        test_data_table_size: Ensures function connects to a database with at least 10,000 rows.
            Parameters: self
            Returns: Pass if table size is more than 10,000, and fail otherwise.

        test_invalid_path_error: Tests whether an invalid path raises a ValueError exception.
            Parameters: self
            Returns: Pass if table invalid path raises exception, and fail otherwise.

    Returns: A human readable string that provides a summary of results of the five tests
        conducted within this class.
    '''

    def test_col_names(self):
        '''Tests whether function connects to DB with the correct column names.'''
        true_cols = set(['b_category', 'b_end_dt', 'b_id', 'b_lat', 'b_long', 'b_start_dt',
                         'base_year', 'c_dt', 'c_id', 'c_lat', 'c_long', 'c_severity', 'c_type',
                         'coll_after', 'coll_before', 'coll_days_from_build', 'coll_during',
                         'radius'])
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
    '''Conducts test on the performance of the generate_categories function.

    This class tests the generate_categories function. It conducts three tests, for
    the pupose of validating the functionality of the function. Each test is contained
    in a function as follows:

    Functions:
        test_cols_needed: Tests whether function recieved valid input
            Parameters: self
            Returns: Pass if inputs are same as prescribed column names, and fail otherwise.

        test_output: Ensures function expected output.
            Parameters: self
            Returns: Pass if expected output is recieved, and fail otherwise.

        test_invalid_path_error: Tests whether an invalid path raises a ValueError exception.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

    Returns: A human readable string that provides a summary of results of the five tests
        conducted within this class.
    '''

    def test_cols_needed(self):
        """Tests that invalid input raises an IndexError"""
        bad_cols_needed = ["bad_category", "base_year", "c_severity", "c_type"]
        self.assertRaises(IndexError, int_func.generate_categories, bad_cols_needed,
                          data_directory=DATA_DIRECTORY)

    def test_output(self):
        '''Ensures function outputs the correct lists.'''
        cols_needed = ["b_category", "base_year", "c_severity", "c_type"]
        test_categories = int_func.generate_categories(cols_needed,
                                                       data_directory=DATA_DIRECTORY)
        true_output = (['All', 'COMMERCIAL', 'MULTIFAMILY', 'INDUSTRIAL', 'INSTITUTIONAL',
                        'SINGLE FAMILY / DUPLEX'], ['All', 2016, 2015, 2017, 2014, 2013],
                       ['All', 'Property Damage Only', 'Injury', 'Serious Injury', 'Fatality'],
                       ['All', 'Vehicle Only', 'Bike/Pedestrian'])
        self.assertTrue(test_categories == true_output)

    def test_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(ValueError, int_func.generate_categories, 'badPath')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGenerateCategories)
_ = unittest.TextTestRunner().run(SUITE)


class TestGenerateTable(unittest.TestCase):
    '''Conducts test on the performance of the generate_table function.

    This class tests the generate_table function. It conducts three tests, for
    the pupose of validating the functionality of the function. Each test is contained
    in a function as follows:

    Functions:
        test_col_names: Tests whether function assigns names to the table
            Parameters: self
            Returns: Pass if inputs are same as prescribed column names, and fail otherwise.

        test_data_frame_size: Ensures function returns output with at least 100 rows.
            Parameters: self
            Returns: Pass if table has at least 100 rows, and fail otherwise.

        test_zero_data_points: Tests that a query that eliminates all datapoints will
            return an empty pandas dataframe
            Parameters: self
            Returns: Pass if query with zero rows raises RuntimeError and fail otherwise.

        test_invalid_path_error: Tests whether an invalid path raises a ValueError exception.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

    Returns: A human readable string that provides a summary of results of the five tests
        conducted within this class.
    '''
    def test_col_names(self):
        '''Validates that the function assigns column names to the table.'''
        self.assertTrue(len(list(TEST_DF)) > 0)

    def test_data_frame_size(self):
        '''Ensures function returns output with at least 100 rows.'''
        self.assertTrue(TEST_DF.shape[0] > 100)

    def test_zero_data_points(self):
        '''Tests that a query that eliminates all datapoints will return an empty dataframe'''
        query = ("""SELECT b_id, b_lat, b_long, SUM(coll_before) AS before,
                 SUM(coll_during)*1.000000 AS during, SUM(coll_after) AS after
                 FROM collidium_data
                 WHERE radius < 1500 AND base_year = 2017 AND b_category = 'INDUSTRIAL'
                 AND c_severity = 'Fatality' AND c_type = 'Bike/Pedestrian'
                 GROUP BY b_id, b_lat, b_long""")

        empty_df = int_func.generate_table(query, data_directory=DATA_DIRECTORY)
        self.assertTrue(empty_df.empty)

    def test_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(Exception, int_func.generate_table, 'badPath')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGenerateTable)
_ = unittest.TextTestRunner().run(SUITE)


class TestInteractPath(unittest.TestCase):

    '''Conducts test on the performance of the *_interact functions.

    This class tests each of the *_interact functions in the interactions_functionality
    module to ensure that the each throw a ValueError if an invalid path to a database
    is there is a function to test the error for each of the *_interact functions.

    Functions:
        test_build_invalid_path_error: Tests whether an invalid path raises a ValueError exception
            in the build_type_interact function.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

        test_year_invalid_path_error: Tests whether an invalid path raises a ValueError exception in
            the year_int_interact function.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

        test_c_s_invalid_path_error: Tests whether an invalid path raises a ValueError exception in
            the collision_severity_interact function.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

        test_c_t_invalid_path_error: Tests whether an invalid path raises a ValueError exception in
            the collision_type_interact function.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

        test_radius_invalid_path_error: Tests whether an invalid path raises a ValueError exception
            radius_interact function.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

        test_a_f_invalid_path_error: Tests whether an invalid path raises a ValueError exception in
            the all_factor_interact function.
            Parameters: self
            Returns: Pass if invalid path raises a ValueError, and fail otherwise.

    Returns: A human readable string that provides a summary of results of the five tests
        conducted within this class.'''

    def test_build_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(ValueError, int_func.build_type_interact,
                          building_category="All",
                          data_directory='badPath')

    def test_year_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(ValueError, int_func.year_int_interact,
                          building_year=2015, collision_interval=12,
                          map_detail='High', data_directory='badPath')

    def test_c_s_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(ValueError, int_func.collision_severity_interact,
                          collision_severity="All", data_directory='badPath')

    def test_c_t_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(ValueError, int_func.collision_type_interact,
                          collision_type='All', data_directory='badPath')

    def test_radius_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(ValueError, int_func.radius_interact,
                          radius_from_building=1500, data_directory='badPath')

    def test_a_f_invalid_path_error(self):
        '''Tests whether an invalid path raises a ValueError exception.'''
        self.assertRaises(ValueError, int_func.all_factor_interact,
                          building_category='All', building_year=2016,
                          collision_interval=12, collision_severity='All',
                          collision_type='All', radius_from_building=1500,
                          data_directory='badPath')

SUITE = unittest.TestLoader().loadTestsFromTestCase(TestInteractPath)
_ = unittest.TextTestRunner().run(SUITE)


class TestInteractFunctions(unittest.TestCase):
    '''Conducts test on the performance of the *_interact functions.

    This class tests each of the *_interact functions in the interactions_functionality
    module to ensure that it can be executed without error when each of its steps does not
    result in an error.

    Functions:
        test_build_interact: Tests whether build_type_interact function can be executed without
            error.
            Parameters: self
            Returns: Pass if no error is raised, and fail otherwise.

        test_year_int_interact: Tests whether an invalid path raises a ValueError exceptionin the
            year_int_interact function.
            Parameters: self
            Returns: Pass if no error is raised, and fail otherwise.

        test_c_severity_interact: Tests whether an invalid path raises a ValueError exception in the
            collision_severity_interact function.
            Parameters: self
            Returns: Pass if no error is raised, and fail otherwise.

        test_collision_type_interact: Tests whether an invalid path raises a ValueError exception in
            the collision_type_interact function.
            Parameters: self
            Returns: Pass if no error is raised, and fail otherwise.

        test_radius_interact: Tests whether an invalid path raises a ValueError exception in the
            radius_interact function.
            Parameters: self
            Returns: Pass if no error is raised, and fail otherwise.

        test_a_f_interact: Tests whether an invalid path raises a ValueError exception in the
            all_factor_interact function.
            Parameters: self
            Returns: Pass if no error is raised, and fail otherwise.

    Returns: A human readable string that provides a summary of results of the five tests
        conducted within this class.'''

    def test_build_interact(self):
        """Tests whether build_type_interact function can be executed without error."""
        try:
            int_func.build_type_interact(building_category="All", data_directory=DATA_DIRECTORY)
        except RuntimeError:
            self.fail("build_type_interact raised ExceptionType unexpectedly.")

    def test_year_int_interact(self):
        """Tests whether year_int_interact function can be executed without error."""
        try:
            int_func.year_int_interact(building_year=2016,
                                       collision_interval=12, data_directory=DATA_DIRECTORY)
        except RuntimeError:
            self.fail("year_int_interact raised ExceptionType unexpectedly.")

    def test_c_severity_interact(self):
        """Tests whether collision_severity_interact function can be executed without error."""
        try:
            int_func.collision_severity_interact(collision_severity="All", map_detail='High',
                                                 data_directory=DATA_DIRECTORY)
        except RuntimeError:
            self.fail("collision_severity_interact raised ExceptionType unexpectedly.")

    def test_collision_type_interact(self):
        """Tests whether collision_type_interact function can be executed without error."""
        try:
            int_func.collision_type_interact(collision_type="All", data_directory=DATA_DIRECTORY)
        except RuntimeError:
            self.fail("collision_type_interact raised ExceptionType unexpectedly.")

    def test_radius_interact(self):
        """Tests whether radius_interact function can be executed without error."""
        try:
            int_func.radius_interact(radius_from_building=1500, data_directory=DATA_DIRECTORY)
        except RuntimeError:
            self.fail("radius_interact raised Exception unexpectedly.")

    def test_all_factor_interact(self):
        """Tests whether all_factor_interact function can be executed without error."""
        try:
            int_func.all_factor_interact(building_category='All', building_year=2016,
                                         collision_interval=12, collision_severity='All',
                                         collision_type='All', radius_from_building=1500,
                                         data_directory=DATA_DIRECTORY)
        except RuntimeError:
            self.fail("all_factor_interact raised ExceptionType unexpectedly.")

SUITE = unittest.TestLoader().loadTestsFromTestCase(TestInteractFunctions)
_ = unittest.TextTestRunner().run(SUITE)
