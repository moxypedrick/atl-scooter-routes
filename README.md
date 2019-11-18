# atl-scooter-routes

This repo has a couple different uses. 

1. The python script creates origin-destination pairs for each scooter in the Atlanta area. To do this it queries an API every five minutes across 168 locations in Atlanta. Each queary
returns the location of the nearest 250 scooters of the company requested. The companies that were operating when I wrote this were (Bird, Lyft, Lime, Boaz, Jump, Gotcha, Bolt, Wheels). 
The script creates a csv database of all observed scooters in Atlanta and their last known location. Any time the location has been displaced
by more than 100' the script writes the last known location, the current/new location, and all times for when each location was first observed to 
a csv database. This is the origin-destination pair. 

2. The R script processes the origin-destination pairs and creates the likely route that the person traveled between the two locations. This is 
done by querying the HERE.com bike routing API. This data is written to a shapefile. 

3. Then there is html, javascript, and css for visualizing this data online. 

Additional data processing and styles were completed in QGIS and Mapbox. 
