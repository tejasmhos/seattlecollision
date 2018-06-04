# Collidium - Seattle Collision Research Tool
[![Build Status](https://travis-ci.org/tejasmhos/seattlecollision.svg?branch=master)](https://travis-ci.org/tejasmhos/seattlecollision.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/tejasmhos/seattlecollision/badge.svg?branch=master)](https://coveralls.io/github/tejasmhos/seattlecollision?branch=master) 

Collidium is a tool that allows users to visualize and understand the impact of construction on the occurence of traffic accidents in the City of Seattle. It's structered as a Jupyter notebook with interactive controls. 

To use the package, you need to pull it from Github, and follow the instructions given below.


## Organization of the Project

The organization of our project is shown below:

```
seattlecollision/
	|- seattlecollision/
		|- build_data_libraries/
			|- process_data.py
			|- table_builder.py
		|- data/
			|- raw_data/
				|- raw_buildings_input.csv
				|- raw_collision_input.csv
			|- Collidium
			|- Test_Data_For_Draw_Markers.csv
			|- buildings.csv
			|- collidium_data.csv
			|- collisions.csv
		|- tests/
			|- test_draw_markers.py
			|- test_interactions_functionality.py
			|- test_process_data.py
			|- test_table_builder.py
		|- Collidium.ipynb
		|- __init__.py
		|- draw_markers.py
		|- interaction_functionality.py
		|- query_class.py
	|- doc/
		|- Tech Review Presentation.pdf
		|- finalpresentation.pdf
		|- functionaldesign.md
	|- tutorial/
		|- placeholder.py
	|- .coveragerc
	|- .travis.yml
	|- LICENSE
	|- README.md
	|- collidium_env.yml
	|- requirements.txt		
```
## Installations

To operate the Collidium jupyter notebook, follow the steps below:
1. Clone the respository onto your machine
2. Run the setup files to install the dependencies for running the notebook.
 ``` python setup.py install ```
 3. To ensure the installations have been installed correctly. Install the elements in the package requirements.
=======
## Data Sources

We use two main data sources. One of our data sources is the Building Permit Dataset, which we took from the Seattle Open Data portal. This data is from 2014 - 2018. Our final cleaned dataset is 440 rows.

Our second dataset is the Collisions dataset. This dataset has collisions from 2003 - 2018.  The final cleaned dataset has 60,000 rows.

We take both these datasets and create a dataset called Collidium. We calculate the distance between collisions and buildings and join collisions that occur within 1500 ft and 1 year of building permit. This dataset helps us reduce the complexity of our queries.

## Installation

To operate the Collidium jupyter notebook, follow the steps below:
1. Clone the respository onto your machine
2. Run the setup files to install the dependencies for running the notebook.
``` python setup.py install ```
3. To ensure the installations have been installed correctly. Install the elements in the package requirements.

``` pip install -r requirements.txt```

4. Launch [Collidium](seattlecollision/Collidium.ipynb) in a Jupyter notebook
 
 ## Project History
 
 
 
 ## Data
 The data sourced for Collidium was taken from the [Seattle Open Data Portal](https://data.seattle.gov/). The tool uses processed versions of the [Building Permits](https://data.seattle.gov/Permitting/Building-Permits-Current/mags-97de/data) dataset and [Collisions](https://data-seattlecitygis.opendata.arcgis.com/datasets/collisions/data) dataset. The processed datasets were aggregated into a database which provides the underlying data for the Collidium notebook.
 
 ## Acknowledgements
 
 Collidium was developed for a class project in Spring 2018 for the Data 515A - Software Engineering for Data Scientists course at University of Washington. Many thanks to instrcutors David A. C. Beck and Joseph L. Hellerstein for their insight and guidance throughout project development.


## How to Use

After pulling and running the setup script, the project can be executed by opening the Collidium.ipynb notebook. All tools and functionality is integrated into this notebook. No other application need to be opened.

## Contributors

There are 4 primary contributors to this project. They are:

- Alyssa Goodrich
- Dan White
- Ian Kirkman 
- Tejas Hosangadi

## Acknowledgements

A thanks to our DATA 515 course professors, Joe Hellerstein and Dave Beck, of the University of Washington eScience Institute, for there guidance and assistance that they gave us during the course of the project. 

## License

This project is licensed under the MIT license.
