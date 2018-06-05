"""
COLLIDIUM
Query Class Test Module

This module is executed at each git push, as part of our continuous
integration design with Travis.

The test_query_class.py module uses the unittest package from Python to test the
functionality of the CollidiumQuery class module, comprised of the
CollidiumQuery object constructor, class methods set_* to set each attribute
(except for attribute qstring, which cannot be set directly by the user),
and static method __dynamic_substring__, which is a helper function for
attributes that allow dynamic (list or string) types.

Each attribute is tested for appropriate errors when bad input is provided
to the constructor:
 - test_bad_attr_constr_b_category_constr_b_category: tests bad constructor input for b_category
 - test_bad_attr_constr_radius: tests bad constructor input for radius
 - test_bad_attr_constr_base_year: tests bad constructor input for base_year
 - test_bad_attr_constr_duration: tests bad constructor input for duration
 - test_bad_attr_constr_c_severity: tests bad constructor input for c_severity
 - test_bad_attr_constr_c_type: tests bad constructor input for c_type

Each arg is test for appropriate errors when using a set_attribute class
method:
 - test_bad_arg_set_b_category: tests bad set_b_category() input
 - test_bad_arg_set_radius: tests bad set_radius() input
 - test_bad_arg_set_base_year: tests bad set_base_year() input
 - test_bad_arg_set_duration: tests bad set_duration() input
 - test_bad_arg_set_c_severity: tests bad set_c_severity() input
 - test_bad_arg_set_c_type: tests bad set_c_type() input

Examples are tested against expected query strings when appropriate input
is provided:
 - test_default_qstring: tests for expected default query string
 - test_constr_b_category_str: tests for expected query string output
   when valid b_category (as string) is set by constructor
 - test_constr_b_category_list: tests for expected query string output
   when valid b_category (as list) is set by constructor
 - test_constr_duration: tests for expected query string output
   when valid duration is set by constructor
 - test_set_b_category_str: tests for expected query string output
   when valid b_category (as string) is arg for set_b_category()
 - test_set_b_category_list: tests for expected query string output
   when valid b_category (as list) is arg for set_b_category()
 - test_set_duration: tests for expected query string output
   when valid duration is arg for set_duration()
"""
import sys
import unittest
sys.path.append('seattlecollision/')
#pylint: disable=import-error
#pylint: disable=wrong-import-position
import query_class as cq

