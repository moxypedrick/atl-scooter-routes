#' 10/12/19
#' @author David Pedrick
#' @description   This script takes the spatial joined data file from 
#' process-scooter-od-pair and atlanta street segments and cleans the 
#' data and filters out null values
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
library(anytime)




scooter_routes <- st_read("C:/Users/dpedrick/OneDrive/ScooterData/roads-by-scooter-counts/scooter_roads_by_count.shp") %>%
  st_transform(3857) 

atl_roads <- st_read("C:/Users/dpedrick/OneDrive/ScooterData/atl-roads-clipped.shp") %>%
  st_transform(3857) 

#C:\Users\dpedrick\OneDrive\ScooterData\roads-by-scooter-counts\scooter_roads_by_count.shp
#C:\Users\dpedrick\OneDrive\ScooterData\atl-roads-clipped.shp


scooter_routes <- scooter_routes %>%
  dplyr::select(osm_id,NAME_2,OBJECTID,OWNER, MANAGEMENT,JURISDICTI, GlobalID, name_3, osm_id_2,scotr.d_co) 


scooter_routes <- scooter_routes %>%
  mutate(
     ScooterCount = scotr.d_co
  ) %>%
  dplyr::select(
    osm_id,NAME_2,OBJECTID,OWNER, MANAGEMENT,JURISDICTI, GlobalID, name_3, osm_id_2,ScooterCount
    ) %>%
  filter(ScooterCount>0)
 

scooter_routes_osmid <- scooter_routes %>%
  filter(!is.na(osm_id)) %>%
  filter(is.na(osm_id_2)) %>%
  dplyr::select(
    osm_id, NAME_2,OBJECTID,OWNER, MANAGEMENT,JURISDICTI, GlobalID, name_3,ScooterCount
  )
  
scooter_routes_osmid2 <- scooter_routes %>%
  filter(!is.na(osm_id_2)) %>%
  dplyr::select(
    NAME_2,OBJECTID,OWNER, MANAGEMENT,JURISDICTI, GlobalID, name_3, osm_id_2,ScooterCount
  ) %>%
  mutate(
    osm_id = osm_id_2
  )%>%
  dplyr::select(
    osm_id, NAME_2,OBJECTID,OWNER, MANAGEMENT,JURISDICTI, GlobalID, name_3,ScooterCount
  )

scooter_routes_clean <- rbind(scooter_routes_osmid, scooter_routes_osmid2)


scooter_routes_na_id <- scooter_routes %>%
  filter(is.na(osm_id_2) & is.na(osm_id))%>%
  dplyr::select(
    osm_id, NAME_2,OBJECTID,OWNER, MANAGEMENT,JURISDICTI, GlobalID, name_3,ScooterCount
  )


st_geometry(scooter_routes_clean) <- NULL

scooter_routes_joined <- atl_roads %>%
  dplyr::left_join(.,as.data.frame(scooter_routes_clean), by="osm_id")


st_write(scooter_routes_joined, "C:/Users/dpedrick/Desktop/scooter_routes_joined.shp")


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
###########################################################################################


