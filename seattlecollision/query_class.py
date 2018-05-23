"""
Class Docstring

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
>>> cq.set_acc_type('Vehicle Only') # Can be string or list
>>> cq.set_b_category(['MULTIFAMILY', 'SINGLE FAMILY / DUPLEX']) # List example
>>> cq.get_qstring()
"SELECT b_id, b_lat, b_long, SUM(coll_before) AS before, SUM(coll_duri
ng)*0.416667 AS during, SUM(coll_after) AS after FROM collidium_data W
HERE radius < 500 AND base_year = 2017 AND (coll_days_from_build BETWE
EN 0 AND 150 OR coll_days_from_build BETWEEN -1 AND -150) AND b_catego
ry IN ('MULTIFAMILY', 'SINGLE FAMILY / DUPLEX') AND acc_type = 'Vehicle
 Only' GROUP BY b_id, b_lat, b_long"

"""
class CollidiumQuery(object):

	def __init__(self, b_category='All', radius=1500, base_year=2017,
				duration=12, acc_severity='All', acc_type='All'):
		"""
		"""
		self.__valid_acc_severity = ['Fatality', 'Serious Injury', 'Injury', 'Property Damage']
		self.__valid_acc_type = ['Vehicle Only', 'Bike/Ped']
		self.__valid_b_category = ['All','COMMERCIAL','MULTIFAMILY', 'INDUSTRIAL','INSTITUTIONAL','SINGLE FAMILY / DUPLEX']
		
		self.b_category = b_category
		self.radius = radius
		self.base_year = base_year
		self.duration = duration
		self.acc_severity = acc_severity
		self.acc_type = acc_type
		self.get_qstring()
		
	def __dynamic_substring__(self, label, arg, valid_args):
		"""
		"""
		if type(arg) == list:
			return "AND %s IN %s " % (label, tuple(arg).__str__())
		elif arg == "All":
			return ''
		elif arg in valid_args:
			return "AND %s = '%s' " % (label, arg)
		else:
			raise AttributeError("Attribute %s is invalid." % label)
		
	def get_qstring(self):
		"""
		"""
		# Check validity of directly referenced attributes
		if not (type(self.radius) == int and self.radius <= 1500):
			raise AttributeError("Attribute radius should be an integer <= 1500.")
		if not (type(self.duration) == int and self.duration <= 12 and self.duration > 0):
			raise AttributeError("Attribute duration (in months) should be a positive integer <= 12.")
		if not (type(self.base_year) == int and self.base_year in (2014, 2015, 2016, 2017)):
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
						30*self.duration, -30*self.duration)
		
		# Dynamic string constructor checks other attributes
		qstring += self.__dynamic_substring__('b_category', self.b_category, self.__valid_b_category)
		qstring += self.__dynamic_substring__('acc_severity', self.acc_severity, self.__valid_acc_severity)
		qstring += self.__dynamic_substring__('acc_type', self.acc_type, self.__valid_acc_type)
		
		# Complete the query string
		qstring += "GROUP BY b_id, b_lat, b_long"
		self.qstring = qstring
		return qstring
		
	def set_acc_severity(self, acc_severity):
		"""
		"""
		self.acc_severity = acc_severity
	
	def set_acc_type(self, acc_type):
		"""
		"""
		self.acc_type = acc_type
	
	def set_b_category(self, b_category):
		"""
		"""
		self.b_category = b_category
	
	def set_radius(self, radius):
		"""
		"""
		self.radius = radius
	
	def set_duration(self, duration):
		"""
		"""
		self.duration = duration
	
	def set_base_year(self, base_year):
		"""
		"""
		self.base_year = base_year
		
	
		
		
		