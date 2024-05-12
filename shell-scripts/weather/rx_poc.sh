#! /bin/bash
#This script automates the process for getting the current temp and the temp for noon the next day in a particular city.
#It gets data from https://github.com/chubin/wttr.in. Inspect that to get the details.
# This script is from the IBM course on shell scripting (practice project)
# further instructuons can be found on the readme.

#filename for storing the raw data
weather_report=raw_data_$(date +%Y%m%d)

#Download the data for that day and save to file
city=Casablanca #you can set this to any city you want
curl wttr.in/$city --output $weather_report

#search for all lines containing temperatures
grep °C $weather_report > temperatures.txt

#the current temp is in the first line. Extract just the numerical value
obs_tmp=$(head -1 temperatures.txt | tr -s " " | xargs | rev | cut -d " " -f2 | rev)

#the forecast for tomorrow at noon is on the 3rd line, 2nd temp field.
fc_temp=$(head -3 temperatures.txt | tail -1 | tr -s " " | cut -d "C" -f2 | rev | cut -d " " -f2 | rev)

#Store the current hr, day, mon, yr for the city to shell variables
TZ='Morocco/Casablanca'
hour=$(TZ='Morocco/Casablanca' date -u +%H) 
day=$(TZ='Morocco/Casablanca' date -u +%d) 
month=$(TZ='Morocco/Casablanca' date +%m)
year=$(TZ='Morocco/Casablanca' date +%Y)

#save extracted data into the log file 
record=$(echo -e "$year\t$month\t$day\t$hour\t$obs_tmp\t$fc_temp")
echo $record>>rx_poc.log

