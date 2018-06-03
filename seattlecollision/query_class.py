"""
COLLIDIUM
Class Module to build CollidiumQuery Object

The CollidiumQuery is an object that takes each of our interactive
use case values as attributes, and builds/retrieves a sqlite query
from those attributes when the get_qstring object method is called.

See class docstrings below for further details on the attributes and
methods.

An instance of this object is created in each of the *_interact functions
in the interactions_functionality module. All instances are initially
created with default attributes, and modified as the interact widgets
request new values. The qstring attribute is then calculated and returned,
with the new data results table sent to the draw_markers function (in the
draw_markers module).
"""
class CollidiumQuery(object):
    """
    Collidium Query Object Class

    A CollidiumQuery object has an attribute to reflect each of our use
    cases, as well as an attribute containing the sqlite query string
    reflecting the values of all other attributes.

    An instance of this object is created in each of the *_interact functions
    in the interactions_functionality module. All instances are initially
    created with default attributes, and modified as the interact widgets
    request new values. The qstring attribute is then calculated and returned,
    with the new data results table sent to the draw_markers function (in the
    draw_markers module).

    Raises AttributeError:
        All attributes have initial default values. Validity checks are
        performed to the specs listed below for each attribute upon
        calling the constructor or any set_* functions.

    Attributes:
      b_category:
        - Description: Building category
        - Default Value: 'All'
        - Valid Types: list or single list element as string
        - Valid Values: ['All', 'COMMERCIAL', 'MULTIFAMILY',
                   'INDUSTRIAL', 'INSTITUTIONAL', 'SINGLE FAMILY / DUPLEX']
      radius:
        - Description: Distance between building and collision in feet
        - Default Value: 1500
        - Valid Types: int
        - Valid Values: (0, 1500]
      base_year:
        - Description: Year of building completion date
        - Default Value: 2016
        - Valid Types: int
        - Valid Values: 2014-2017 (inclusive)
      duration:
        - Description: Months to count collisions before and after construction
        - Default Value: 12
        - Valid Types: int or float
        - Valid Values: (0, 12]
      c_severity:
        - Description: Accident severity
        - Default Value: 'All'
        - Valid Types: list or single list element as string
        - Valid Values: ['All', 'Fatality', 'Serious Injury', 'Injury',
                         'Property Damage Only']
      c_type:
        - Description: Accident type
        - Default Value: 'All'
        - Valid Types: list or single list element as string
        - Valid Values: ['All', 'Vehicle Only', 'Bike/Pedestrian']
      qstring (no constructor arg, NOTE: user does not ever set):
        - Description: Sqlite query string for Collidium database
        - Default Value (set by get_qstring function):
          'SELECT b_id, b_lat, b_long, SUM(coll_before) AS before, ' +\
          'SUM(coll_during)*1.000000 AS during, SUM(coll_after) AS ' +\
          'after FROM collidium_data WHERE radius< 1500 AND ' +\
          'base_year = 2017 GROUP BY b_id, b_lat, b_long'

    Class Methods:
        - set_* methods allow setting an individual attribute for abs
              CollidiumQuery object. Raises AttributeError if new value
              does not meet requirements.
        - get_qstring method constructs a sqlite query string from
              current attributes. The query string is set as an attribute
              and returned by the method.

    Static Methods:
        - __dynamic_substring__ method is a helper function to allow
              multiple entries for each attribute that accepts lists or
              strings (c_severity, c_type, and b_category). Performs a
              validity check and throws AttributeError if args are invalid.
    """
    # Locally disable linter to allow for reasonable object construction:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(self, b_category='All', radius=1500, base_year=2016,
                 duration=12, c_severity='All', c_type='All'):
        """
        Constructor method for CollidiumQuery object.

        Sets all attributes to default or specified values.

        Raises AttributeError if invalid arguments are provided.

        Note that there is a qstring attribute that cannot be set by
        the user in this constructor or any class method. The qstring
        attribute is set only by calling the get_qstring method, which
        is executed by this constructor.

        Attributes/Args:
          b_category:
            - Description: Building category
            - Default Value: 'All'
            - Valid Types: list or single list element as string
            - Valid Values: ['All', 'COMMERCIAL', 'MULTIFAMILY',
                       'INDUSTRIAL', 'INSTITUTIONAL', 'SINGLE FAMILY / DUPLEX']
          radius:
            - Description: Distance between building and collision in feet
            - Default Value: 1500
            - Valid Types: int
            - Valid Values: (0, 1500]
          base_year:
            - Description: Year of building completion date
            - Default Value: 2016
            - Valid Types: int
            - Valid Values: 2014-2017 (inclusive)
          duration:
            - Description: Months to count collisions before and after construction
            - Default Value: 12
            - Valid Types: int
            - Valid Values: (0, 12]
          c_severity:
            - Description: Accident severity
            - Default Value: 'All'
            - Valid Types: list or single list element as string
            - Valid Values: ['All', 'Fatality', 'Serious Injury', 'Injury',
                             'Property Damage Only']
          c_type:
            - Description: Accident type
            - Default Value: 'All'
            - Valid Types: list or single list element as string
            - Valid Values: ['All', 'Vehicle Only', 'Bike/Pedestrian']
          qstring (no arg, NOTE: user does not ever set):
            - Description: Sqlite query string for Collidium database
            - Default Value (set by get_qstring function):
              'SELECT b_id, b_lat, b_long, SUM(coll_before) AS before, ' +\
              'SUM(coll_during)*1.000000 AS during, SUM(coll_after) AS ' +\
              'after FROM collidium_data WHERE radius < 1500 AND ' +\
              'base_year = 2016 GROUP BY b_id, b_lat, b_long'
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
        Static method to create substring for variables with dynamic
        valid types (e.g.: b_category, c_severity, and c_type). Each
        of those args can be a list or string. This method builds an
        appropriate query substring based on the arg type. If the arg
        is 'All', then a blank query substring is returned.

        Args:
          - label: the attribute name we are constructing a substring for
          - arg: the value of the attribute
          - valid_args: the list of valid args for the attribute

        Returns:
          query substring depending on the value of arg:
            - blank if arg == 'All'
            - 'AND (label) = (arg)' if arg is a string
            - 'AND (label) IN (tuple(arg))' if arg is list

        Raises:
          AttributeError if invalid arg is provided
        """
        if isinstance(arg, list):
            if not all([x in valid_args for x in arg]):
                raise AttributeError("%s list contains invalid values." % label)
            return "AND %s IN %s " % (label, tuple(arg).__str__())
        elif arg == "All":
            return ''
        elif arg in valid_args:
            return "AND %s = '%s' " % (label, arg)
        else:
            raise AttributeError("Attribute %s is invalid." % label)

    def get_qstring(self):
        """
        Class method builds sqlite query string from currently set
        attributes.

        Raises:
          - AttributeError if any directly referenced attributes are
            invalid. Helper function covers remaining attributes so
            all are checked when running this method.

        Sets attribute:
          - self.qstring is set after calculating the query string

        Returns:
          - self.qstring is returned after calculating the query string
            from current attributes
        """
        # Check validity of directly referenced attributes
        if not (isinstance(self.radius, int) and self.radius <= 1500 and self.radius > 0):
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
            qstring += "%d OR coll_days_from_build BETWEEN %d AND -1) " %(
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
        Sets c_severity attribute.

        Args:
            c_severity:
              - Description: Accident severity
              - Valid Types: list or single list element as string
              - Valid Values: ['All', 'Fatality', 'Serious Injury',
                               'Injury', 'Property Damage Only']

        Raises:
            ValueError if c_severity is not a valid type or value.
        """
        # Use __dynamic_substring__ method to check validity
        try:
            self.__dynamic_substring__('c_severity', c_severity, self.__valid_c_severity)
            self.c_severity = c_severity
        except AttributeError as attr_err:
            raise ValueError(str(attr_err))

    def set_c_type(self, c_type):
        """
        Sets c_type attribute.

        Args:
            c_type:
              - Description: Accident type
              - Valid Types: list or single list element as string
              - Valid Values: ['All', 'Vehicle Only', 'Bike/Pedestrian']

        Raises:
            ValueError if c_type is not a valid type or value.
        """
        # Use __dynamic_substring__ method to check validity
        try:
            self.__dynamic_substring__('c_type', c_type, self.__valid_c_type)
            self.c_type = c_type
        except AttributeError as attr_err:
            raise ValueError(str(attr_err))

    def set_b_category(self, b_category):
        """
        Sets b_category attribute.

        Args:
            b_category:
              - Description: Building Permit Category
              - Valid Types: list or single list element as string
              - Valid Values: ['All', 'COMMERCIAL', 'MULTIFAMILY',
                'INDUSTRIAL', 'INSTITUTIONAL', 'SINGLE FAMILY / DUPLEX']

        Raises:
            ValueError if b_category is not a valid type or value.
        """
        # Use __dynamic_substring__ method to check validity
        try:
            self.__dynamic_substring__('b_category', b_category, self.__valid_b_category)
            self.b_category = b_category
        except AttributeError as attr_err:
            raise ValueError(str(attr_err))

    def set_radius(self, radius):
        """
        Sets radius attribute.

        Args:
            radius:
              - Description: Distance between building and collision in feet
              - Valid Types: int
              - Valid Values: (0, 1500]

        Raises:
            ValueError if radius is not a valid type or value.
        """
        if not (isinstance(radius, int) and radius <= 1500 and radius > 0):
            raise ValueError("Arg radius should be a positive integer <= 1500.")
        self.radius = radius

    def set_duration(self, duration):
        """
        Sets duration attribute.

        Args:
            duration:
              - Description: Months to count collisions before and after construction
              - Valid Types: int
              - Valid Values: (0, 12]

        Raises:
            ValueError if duration is not a valid type or value.
        """
        if not (isinstance(duration, int) and duration <= 12 and duration > 0):
            raise ValueError("Arg duration (in months) should be a positive int <= 12.")
        self.duration = duration

    def set_base_year(self, base_year):
        """
        Sets base_year attribute.

        Args:
            base_year:
              - Description: Year of building completion date
              - Valid Types: int
              - Valid Values: 2014-2017 (inclusive)

        Raises:
            ValueError if base_year is not a valid type or value.
        """
        if not (isinstance(base_year, int) and base_year in (2014, 2015, 2016, 2017)):
            raise ValueError("Arg base_year should be an integer between 2014-2017.")
        self.base_year = base_year
