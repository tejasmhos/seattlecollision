"""
Develops functions that plots maps based on user inputs

Module summary:
    This module includes six "*_interact" functions that take user parameters and plot
    three maps showing where new buildings are constructed, as well as how many traffic
    collisions occured before, during, and after that building's construction. The
    before, during and after cases are constructed on three separate maps. In addition
    to the "*_interact" functions which output maps, there are three supporting functions
    that output intermediate steps used in processing data to plot the maps. The "*_interact"
    functions are designed to be implemented in a Jupyter Notebook environment using
    ipywidges interact fucntionality.

Functions:
    generate_connection: This function generates a connection to a sqlite3 database, and
        returns a cursor object that can be used to query the database. It is used
        within each of the other functions in this module.

    generate_categories: This function queries the database and generates a list of all
        the categories that a user can select from when developing thier query. The
        function takes and input of the data_directory, which is the location of the
        datebase, as well as the cols_needed, which are a list of four columns for which
        the user desires a list of options to select from. The function returns four
        lists, one for each column in the "cols_needed input."

    generate_table: This function takes input of a database directory and a query. It
        then querys the database, using the query string input and creates a pandas
        dataframe out of the query output. The function also creates field names for
        the pandas dataframe based on the field names of the query output.

    build_type_interact: takes input of building type and data_directory. It then
        filters queries the database in the data_directory and uses that data to create
        output of three map objects that show building locations that fit the filter
        critera, and plots the number of collisions that occured before, during and after
        the building was constructed. This function is intended to be run in a Jupyter
        Notebook environment.

    year_int_interact: takes input of building_year (the year a building was completed)
        collision_interval (# of months before and after building was constructed for which
        you want to count collisions) and data_directory (a location of a database). It then
        queries the database in the data_directory and uses that data to create
        output of three map objects that show building locations that fit the filter
        critera, and plots the number of collisions that occured before, during and after
        the building was constructed. This function is intended to be run in a Jupyter
        Notebook environment.

    collision_severity_interact: takes input of collision_severity (the severity of
        impact of a collision, e.g., injury, fatality, property damage) and data_directory.
        It then queries the database in the data_directory and uses that data to create
        output of three map objects that show building locations that fit the filter
        critera, and plots the number of collisions that occured before, during and after
        the building was constructed. This function is intended to be run in a Jupyter
        Notebook environment.

    collision_type_interact: Takes input of collision_type (e.g., vehicle only or bike/
        pedestrian involved) and data_directory (location of a database.
        It then queries the database in the data_directory and uses that data to create
        output of three map objects that show building locations that fit the filter
        critera, and plots the number of collisions that occured before, during and after
        the building was constructed. This function is intended to be run in a Jupyter
        Notebook environment.

    radius_interact: Takes input of radius from building, which lets the user define how
        far away from the building they desire to count collisions. The second user input
        is data_directory (location of a database to be queried). The function then queries
        the database based on the radius filter and uses that data to create
        output of three map objects that show building locations that fit the filter
        critera, and plots the number of collisions that occured before, during and after
        the building was constructed. This function is intended to be run in a Jupyter
        Notebook environment.


    all_factor_interact: Takes user input on all potential factors listed above and uses
        The those inputs as query filters. The user also defines database location. The
        function then queries the database based on the user defined filters and uses
        that data to create output of three map objects that show building locations that
        fit the filter critera, and plots the number of collisions that occured before,
        during and after the building was constructed. This function is intended to be
        run in a Jupyter Notebook environment


Exceptions:
    RuntimeError: Raised if the user selects criteria that result in a query that retunrs
        no results

    ValueError: Raised if a user enters an invalid data directory as input

    IndexError: Raised if user enters invalid columns in the generate_categories function

"""
import sqlite3
import os
import pandas as pd
import draw_markers
from query_class import CollidiumQuery

def generate_connection(data_directory):
    """
    This function generates a sqlite3 connection with a database

    Args:
        data_directory(str): Input with path to database location

    Returns:
        sql_cursor(cursor object): A sqlite cursor object that allows
        queries to an SQL database

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    connection = sqlite3.connect(data_directory)
    sql_cursor = connection.cursor()
    return sql_cursor



def generate_categories(cols_needed, data_directory="data/Collidium"):
    """
    This function generates lists of unique entries in each of four categories.

    These lists are later used to populate the
    dropdown menu in the map interaction in the Jupyter Notebook.

    Args:
    cols_needed(list): List of four entries including ('b_category', 'base_year',
        'c_severity', 'c_type'), where b_category is building category (e.g.,
        multifamily, commercial), base_year is the year construction was completed
        c_severity is collision severity (e.g., fatality, injury) and c_type is
        collision type (e.g., vehicle only or bike/pedestrian).

        data_directory(str): Input with path to database location

    Returns: Four lists, one for each cols_needed entry

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.

        IndexError: If cols_needed input does not contain the list with the items
            ['b_category', 'base_year', 'c_severity', 'c_type'].

    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    true_set = set(['b_category', 'base_year', 'c_severity', 'c_type'])
    if not set(list(cols_needed)) == true_set:
        raise IndexError("cols_needed must only contain the fields:", true_set)
    categories = list()
    i = 0
    for col in cols_needed:
        query_string = str("select distinct " + col + " from collidium_data")
        sql_cursor = generate_connection(data_directory)
        sql_cursor.execute(query_string)
        temp = pd.DataFrame(sql_cursor.fetchall())
        temp = temp.values.tolist()
        temp = [val for sublist in temp for val in sublist]
        temp.insert(0, 'All')
        categories.append(temp)
        i += 1
    return categories[0], categories[1], categories[2], categories[3]