class TestQueryClass(unittest.TestCase):
    """
    Using the unit test framework, CollidiumQuery object constructors
    and class methods are tested with various bad input, as well as
    checking the default query string and expected query string after
    attribute modification.
    """
    def test_bad_attr_constr_b_category(self):
        """
        Tests the object constructor with bad input for b_category.

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(AttributeError, cq.CollidiumQuery, b_category='bad input')
        self.assertRaises(AttributeError, cq.CollidiumQuery, b_category=['bad input'])

    def test_bad_arg_set_b_category(self):
        """
        Tests the class method set_b_category with bad input arg.

        Returns:
            True (bool) if the correct exception is raised.
        """
        tmp = cq.CollidiumQuery()
        self.assertRaises(ValueError, tmp.set_b_category, 'bad input')
        self.assertRaises(ValueError, tmp.set_b_category, ['bad input'])

    def test_bad_attr_constr_radius(self):
        """
        Tests the object constructor with bad input for radius.

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(AttributeError, cq.CollidiumQuery, radius='bad input')

    def test_bad_arg_set_radius(self):
        """
        Tests the class method set_radius with bad input arg.

        Returns:
            True (bool) if the correct exception is raised.
        """
        tmp = cq.CollidiumQuery()
        self.assertRaises(ValueError, tmp.set_radius, 'bad input')

    def test_bad_attr_constr_base_year(self):
        """
        Tests the object constructor with bad input for base_year.

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(AttributeError, cq.CollidiumQuery, base_year='bad input')

    def test_bad_arg_set_base_year(self):
        """
        Tests the class method set_base_year with bad input arg.

        Returns:
            True (bool) if the correct exception is raised.
        """
        tmp = cq.CollidiumQuery()
        self.assertRaises(ValueError, tmp.set_base_year, 'bad input')

    def test_bad_attr_constr_duration(self):
        """
        Tests the object constructor with bad input for duration.

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(AttributeError, cq.CollidiumQuery, duration='bad input')

    def test_bad_arg_set_duration(self):
        """
        Tests the class method set_duration with bad input arg.

        Returns:
            True (bool) if the correct exception is raised.
        """
        tmp = cq.CollidiumQuery()
        self.assertRaises(ValueError, tmp.set_duration, 'bad input')

    def test_bad_attr_constr_c_severity(self):
        """
        Tests the object constructor with bad input for c_severity.

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(AttributeError, cq.CollidiumQuery, c_severity='bad input')
        self.assertRaises(AttributeError, cq.CollidiumQuery, c_severity=['bad input'])

    def test_bad_arg_set_c_severity(self):
        """
        Tests the class method set_c_severity with bad input arg.

        Returns:
            True (bool) if the correct exception is raised.
        """
        tmp = cq.CollidiumQuery()
        self.assertRaises(ValueError, tmp.set_c_severity, 'bad input')
        self.assertRaises(ValueError, tmp.set_c_severity, ['bad input'])

    def test_bad_attr_constr_c_type(self):
        """
        Tests the object constructor with bad input for c_type.

        Returns:
            True (bool) if the correct exception is raised.
        """
        self.assertRaises(AttributeError, cq.CollidiumQuery, c_type='bad input')
        self.assertRaises(AttributeError, cq.CollidiumQuery, c_type=['bad input'])

    def test_bad_arg_set_c_type(self):
        """
        Tests the class method set_c_type with bad input arg.

        Returns:
            True (bool) if the correct exception is raised.
        """
        tmp = cq.CollidiumQuery()
        self.assertRaises(ValueError, tmp.set_c_type, 'bad input')
        self.assertRaises(ValueError, tmp.set_c_type, ['bad input'])

    def test_default_query(self):
        """
        Tests that the default query string matches expected value.

        Returns:
            True (bool) if the correct default query string is constructed.
        """
        tmp = cq.CollidiumQuery()
        self.assertTrue(tmp.get_qstring() == "SELECT b_id, b_lat, b_long, "+\
                        "SUM(coll_before) AS before, SUM(coll_during)*1.000000 " +\
                        "AS during, SUM(coll_after) AS after FROM collidium_data " +\
                        "WHERE radius < 1500 AND base_year = 2016 GROUP BY " +\
                        "b_id, b_lat, b_long")

    def test_constr_b_category_str(self):
        """
        Tests that the constructed query string matches expected value when
        b_category is set as a valid string.

        Returns:
            True (bool) if the correct default query string is constructed.
        """
        tmp = cq.CollidiumQuery(b_category='COMMERCIAL')
        self.assertTrue(tmp.get_qstring() == "SELECT b_id, b_lat, b_long, "+\
                        "SUM(coll_before) AS before, SUM(coll_during)*1.000000 " +\
                        "AS during, SUM(coll_after) AS after FROM collidium_data " +\
                        "WHERE radius < 1500 AND base_year = 2016 " +\
                        "AND b_category = 'COMMERCIAL' " +\
                        "GROUP BY b_id, b_lat, b_long")

    def test_constr_b_category_list(self):
        """
        Tests that the constructed query string matches expected value when
        b_category is set as a valid list.

        Returns:
            True (bool) if the correct default query string is constructed.
        """
        tmp = cq.CollidiumQuery(b_category=['COMMERCIAL', 'INDUSTRIAL'])
        self.assertTrue(tmp.get_qstring() == "SELECT b_id, b_lat, b_long, "+\
                        "SUM(coll_before) AS before, SUM(coll_during)*1.000000 " +\
                        "AS during, SUM(coll_after) AS after FROM collidium_data " +\
                        "WHERE radius < 1500 AND base_year = 2016 " +\
                        "AND b_category IN ('COMMERCIAL', 'INDUSTRIAL') " +\
                        "GROUP BY b_id, b_lat, b_long")

    def test_set_b_category_str(self):
        """
        Tests that the query string matches expected value when
        set_b_category method gets a valid string parameter.

        Returns:
            True (bool) if the correct query string is returned.
        """
        tmp = cq.CollidiumQuery()
        tmp.set_b_category('COMMERCIAL')
        self.assertTrue(tmp.get_qstring() == "SELECT b_id, b_lat, b_long, "+\
                        "SUM(coll_before) AS before, SUM(coll_during)*1.000000 " +\
                        "AS during, SUM(coll_after) AS after FROM collidium_data " +\
                        "WHERE radius < 1500 AND base_year = 2016 " +\
                        "AND b_category = 'COMMERCIAL' " +\
                        "GROUP BY b_id, b_lat, b_long")

    def test_set_b_category_list(self):
        """
        Tests that the query string matches expected value when
        set_b_category method gets a valid list parameter.

        Returns:
            True (bool) if the correct query string is returned.
        """
        tmp = cq.CollidiumQuery()
        tmp.set_b_category(['COMMERCIAL', 'INDUSTRIAL'])
        self.assertTrue(tmp.get_qstring() == "SELECT b_id, b_lat, b_long, "+\
                        "SUM(coll_before) AS before, SUM(coll_during)*1.000000 " +\
                        "AS during, SUM(coll_after) AS after FROM collidium_data " +\
                        "WHERE radius < 1500 AND base_year = 2016 " +\
                        "AND b_category IN ('COMMERCIAL', 'INDUSTRIAL') " +\
                        "GROUP BY b_id, b_lat, b_long")

    def test_constr_duration(self):
        """
        Tests that the constructed query string matches expected value when
        b_category is set as the string 'All'.

        Returns:
            True (bool) if the correct default query string is constructed.
        """
        tmp = cq.CollidiumQuery(duration=5)
        self.assertTrue(tmp.get_qstring() == "SELECT b_id, b_lat, b_long, "+\
                        "SUM(coll_before) AS before, SUM(coll_during)*0.416667 " +\
                        "AS during, SUM(coll_after) AS after FROM collidium_data " +\
                        "WHERE radius < 1500 AND base_year = 2016 " +\
                        "AND (coll_days_from_build BETWEEN 0 AND 152 OR " +\
                        "coll_days_from_build BETWEEN -152 AND -1) " +\
                        "GROUP BY b_id, b_lat, b_long")

    def test_set_duration(self):
        """
        Tests that the query string matches expected value when
        set_b_category method gets a valid list parameter.

        Returns:
            True (bool) if the correct query string is returned.
        """
        tmp = cq.CollidiumQuery()
        tmp.set_duration(5)
        self.assertTrue(tmp.get_qstring() == "SELECT b_id, b_lat, b_long, "+\
                        "SUM(coll_before) AS before, SUM(coll_during)*0.416667 " +\
                        "AS during, SUM(coll_after) AS after FROM collidium_data " +\
                        "WHERE radius < 1500 AND base_year = 2016 " +\
                        "AND (coll_days_from_build BETWEEN 0 AND 152 OR " +\
                        "coll_days_from_build BETWEEN -152 AND -1) " +\
                        "GROUP BY b_id, b_lat, b_long")

if __name__ == '__main__':
    unittest.main()
