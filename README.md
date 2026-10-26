# Predicting The Occupancy of a Room
Source code and documentation for modelling the occupancy of a room using splines.

## Python Modules Used
- Numpy
- Matplotlib
- Pandas (for dataframes)
- Time

## Usage
Source code folder src contains functions necessary to run model and its analysis. 
Use run.py to run all the functions.

## Engineering Context
Monash Smart Infrastructure utilises sensors in certain buildings that collect data for occupancy and environmental variables such as temperature, carbon dioxide concentration and particulate matter among others. With this data, is it possible to predict the future state of a room based on this data?
In this documentation, the goal is to predict the future occupancy in Building 60 G20 at a specific hour of the week based on data collected throughout the previous weeks. This could be useful in finding if a room is being underutilised at certain times of the day and provides a basis for thinking for further questions such as if occupancy is dependent on environmental factors or if occupancy in one room is dependent on occupancy in another. With further data, a model of the entire building and the environmental factors and occupancy can be established.

  

