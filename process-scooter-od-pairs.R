#' 10/12/19
#' @author David Pedrick
#' @description   This script takes an Origin-Destination pair and returns a likely 
#' route to travel in between the Origin-Destination. 
#' 
#' To calculate the route, I use the HERE api. It returns a json
#' object of the route as well as meta data that says time, distance, etc. 
#' 
#' 
#' 


library(tidyverse)
library(stringr)     
library(sf)     
library(raster)
library(sp)
library(mapview)
library(tmap)
library(tidycensus)
library(tigris)
library(lehdr)
library(httr) 
library(jsonlite)
library(viridis)
library(ggpubr)
library(rgdal)
library(xml2)
library(curl)
library(maptools)
library(GISTools)

get_distance <- function(origin, destination, mode = 'bicycle', app_id = '', app_code = ''){
  #' distance
  
  url = paste0('https://route.api.here.com/routing/7.2/calculateroute.json?',
               'app_id=', app_id,
               '&app_code=', app_code,
               '&waypoint0=geo!', origin,
               '&waypoint1=geo!', destination,
               '&mode=fastest;', mode,
               ';traffic:disabled',
               '&routeattributes=sh')
  
  text_response <- url %>%
    GET() %>% 
    content(as = "text") %>%
    fromJSON()
  
  return(text_response)
}

## Read in scooter o-d pairs. 
## Use Googles crs for this

#scooter_df <- read_csv("C:/Users/dpedrick/OneDrive/ScooterData/sample_od.csv")
scooter_df <- read_csv("C:/Users/dpedrick/OneDrive/ScooterData/O-D Data/missing-days - 27.csv")


#' iterate over the rows of the dataframe
#' assemble lat,lon pairs to use as waypoints in the route query
#' scooter_df == time, id, company, o-lat, o-lon, departure, arrival, d-lat, d-lon
#' 
#' 
#' Final spdf === scooter_df, distance, duration, speed, geometry



scooter_length <- nrow(scooter_df)
scooter_df <- tibble::rowid_to_column(scooter_df, "ID")

#' initialize the spdf
origin <- paste0(scooter_df[1,]$'o-lat',',',scooter_df[1,]$'o-lon')
destination <- paste0(scooter_df[1,]$'d-lat',',', scooter_df[1,]$'d-lon')
id2 <- scooter_df[1,]$ID


shape <- get_distance(origin, destination, 'bicycle', app_id = 'Mtp0R3CkrTuuXGy0HvrX', app_code = 'MmRLt66MX33Jl1c6RF3F0Q')
coords2 <- shape$response$route$shape

data_df <- data.frame(NA, NA, NA, NA)
names(data_df) <- c('id', 'lat', 'lon', 'num')


length <-length(coords2[[1]])
for(i in seq(1,length,by=1)){
  str <- strsplit(coords2[[1]][i],",")
  lat <- as.numeric(str[[1]][1])
  lon <- as.numeric(str[[1]][2])
  data_df2 <- data.frame(id2, lat, lon, i)
  names(data_df2) <- c('id', 'lat', 'lon', 'num')
  data_df <- rbind(data_df, data_df2)
}

data_df <- na.omit(data_df)
coordinates(data_df) <- c("lon","lat")
lines <- SpatialLines(list(Lines(list(Line(data_df)), "id")))
lines <- st_as_sf(lines)
lines$id <- id2



for(i in seq(2,scooter_length,by=1)){
  print(i)
  origin <- paste0(scooter_df[i,]$'o-lat',',',scooter_df[i,]$'o-lon')
  destination <- paste0(scooter_df[i,]$'d-lat',',', scooter_df[i,]$'d-lon')
  id2 <- scooter_df[i,]$ID
  shape <- get_distance(origin, destination, 'bicycle', app_id = 'Mtp0R3CkrTuuXGy0HvrX', app_code = 'MmRLt66MX33Jl1c6RF3F0Q')
  #' I need the shapefile, time, distance, route
  #' convert the scooter_df to a spdf and then add the results to that.
  coords2 <- shape$response$route$shape
  data_df <- data.frame(NA, NA, NA)
  names(data_df) <- c('lat', 'lon', 'num')
  length <-length(coords2[[1]])
  if(length>1){
    for(i in seq(1,length,by=1)){
      str <- strsplit(coords2[[1]][i],",")
      lat <- as.numeric(str[[1]][1])
      lon <- as.numeric(str[[1]][2])
      data_df_d <- data.frame(lat, lon, i)
      names(data_df_d) <- c('lat', 'lon', 'num')
      data_df <- rbind(data_df, data_df_d)
    }
    data_df <- na.omit(data_df)
    coordinates(data_df) <- c("lon","lat")
    lines2 <- SpatialLines(list(Lines(list(Line(data_df)),"id")))
    lines2 <- st_as_sf(lines2)
    lines2$id <- id2
    #View(lines)
    lines <- rbind(lines, lines2)
  }
}

scooterRoutes <- merge(lines, scooter_df, by.x = "id", by.y = "ID")


#' write to file to do spatial join in QGIS
st_write(scooterRoutes, "C:/Users/dpedrick/Desktop/scooter-rides-27.shp")


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
##########################################