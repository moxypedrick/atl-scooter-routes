# -*- coding: cp1252 -*-
import datetime
import glob
import json
import os
import urllib3.request
import math
import datetime
import time
from datetime import timedelta
import socket
import csv
import gc
from pympler import muppy, summary
import sys
import certifi

def main():

    
    
    scooterCompanies = ['lyft', 'boaz', 'bolt', 'gotcha', 'lime', 'bird', 'spin', 'wheels', 'jump']
    queryGrid = ['33.7856757,-84.40187104','33.78051707,-84.38666065','33.7753564,-84.37145227',
    '33.77019369,-84.35624591','33.77297421,-84.40804687','33.76781649,-84.39283855',
    '33.76265672,-84.37763224','33.75749492,-84.36242793','33.75233108,-84.34722563',
    '33.76027255,-84.4142207','33.75511572,-84.39901444','33.74995686,-84.38381019',
    '33.74479597,-84.36860794','33.73963304,-84.35340771','33.74757071,-84.42039252',
    '33.74241479,-84.40518833','33.73725683,-84.38998614','33.73209684,-84.37478595',
    '33.72693481,-84.35958778','33.72971368,-84.4113602','33.72455663,-84.39616008',
    '33.71939754,-84.38096196','33.87458112,-84.35858392','33.87220289,-84.39522543',
    '33.86704291,-84.37999862','33.86188088,-84.36477383','33.85671682,-84.34955105',
    '33.85950067,-84.40140919','33.85434159,-84.38618445','33.84918047,-84.37096173',
    '33.84401731,-84.35574101','33.84679827,-84.40759094','33.84164009,-84.39236827',
    '33.83647988,-84.37714761','33.83131762,-84.36192896','33.83409568,-84.41377067',
    '33.82893841,-84.39855007','33.8237791,-84.38333148','33.81861775,-84.3681149',
    '33.81345437,-84.35290033','33.81107815,-84.38951334','33.88113339,-84.3997474699999',
    '33.86603713,-84.44256837','33.85572804,-84.4121129199999','33.8406274499999,-84.4549174999999',
    '33.83032197,-84.42447033','33.80968654,-84.3636000999999','33.7993566,-84.3331770399999',
    '33.81521704,-84.4672585999999','33.80491518,-84.4368197','33.79460516,-84.4063888299999',
    '33.7842869899999,-84.3759659899999','33.77396067,-84.3455511899999','33.7636261999999,-84.31514443',
    '33.78980593,-84.4795916599999','33.77950768,-84.44916104','33.7692012799999,-84.41873843',
    '33.73823319,-84.32751878','33.7643941199999,-84.4919167099999','33.75409948,-84.46149436',
    '33.74379669,-84.43108001','33.74926448,-84.5346558499999','33.73898161,-84.5042337499999',
    '33.7286905799999,-84.47381966','33.71839141,-84.44341357','33.70808409,-84.4130155',
    '33.69776864,-84.38262543','33.68744504,-84.3522433899999','33.7238476599999,-84.54695662',
    '33.7135684,-84.51654279','33.70328099,-84.48613695','33.6723699,-84.3949674699999',
    '33.66204993,-84.3645936599999','33.6881545099999,-84.52884382','33.67787071,-84.49844625']
    
    counter = 1
    currentTime = datetime.datetime.now()
    curfewStart = datetime.time(21,30,0)
    curfewEnd = datetime.time(4,0,0)
    lastRunTime = datetime.datetime(2019, 9, 17, 18, 20, 00)
    stopTime = datetime.datetime(2019, 11, 10, 21, 30, 00)

    
    print('Internet connected? ', internet())

    #scooterData = readScooterLocationMemory()
    
    # Run this script until the current time is greater than a datetime in the future
 
    while currentTime < stopTime:
        # Read in the last known location of all of the scooters in the atl region
        scooterData = readScooterLocationMemory()

        # Pause the script if the current time is during atlanta's scooter curfew
        if currentTime.time() > curfewStart or currentTime.time() < curfewEnd:
            # During curfew backup the last known scooter location memory, scooterData
            writeCurrentScooterLocationMemory(scooterData)
            timePause = datetime.datetime.combine(datetime.date.today() + timedelta(days=1), curfewEnd) - currentTime
            print("Curfew is active. Pausing for: ", timePause)
            time.sleep(timePause.total_seconds())
            
        else:
            print('lastRunTime: ', lastRunTime)
            print('currentTime: ', currentTime)
            timeGap = currentTime - lastRunTime
            print('timeGap: ',timeGap)

            # Only run this every 5 minutes. 
            # It takes longer than 5 mintes to make all queries so this is rarely used. 
            if timeGap.total_seconds() < 300:
                print('sleep: '+str(300-timeGap.total_seconds()))
                # During pauses, backup the last known scooter location memory, scooterData
                writeCurrentScooterLocationMemory(scooterData)
                time.sleep(300-timeGap.total_seconds())
            else:           
                print('New Run #'+str(counter))
                lastRunTime = datetime.datetime.now()
                # Iterate over all of the scooter companies that operate in atlanta
                for company in scooterCompanies:
                    print(company)
                    # iterate over all of the query points in our query grid
                    # The api gives us a max of 250 scooter per query
                    # if we query at a rate/density greater than 250 scooters per unit density
                    # we can ensure that we get all scooters in the network
                    for location in queryGrid:
                        print("ScooterData getUrlResponse") 
                        now = datetime.datetime.now()  
                        # Run getUrlResponse - this updates the scooterData and writes any knew 
                        # scooter locations to file of unique scooter locations                   
                        scooterData = getUrlResponse(company, scooterData, now, location)
                    # Backup the scooter location memory after each company
                    writeCurrentScooterLocationMemory(scooterData)
                counter = counter + 1
                
                print('Finished Run #'+str(counter))

        currentTime = datetime.datetime.now()
        #gc.collect()
        
   

    return

