"""
COLLIDIUM
Data Processing Test Module

This module is executed at each git push, as part of our continuous
integration design with Travis.

The test_process_data.py module uses the unittest package from Python to test the
functionality of the Collidium data processing module, comprsed of the
functions collision_clean, buildings_clean, and create_collidium_table.

Each function is tested for appropriate errors when bad input is provided:
 - test_buildings_file_path
 - test_collisions_file_path
 - test_collidium_inputs

Buildings and Collisions processed data should have unique keys for their
b_id and c_id columns, respectively. These fields are tested for duplicate
values:
 - test_buildings_index
 - test_collisions_index

Each processed DataFrame should be populated with rows. The following functions
check that there are at least 10 rows in each DataFrame:
 - test_buildings_rows
 - test_collisions_rows
 - test_collidium_rows
"""
import sys
import unittest
import pandas as pd
sys.path.append('seattlecollision/build_data_libraries/')
sys.path.append('seattlecollsion/data')
from process_data import collisions_clean
from process_data import buildings_clean
from process_data import create_collidium_table

class TestProcessData(unittest.TestCase):
    """
    This class includes unit tests that test the collision_clean fucntion in data_clean.py

    Using the unit test framework, the TestCollisionCleanclass tests whether
    the create_database function from the homework3 py module was created correctly.
    The functions in the class include:
    test_columnnames - tests whether the column names were generated correctly
    test_keys - tests whether language and video_id are a key
    test_rows - tests whether the dataset has more than 10 rows
    test_file_path - tests whether the file path is valid

    """
    def test_collisions_file_path(self):
        """
        This tests whether the correct ValueError exception is raised when an with
        an incorrect file path

        Args:

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(ValueError, collisions_clean, "not_a_file_path")

    def test_buildings_file_path(self):
        """
        This tests whether the correct ValueError exception is raised when an with
        an incorrect file path

        Args:

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(ValueError, buildings_clean, "not_a_file_path")

    def test_collidium_inputs(self):
        """
        This tests whether the correct ValueError exception and message is raised
        when buildings and collision inputs do not match specs

        Args:

        Returns:
            True (bool) if the correct exceptions are raised.
        """
        good_colls = collisions_clean("seattlecollision/data/raw_data/raw_collisions_input.csv")
        good_builds = buildings_clean("seattlecollision/data/raw_data/raw_buildings_input.csv")
        empty_pd = pd.DataFrame()
        bad_pd = pd.DataFrame([[1, 2, 3]])
        no_pd = [1, 2, 3]

        # Locally disable pylint warning
        # Note pylint bug to report assertRaisesRegex as deprecated-method:
        #     https://github.com/PyCQA/pylint/issues/1946
        # pylint: disable=deprecated-method
        self.assertRaisesRegex(ValueError, ".*buildings.*empty rows.*",
                               create_collidium_table, good_colls, empty_pd)
        self.assertRaisesRegex(ValueError, ".*buildings.*extra or missing.*",
                               create_collidium_table, good_colls, bad_pd)
        self.assertRaisesRegex(ValueError, ".*buildings.*pandas.*",
                               create_collidium_table, good_colls, no_pd)
        self.assertRaisesRegex(ValueError, ".*collisions.*empty rows.*",
                               create_collidium_table, empty_pd, good_builds)
        self.assertRaisesRegex(ValueError, ".*collisions.*extra or missing.*",
                               create_collidium_table, bad_pd, good_builds)
        self.assertRaisesRegex(ValueError, ".*collisions.*pandas.*",
                               create_collidium_table, no_pd, good_builds)

    def test_collisions_index(self):
        """
        This tests whether c_id is a key in the Collisions database

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_collision_output = collisions_clean(
            "seattlecollision/data/raw_data/raw_collisions_input.csv")
        processed_collision_output_dup = processed_collision_output.drop_duplicates(["c_id"])
        self.assertTrue(
            processed_collision_output.shape[0] == processed_collision_output_dup.shape[0])

    def test_buildings_index(self):
        """
        This tests whether b_id is a key in the Buildings database

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_buildings_output = buildings_clean(
            "seattlecollision/data/raw_data/raw_buildings_input.csv")
        processed_buildings_output_dup = processed_buildings_output.drop_duplicates(["b_id"])
        self.assertTrue(
            processed_buildings_output.shape[0] == processed_buildings_output_dup.shape[0])

    def test_collisions_rows(self):
        """
        This tests whether there are greater than 10 rows in the dataframe

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_collision_output = collisions_clean(
            "seattlecollision/data/raw_data/raw_collisions_input.csv")
        self.assertTrue(processed_collision_output.shape[0] >= 10)

    def test_buildings_rows(self):
        """
        This tests whether there are greater than 10 rows in the dataframe

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_buildings_output = buildings_clean(
            "seattlecollision/data/raw_data/raw_buildings_input.csv")
        self.assertTrue(processed_buildings_output.shape[0] >= 10)

    def test_collidium_rows(self):
        """
        This tests whether there are greater than 10 rows in the dataframe

        Note: This test will fail if the first building row does not have 10 collisions
        within 1500 feet and 1 year of construction.

        Only the first row of building data is used to limit computation time.

        Args:

        Returns:
            True (bool) if the condition is true
        """
        good_colls = collisions_clean("seattlecollision/data/raw_data/raw_collisions_input.csv")
        good_builds_1 = buildings_clean(
            "seattlecollision/data/raw_data/raw_buildings_input.csv").head(1)
        processed_collidium_output = create_collidium_table(good_colls, good_builds_1)
        self.assertTrue(processed_collidium_output.shape[0] >= 10)

if __name__ == '__main__':
    unittest.main()
