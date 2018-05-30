"""
Draws map of Seattle and plots collisions near new buildings.

This moddule's purpose is to draws a map of Seattle and plots points to show
the volume of collisions near new buildings. It plots three maps side by
side, one showing the number of collions before buildings were constructed,
another shows collisions that occured during construction and a third shows
collisions after construction ended.

This module contains two functions including:

    create_map: creates map and plots the location of building permits on it
    with the size of each dot corresponding to the number of collisions that
    occured near that building

    place_maps: renders three maps (created using create_map function) and
    places them side by side next to each other. It creates one map for each
    time period including before construction, during construction and after
    construction.

This module raises the following exceptions:

    IndexError: If a dataframe is passed to the create_map function or the
    place_maps function that does not contain the correct fields, an Index
    Error is raised.

    KeyError: If a string other than "before", "during", or "after" is
    passed as the second argument to create_map then a KeyError is raised.
"""

import branca
import folium
import numpy as np

def create_map(data, period):
    """
    Creates a map and plots new buildings (location) and collisions (marker size)

    Args:
    data: a dataframe that contains the following fields:
        b_id (int): buiding id number (key)
        b_lat (float): latitude of building
        b_long (float): longitude of building
        before (int): Number of collisions that happend in period prior
        to construction
        duirng (int): Number of collisions that happend in period during
        construction
        after (int): Number of collisions that happend in period after
        construction

    period (string): String of value "before", "during" or "after"
        indicating whether function should plot volume of collisions before,
        during or after construction

    Returns:
    Image of map with building locations plotted on it. The size of the
    marker corresponds to the number of collisions that happened in the
    period (e.g., before, during or after) identified in the inputs

    Raises:
        IndexError: If a dataframe is passed to the create_map function or
        the place_maps function that does not contain the correct fields, an
        Index Error is raised.

        KeyError: If a string other than "before", "during", or "after" is
        passed as the second argument to create_map then a KeyError is
        raised.

        ValueError: If input data is too big it is difficult to render in
        jupyter. If this happens, a ValueError is raised.

    """

    true_set = set(['b_lat', 'after', 'before', 'b_id', 'b_long', 'during'])
    if not set(list(data)) == true_set:
        raise IndexError("Data set does not contain correct fields")

    if data.shape[0] > 800:
        raise TypeError("Please select 800 or fewer observations from dataframe.")

    location = [np.mean(data['b_lat']), np.mean(data['b_long'])]

    my_map = folium.Map(location=location, zoom_start=11)

    for index, row in data.iterrows(): #pylint: disable=unused-variable
        folium.CircleMarker(
            location=[row['b_lat'], row['b_long']],
            radius=row[str(period)]/20,
            fill=True,
            fill_color='#132b5e').add_to(my_map)
    return my_map


def place_maps(data):
    """
    Draws three maps, plotting buiding permit locations with size
    representing number of collisions. Maps included show collisions,
    before, during and after building construction.

    Args:
    data: a dataframe that contains the following fields:
        b_id (int): buiding id number (key)
        b_latitude (float): latitude of building
        b_longitude (float): longitude of building
        before (int): Number of collisions that happend in period prior
        to construction
        during (int): Number of collisions that happend in period during
        construction
        after (int): Number of collisions that happend in period after
        construction.

    Returns:
        Three map images, with building permit locations identified. Maps
        each show building locations (location of dot), and number of
        collisions (size of dot). The three maps shown include collisions
        before construction (left), during construction (middle) and after
        construction (right).

    Raises
        IndexError: If a dataframe is passed to the create_map function or
        the place_maps function that does not contain the correct fields, an
    """

    map_grid = branca.element.Figure()
    titles = branca.element.Element('<big><b><table class="equalDivide" ' + \
                                    'cellpadding="0" cellspacing="0" ' + \
                                    'width="100%" border="0"><tr>' + \
                                    '<td  width="33%"><center>Before ' + \
                                    'Construction</center></td>' + \
                                    '<td  width="33%"><center>During ' + \
                                    'Construction</center></td>' + \
                                    '<td  width="33%"><center>After ' +\
                                    'Construction</center></td></tr>' + \
                                    '</table></b></big>')
    map_grid.html.add_child(titles)

    map_1 = create_map(data, "before")
    map_2 = create_map(data, "during")
    map_3 = create_map(data, "after")

    loc_1 = map_grid.add_subplot(1, 3, 1)
    loc_2 = map_grid.add_subplot(1, 3, 2)
    loc_3 = map_grid.add_subplot(1, 3, 3)

    loc_1.add_child(map_1)
    loc_2.add_child(map_2)
    loc_3.add_child(map_3)

    return map_grid