def internet(host="8.8.8.8", port=53, timeout=3):
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except socket.error as ex:
    print('internet error')
    print(ex)
    return False

def readScooterLocationMemory():
    currentScooterLocations = dict()
    #directory = 'C:/Users/dpedrick/OneDrive/ScooterData/scooterMemory.csv'
    directory = 'C:/Users/David/Desktop/scooterMemory.csv'
    if os.path.exists(directory):
        scooter_data_file = open(directory, "r+")
        for line in scooter_data_file:
            vehicleList = line.split(',')
            returnVehicle = dict(id=vehicleList[1],company=vehicleList[2], lat=float(vehicleList[3]), long=float(vehicleList[4]),
                                arrival=vehicleList[5], departure=str(vehicleList[6]).rstrip())
            currentScooterLocations[vehicleList[1]] = returnVehicle
        scooter_data_file.close()
        #del scooter_data_file
    return currentScooterLocations

def writeCurrentScooterLocationMemory(scooterDict):
  now = datetime.datetime.now()  
  scooterDataList = []
  scooterData = scooterDict
  for key in scooterData.keys():
    scooterDataList.append(scooterData[key])
      

  writeDataFile(scooterDataList, 'lastKnownLocationBackup', now)
  #scooterDataList = []
  return
  
def getUrlResponse(company, scooterData, currentTime, location):
    writeList = []
    now = currentTime
    userLocation = location
    #33.767377,-84.386730
    #check to see if we have internet connection
    # if we do complete the api query
    if(internet()):
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED', 
            ca_certs=certifi.where()
            )

        try:
            txtResponse = http.request('GET','https://######################################' + userLocation + '&northeast_point=33.938100,'
                '-84.201316&southwest_point=33.601844,-84.504096&company=' + company + '&mode=ride&randomize=false')
            
            scooterVehicles = json.loads(txtResponse.data.decode('utf-8'))
            del(txtResponse)
            gc.collect()
            
            for vehicle in scooterVehicles['vehicles']:
                outsideATL = vehicle['latitude'] < 33.601844 or vehicle['latitude'] > 33.9381 or vehicle['longitude'] > -84.201316 or vehicle['longitude'] < -84.504096
                if vehicle['vehicle_id'] in scooterData:
                    #check to see if it's outside atl
                    #yes: skip all of this and delete record from scooterDatas
                    if outsideATL:
                        print('deleted this vehicle: ', scooterData[vehicle['vehicle_id']])
                        print(scooterData[vehicle['vehicle_id']])
                        del scooterData[vehicle['vehicle_id']]
                    else: 
                        # Checks to see if the vehicles location has changed since the last time we checked.
                        # the last known location of the scooter is stored in the scooterData dictionary
                        # updateVehicle returns a list [boolean, updated vehicle, distance moved]
                        # if boolean is true, it means the vehicle has not moved 
                        updatedVehicle = didVehicleMove(vehicle, scooterData[vehicle['vehicle_id']], now)

                        if updatedVehicle[1] == True:
                            #Vehicle moved; write the vehicle data from scooterData (last known location) to the 
                            # scooterLocationDatabase.  
                            #scooterData[vehicle['vehicle_id']]['departure'] = now
                            scooterData[vehicle['vehicle_id']]['d_lat'] = vehicle['latitude']
                            scooterData[vehicle['vehicle_id']]['d_lon'] = vehicle['longitude']
                            writeList.append(scooterData[vehicle['vehicle_id']])
                            scooterData[vehicle['vehicle_id']] = updatedVehicle[0]
                            
                        else:
                            #Vehicle did not move; update the scooterData reference for this 
                            # vehicle to the new location of the scooter from the didVehicleMove function
                            scooterData[vehicle['vehicle_id']] = updatedVehicle[0]
                        
                else:
                    # This is a new vehicle. We do not have vehicle in our database
                    # Check to see if its outside atl
                    # yes=skip
                    # no = add the vehicle to our scooterData database
                    if outsideATL:
                        pass
                    else:
                        scooterData[vehicle['vehicle_id']] = dict(id=vehicle['vehicle_id'], 
                                                                company=vehicle['company'],
                                                                lat=vehicle['latitude'], 
                                                                long=vehicle['longitude'],
                                                                arrival=now, departure=-1, 
                                                                destination = [-1,-1])
            
            # back up the newly downloaded data to our file
            # after processing all vehicles from each api call
            writeDataFile(writeList, 'vehicleLogging', now)
                
                
        except Exception as e:
            # something in the try block failed
            print('URL Request failed.')
            print(e)
            
    # Return the updated scooterData (last known location of all scooters in atl) dictionary
    return scooterData

