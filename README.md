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
## Installation

To install run 
 ``` pip install -r requirements.txt```

 Setup
 ``` python setup.py install ```

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