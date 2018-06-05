'''Tests draw_markers.py module to ensure it executes as expected.

This module contains one class, UnitTests which conducts 3 unit tests. These tests evaluate
whether the functions create_map and place_maps from draw_markers.py perform as expected.

Classes:
    UnitTests: A class created to conduct unit tests on the functions from the draw_markers.py
        module. The test ensures that an IndexError is raised if the input data doesn't contain the
        correct fields. It also checks that a TypeError is thrown if too many observations are
        included in the input data. Finally, it throws a TypeError if the b_id is not a key of the
        data. The class returns a human readable string summarizing the results of the unit tests.

Functions: The five functions are each contained in the UnitTests class

    test_col_names: assesses whether incorrect column names result in an IndexError

    test_data_frame_size: assesses whether a data frame that is larger than 800 rows
        raises TypeError.

    test_b_id_is_key: assesses whether b_id a key to input.

Exceptions:
    AssertionError: If a test fails the class will raise an assertion error, and describe
        which test failed

Attributes:
    TEST_DATA: This is sample input data that is used to test how whether the correct exceptions
    are raised.
'''
import sys
import unittest
import pandas as pd
sys.path.append('seattlecollision/')
sys.path.append('seattlecollision/data')
#pylint: disable=import-error
#pylint: disable=wrong-import-position
import draw_markers as dm


with open('seattlecollision/data/Test_Data_For_Draw_Markers.csv',
          encoding='ascii', errors='ignore') as csvfile:
    TEST_DATA = pd.read_csv(csvfile)

class UnitTests(unittest.TestCase):
    '''Conducts test on the performance of the create_dataframe function.

    This class conducts five tests, for the pupose of validating the functionality
    of the create_map and place_maps functions. Each test is conducted within a function, as
    follows:

    Functions:
        test_col_names: assesses whether incorrect column names raises an IndexError.

        test_data_frame_size: assesses whether a dataframe that is too big raises a ValueError.

        test_b_id_key: assesses whether building ID is key to the dataframe

    Returns: A human readable string that provides a summary of results of the three tests
        conducted within this class.
    '''

    def test_col_names(self):
        '''Tests whether function raises IndexError if column names are incorrect.'''
        self.assertRaises(IndexError, dm.create_map, TEST_DATA.iloc[:, [0, 4]], "before")

    def test_data_frame_size(self):
        '''Tests whether a TypeError is raised if more than 800 rows are in data.'''
        self.assertRaises(TypeError, dm.create_map, TEST_DATA.head(801), "before")

    def test_b_id_is_key(self):
        ''' Tests if b_id is a key to function input.'''
        total_unique = len(TEST_DATA['b_id'].drop_duplicates())
        key_unique = len(TEST_DATA.drop_duplicates())
        self.assertTrue(total_unique == key_unique)

SUITE = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
_ = unittest.TextTestRunner().run(SUITE)