def didVehicleMove(newVehicle, oldVehicle, currentTime): 
    update = bool
    now = currentTime
    oldLat = float(oldVehicle['lat'] * 3.14159 / 180)
    oldLon = float(oldVehicle['long'] * 3.14159 / 180)
    newLat = float(newVehicle['latitude'] * 3.14159 / 180)
    newLon = float(newVehicle['longitude'] * 3.14159 / 180)
    
    x = math.sin((oldLat-newLat)/2)**2
    y = math.cos(oldLat)
    b = math.cos(newLat)
    c = math.sin((oldLon - newLon)/2)**2
    sqrt = math.sqrt(x+y*b*c)
    asin = math.asin(sqrt)*2
    distanceRadians = asin*180*60
    distance = distanceRadians / 3.1415926
    
    if distance > 0.0165:
       update = True
       returnVehicle = dict(id=newVehicle['vehicle_id'],company=newVehicle['company'], lat=newVehicle['latitude'], long=newVehicle['longitude'],
                            arrival=now, departure=-1, d_lon = -1, d_lat = -1)
    else:
       update = False
       returnVehicle = dict(id=newVehicle['vehicle_id'],company=oldVehicle['company'], lat=oldVehicle['lat'], long=oldVehicle['long'],
                            arrival=oldVehicle['arrival'], departure=now, d_lon = -1, d_lat = -1)
    return [returnVehicle, update, distance]

def writeDataFile(vehicleList, file_type, now):
    data_file_type = file_type
    currentTime = datetime.datetime.now()
    if data_file_type == 'lastKnownLocationBackup':
        #directory = 'C:/Users/dpedrick/OneDrive/ScooterData/scooterMemory.csv'
        directory = 'C:/Users/David/Desktop/scooterMemory.csv'
        if os.path.exists(directory):
            os.remove(directory)
        scooter_database_file = open(directory, "w+", newline='')
        for vehicle in vehicleList:          
            writeString = str(currentTime) + ',' + vehicle['id'] + ',' + vehicle['company'] + ',' + str(vehicle['lat']) + ','  + str(vehicle['long']) + ',' + str(vehicle['arrival']) + ','  + str(vehicle['departure']) +  '\n'
            #print(writeString)
            scooter_database_file.write(writeString)
            del writeString
        scooter_database_file.close()
        
    else:
      #directory = 'C:/Users/dpedrick/OneDrive/ScooterData/scooterLocationDatabase.csv'
      directory = 'C:/Users/David/Desktop/scooterLocationDatabase.csv'
      company_file = open(directory, "a+", newline='')
      for vehicle in vehicleList:
          writeString = str(currentTime) + ',' + vehicle['id'] + ',' + vehicle['company'] + ',' + str(vehicle['lat']) + ',' + str(vehicle['long']) + ',' + str(vehicle['arrival']) + ','  + str(vehicle['departure']) + ',' + str(vehicle['d_lon']).rstrip() +',' + str(vehicle['d_lat']).rstrip() + ',' + str(now) +'\n'
          company_file.write(writeString)
          del writeString

      company_file.close()












