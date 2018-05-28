"""

TODO: Add unit tests and docstrings throughout

EXAMPLES (Command-line):
Import Object Class:
>>> from query_class import CollidiumQuery
>>> cq = CollidiumQuery() #default attributes
>>> cq.get_qstring()
'SELECT b_id, b_lat, b_long, SUM(coll_before) AS before, SUM(coll_duri
ng)*1.000000 AS during, SUM(coll_after) AS after FROM collidium_data W
HERE radius < 1500 AND base_year = 2017 GROUP BY b_id, b_lat, b_long'

Functions to Set Attributes:
>>> cq.set_duration(5) # duration is in months
>>> cq.get_qstring()
'SELECT b_id, b_lat, b_long, SUM(coll_before) AS before, SUM(coll_duri
ng)*0.416667 AS during, SUM(coll_after) AS after FROM collidium_data W
HERE radius < 1500 AND base_year = 2017 AND (coll_days_from_build BETW
EEN 0 AND 150 OR coll_days_from_build BETWEEN -1 AND -150) GROUP BY b_
id, b_lat, b_long'

>>> cq.set_radius(500)
>>> cq.set_c_type('Vehicle Only') # Can be string or list
>>> cq.set_b_category(['MULTIFAMILY', 'SINGLE FAMILY / DUPLEX']) # List example
>>> cq.get_qstring()
"SELECT b_id, b_lat, b_long, SUM(coll_before) AS before, SUM(coll_duri
ng)*0.416667 AS during, SUM(coll_after) AS after FROM collidium_data W
HERE radius < 500 AND base_year = 2017 AND (coll_days_from_build BETWE
EN 0 AND 150 OR coll_days_from_build BETWEEN -1 AND -150) AND b_catego
ry IN ('MULTIFAMILY', 'SINGLE FAMILY / DUPLEX') AND c_type = 'Vehicle
 Only' GROUP BY b_id, b_lat, b_long"

"""
class CollidiumQuery(object):
    """
    Class docstring actually goes here. TODO
    """
	# Locally disable linter to allow for reasonable object construction:
	# pylint: disable=too-many-instance-attributes
	# pylint: disable=too-many-arguments

    def __init__(self, b_category='All', radius=1500, base_year=2017,
                 duration=12, c_severity='All', c_type='All'):
        """
		Add stuff here TODO
        """
        self.__valid_c_severity = ['All', 'Fatality', 'Serious Injury', 'Injury',
		                                 'Property Damage Only']
        self.__valid_c_type = ['All', 'Vehicle Only', 'Bike/Pedestrian']
        self.__valid_b_category = ['All', 'COMMERCIAL', 'MULTIFAMILY', 'INDUSTRIAL',
		                                 'INSTITUTIONAL', 'SINGLE FAMILY / DUPLEX']

        self.b_category = b_category
        self.radius = radius
        self.base_year = base_year
        self.duration = duration
        self.c_severity = c_severity
        self.c_type = c_type
        self.get_qstring()

    @staticmethod
    def __dynamic_substring__(label, arg, valid_args):
        """
		LALALAALA TODO
        """
        if isinstance(arg, list):
            return "AND %s IN %s " % (label, tuple(arg).__str__())
        elif arg == "All":
            return ''
        elif arg in valid_args:
            return "AND %s = '%s' " % (label, arg)
        else:
            raise AttributeError("Attribute %s is invalid." % label)

    def get_qstring(self):
        """
		TODO TODO TODO
        """
        # Check validity of directly referenced attributes
        if not (isinstance(self.radius, int) and self.radius <= 1500):
            raise AttributeError("Attribute radius should be an integer <= 1500.")
        if not (isinstance(self.duration, int) and self.duration <= 12 and self.duration > 0):
            raise AttributeError("Attribute duration (in months) should be a positive int <= 12.")
        if not (isinstance(self.base_year, int) and self.base_year in (2014, 2015, 2016, 2017)):
            raise AttributeError("Attribute base_year should be an integer between 2014-2017.")

        # Build query string from attributes
        qstring = "SELECT b_id, b_lat, b_long, "
        qstring += "SUM(coll_before) AS before, "
        qstring += "SUM(coll_during)*%f AS during, " % (self.duration/12)
        qstring += "SUM(coll_after) AS after "
        qstring += "FROM collidium_data "
        qstring += "WHERE radius < %d " % self.radius
        qstring += "AND base_year = %d " % self.base_year
        if self.duration != 12:
            qstring += "AND (coll_days_from_build BETWEEN 0 AND "
            qstring += "%d OR coll_days_from_build BETWEEN -1 AND %d) " %(
                30.4167*self.duration, -30.4167*self.duration)

        # Dynamic string constructor checks other attributes
        qstring += self.__dynamic_substring__('b_category', self.b_category,
		                                            self.__valid_b_category)
        qstring += self.__dynamic_substring__('c_severity', self.c_severity,
		                                            self.__valid_c_severity)
        qstring += self.__dynamic_substring__('c_type', self.c_type, self.__valid_c_type)

        # Complete the query string
        qstring += "GROUP BY b_id, b_lat, b_long"
        self.qstring = qstring
        return qstring

    def set_c_severity(self, c_severity):
        """
		guys TODO
        """
        self.c_severity = c_severity

    def set_c_type(self, c_type):
        """
		and more TODO
        """
        self.c_type = c_type

    def set_b_category(self, b_category):
        """
		so glad TODO doesn't trigger pylint
        """
        self.b_category = b_category

    def set_radius(self, radius):
        """
		and more docstrings TODO
        """
        self.radius = radius

    def set_duration(self, duration):
        """
		TODO DO DO
        """
        self.duration = duration

    def set_base_year(self, base_year):
        """
		MUCH TODO ABOUT NOTHING
        """
        self.base_year = base_year