def generate_table(query, data_directory="data/Collidium"):
    """
    Generates a pandas dataframe from the output of a query on a database.

    Args:
    query(str): String written as a query for SQLite3, to query the data
        table called collidium_data, located in the data_directory

    data_directory(str): Input with path to database location

    Returns: A pandas dataframe with the output of the query, incuding
        field names. If the query had no results and empty dataframe is
        returned.

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.

    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    sql_cursor = generate_connection(data_directory)
    sql_cursor.execute(query)
    temp = pd.DataFrame(sql_cursor.fetchall())
    if temp.size == 0:
        temp = pd.DataFrame({'A' : []})
    else:
        temp.columns = list(map(lambda x: x[0], sql_cursor.description))
    return temp

def build_type_interact(building_category, data_directory="data/Collidium"):
    """
    Queries database and returns maps based on data filtered by building type.

    Args:
    building_category(st): String indicating which type of building user would
        like to see location and collision data plotted. Options include (MULTIFAMILY,
        COMMERCIAL, INDUSTRIAL, INSTITUTIONAL SINGLE FAMILY/DUPLEX, ALL)

    data_directory(str): Input with path to database location

    Returns: Three maps showing building locations and number of collisions corresponding
        to each location before, during and after building construction

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_b_category(building_category)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def year_int_interact(building_year, collision_interval, data_directory="data/Collidium"):
    """
    Queries database and returns maps based on data filtered by construction and colision timing.

    Args:
    building_year(int): Year building construction was completed. Can take values 2014-2017.

    collision_interval(int): Number of months before and after construction period user
        wishes to count collisions. Can take values 6-12.

    data_directory(str): Input with path to database location

    Returns: Three maps showing building locations and number of collisions corresponding
        to each location before, during and after building construction

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_base_year(building_year)
    query_builder.set_duration(collision_interval)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def collision_severity_interact(collision_severity, data_directory="data/Collidium"):
    """
    Queries database and returns maps based on data filtered by collision severity

    Args:
    collision_severity(str): severity of collision impact. Values include Property Damage,
        Injury, Serious Injury and Fatality.

    data_directory(str): Input with path to database location

    Returns: Three maps showing building locations and number of collisions corresponding
        to each location before, during and after building construction

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_c_severity(collision_severity)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def collision_type_interact(collision_type, data_directory="data/Collidium"):
    """
    Queries database and returns maps based on data filtered by collision type

    Args:
    collision_type(str): Type of collision, characterized by entities involved. Values
        include Vehicle only and Bike/Pedestrian

    data_directory(str): Input with path to database location

    Returns: Three maps showing building locations and number of collisions corresponding
        to each location before, during and after building construction

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_c_type(collision_type)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def radius_interact(radius_from_building, data_directory="data/Collidium"):
    """
    Queries database and returns maps based on proximity of collisions to building site

    Args:
    radius_from_building(int): Maximum distance from building location a collision can be
        in order to be included in the building's collision count. All buildings with a
        radius_from_building number less than this input will be included in collision counts.

    data_directory(str): Input with path to database location

    Returns: Three maps showing building locations and number of collisions corresponding
        to each location before, during and after building construction

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_radius(radius_from_building)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def all_factor_interact(building_category, building_year, collision_interval, #pylint: disable=too-many-arguments
                        collision_severity, collision_type, radius_from_building,
                        data_directory="data/Collidium"):
    """
    Queries database and returns maps based on proximity of collisions to building site

    Args:
    building_category(st): String indicating which type of building user would
        like to see location and collision data plotted. Options include (MULTIFAMILY,
        COMMERCIAL, INDUSTRIAL, INSTITUTIONAL SINGLE FAMILY/DUPLEX, ALL)

    building_year(int): Year building construction was completed. Can take values 2014-2017.

    collision_interval(int): Number of months before and after construction period user
        wishes to count collisions. Can take values 6-12.

    collision_severity(str): severity of collision impact. Values include Property Damage,
        Injury, Serious Injury and Fatality.

    collision_type(str): Type of collision, characterized by entities involved. Values
        include Vehicle only and Bike/Pedestrian

    radius_from_building(int): Maximum distance from building location a collision can be
        in order to be included in the building's collision count. All buildings with a
        radius_from_building number less than this input will be included in collision counts.

    data_directory(str): Input with path to database location

    Returns: Three maps showing building locations and number of collisions corresponding
        to each location before, during and after building construction

    Raises:
        ValueError: If data_directory is not a valid path a value error is raised.
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_b_category(building_category)
    query_builder.set_base_year(building_year)
    query_builder.set_duration(collision_interval)
    query_builder.set_c_severity(collision_severity)
    query_builder.set_c_type(collision_type)
    query_builder.set_radius(radius_from_building)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)