def alternativeMain():
    scooterData = dict()
    currentTime = datetime.datetime.now()
    lastRunTime = datetime.datetime(2019, 9, 17, 18, 20, 00)
    stopTime = datetime.datetime(2019, 9, 18, 16, 51, 00)

    curfewStart = datetime.time(21,30,0)
    curfewEnd = datetime.time(4,0,0)

    counter = 1
    
    directory = 'C:/Users/dpedrick/Google Drive/E-Scoots/Data/' + '*.txt'
    fNameList = []
    for filename in glob.glob(directory):
        writeList = []
        fNameList = fNameList + [filename]
        #print('New File: ', filename)
        df = pd.read_json(filename)
        date_string = filename[:]
        #print(date_string)
        now = txtToDatetime(str(date_string))
        #print(now)
        for vehicle in df['vehicles']:
            if vehicle['vehicle_id'] in scooterData:
                updatedVehicle = updateVehicle(vehicle, scooterData[vehicle['vehicle_id']], now)
                #print(updatedVehicle)
                if updatedVehicle[1] == True:
                    scooterData[vehicle['vehicle_id']] = updatedVehicle[0]
                else:
                    scooterData[vehicle['vehicle_id']]['departure'] = now
                    writeList.append(scooterData[vehicle['vehicle_id']])
                    scooterData[vehicle['vehicle_id']] = updatedVehicle[0]
            else:
                scooterData[vehicle['vehicle_id']] = dict(id=vehicle['vehicle_id'], company=vehicle['company'],lat=vehicle['latitude'], long=vehicle['longitude'],arrival=now, departure=-1)
        #print(writeList)
        writeDataFile(writeList)

    scooterDataList = []
    for key in scooterData.keys():        
        scooterDataList.append(scooterData[key])
        

    writeDataFile(scooterDataList, 'lasetKnownLocationBackup')
    return
    
def txtToDatetime(txtline):
    # convert a text line to return a date. This requires that you input
    # a text line like 25/03/2015 01:45:30
    #                  Mon Sep 16 2019 18_56_34 . From this it assembles
    # datetime.datetime object
    
    Date = txtline.split('-')[2]
    Year = int(Date.split(' ')[3])
    Month = 9
    Day = int(Date.split(' ')[2])
    hour = int(Date.split(' ')[4][0:2])
    minute = int(Date.split(' ')[4][3:5])
    second = int(Date.split(' ')[4][6:8])
    

    return datetime.datetime(Year, Month, Day, hour, minute, second)

def combineFiles(scooterCompanyList):
    scooterCompanies = scooterCompanyList
    for company in scooterCompanies:
        directory = 'C:/Users/dpedrick/Google Drive/E-Scoots/Data/Company Files/' + company + '_total.txt'
        company_file = open(directory, "a+", newline='')
        filenames = inputFileNames(company)

        for files in filenames:
            root_directory = files[:40] + 'Data/Processed Files/' + files[45:]

            df = pd.read_json(files)
            date_string = files[54:74]
            vehicles = df['vehicles']
            for item in vehicles:
                plist = (list(item.values()))
                writeString = date_string + ',' + str(plist[1]) + ',' + str(plist[3]) + ',' + str(plist[7]) + ',' + str(
                    plist[9]) + ',' + str(plist[10]) + ',' + str(plist[12]) + ',' + str(plist[13]) + ',' + str(
                    plist[14]) + ',' + str(plist[15]) + '\n'
                company_file.write(writeString)
            os.rename(files, root_directory)
    return

main()
