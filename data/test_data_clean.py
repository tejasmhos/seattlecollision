"""

The test_data_clean.py module uses the unittest package from Python to test the
functionality of collision_clean and  function within homework3.py.
This includes the TestCreateDatabase class which includes the test_columnnames, test_keys
test_rows, and test_file path.

"""


import unittest
from data_clean import collision_clean
from data_clean import buildings_clean

class TestDataClean(unittest.TestCase):
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
    def test_collision_file_path(self):
        """
        This tests whether the correct ValueError exception is raised when an with an incorrect file path

        Args:

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(ValueError, collision_clean, "not_a_file_path")

    def test_buildings_file_path(self):
        """
        This tests whether the correct ValueError exception is raised when an with an incorrect file path

        Args:

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(ValueError, buildings_clean, "not_a_file_path")


    def test_collisions_index(self):
        """
        This tests whether c_id is a key in the Collisions database

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_collision_output = collision_clean("Collisions.csv")
        processed_collision_output_dup =  processed_collision_output.drop_duplicates(["c_id"])
        self.assertTrue(processed_collision_output.shape[0] ==  processed_collision_output_dup.shape[0])

    def test_buildings_index(self):
        """
        This tests whether b_id is a key in the Buildings database

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_buildings_output = buildings_clean("clean_permits.csv")
        processed_buildings_output_dup =  processed_buildings_output.drop_duplicates(["b_id"])
        self.assertTrue(processed_buildings_output.shape[0] ==  processed_buildings_output_dup.shape[0])
    

    def test_collision_rows(self):
        """
        This tests whether there are greater than 10 rows in the dataframe

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_collision_output = collision_clean("Collisions.csv")
        self.assertTrue(processed_collision_output.shape[0] >= 10)

    def test_buildings_rows(self):
        """
        This tests whether there are greater than 10 rows in the dataframe

        Args:

        Returns:
            True (bool) if the condition is true
        """
        processed_buildings_output = buildings_clean("clean_permits.csv")
        self.assertTrue(processed_buildings_output.shape[0] >= 10)

if __name__ == '__main__':
    unittest.main()