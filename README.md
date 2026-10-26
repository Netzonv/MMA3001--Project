# MMA3001--Project

## Engineering Problem
Monash Smart Infrastructure utilises sensors in certain buildings that collect data for occupancy and environmental variables such as temperature, carbon dioxide concentration and particulate matter among others. With this data, is it possible to predict the future state of a room based on this data?
In this documentation, the goal is to predict the future occupancy in Building 60 G20 at a specific hour of the week based on data collected throughout the previous weeks. This could be useful in finding if a room is being underutilised at certain times of the day and provides a basis for thinking for further questions such as if occupancy is dependent on environmental factors or if occupancy in one room is dependent on occupancy in another. With further data, a model of the entire building and the environmental factors and occupancy can be established.
However, some limitations in the scope are that it does not find a relationship between environmental factors and occupancy and therefore assumes the values for these factors do not change from the week the data is collected from. Additionally, another limitation is that only one room’s data is utilised.

## Inputs and Outputs
Input:
	Timestamped occupancy data in Building 60 G20 
This is a .csv dataset with columns: ‘sensor_id’, ‘floor_space_id’, ‘current_status’, ‘headcount’, ‘timestamp_record’, ‘timestamp_event’, ‘occupancy_label’, ‘day_of_week’, ‘day_of_week_num’, ‘hour’, ‘is_weekend’. 
The first two columns should stay the same for every row because we are utilising data for a singular room.
	‘count’ gives the headcount as integer
	‘day_of_week’ gives a string with the day
	‘day_of_week_num’ gives index on the day, with 0 being Monday and 6 being Sunday
	‘is_weekend’ gives a Boolean value.
 

Output: 
	Peaks and trends of occupancy in Building 60 G20

This can be seen through using a smoothing spline approximating the dataset. This brings out Figure 2:
 
From this output, occupancy usually begins in the morning, peaks at midday and stops at midnight. In this week, Tuesday had the greatest number of occupants at midday. Each day usually has two peaks except Friday. This could mean occupants leave the room for a temporary break such as lunch. 
This output can be used to judge if a space is utilised well, underutilised or over-utilised. Therefore, this aids in planning and developing spaces in the building. 

Invalid Inputs
If sensor ID or floorspace ID do not equal the correct value or if there is a timestamp missing, then the row is removed from the dataset. If there is a missing value in headcount column, take the average between the top and bottom rows. 

## Finding Trends and Patterns
We now have a dataset that we can find trends and patterns through. We extract the timestamp and headcount columns and turn them into two matrices such that both can be graphed against each other. Then, use a smoothing spline to approximate the dataset.

As seen in the outputs, a smoothing spline does a good job at finding a general trend throughout the week. However, it is limited in that it only takes one week of data to find a trend through. It would be more precise and general if more weeks are used as data. This would mean taking multiple weeks and average out the number of occupants at every hour.
