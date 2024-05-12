# Weather ETL Process (IBM practice project on shell scripting)
 *This is all gotten from the project - https://www.coursera.org/learn/hands-on-introduction-to-linux-commands-and-shell-scripting/ungradedWidget/u1vK5/reading-practice-project-overview*

## Description
You've been tasked by your team to create an automated Extract, Transform, Load (ETL) process to extract daily weather forecast and observed weather data and load it into a live report to be used for further analysis by the analytics team. As part of a larger prediction modelling project, the team wants to use the report to monitor and measure the historical accuracy of temperature forecasts by source and station.
<br>
As a proof-of-concept (POC), you are only required to do this for a single station and one source to begin with. For each day at noon (local time), you will gather both the actual temperature and the temperature forecasted for noon on the following day for Casablanca, Morocco.
<br>
At a later stage, the team anticipates extending the report to include lists of locations, different forecasting sources, different update frequencies, and other weather metrics such as wind speed and direction, precipitation, and visibility.
<br>
For this practice project, you'll use the weather data package provided by the open source project wttr.in, a web service that provides weather forecast information in a simple and text-based format. 
<br>

## Expected result (should be tab-seperated)
You must extract and store the following data every day at noon, local time, for Casablanca, Morocco:
- The actual temperature (in degrees Celsius)
- The forecasted temperature (in degrees Celsius) for the following day at noon

Result should look like this: 

| Year | month	| day	| obs_tmp	| fc_temp |
|------|--------|-----|---------|---------|
| 2023 | 1	| 1	 | 10	| 11 |
| 2023 | 1	| 2	| 11 | 	12 |
| 2023 |	1	 | 3	| 12	| 10|

## Instructions
These are to be executed on a terminal unless otherwise stated

### Create file to hold the daily weather result 
`touch rx_poc.log`

### Add column headers to the file to recreate the table seperated by tabs
```
header=$(echo -e "year\tmonth\tday\thour\tobs_tmp\tfc_temp")
echo $header>rx_poc.log
```

### Create a text file called rx_poc.sh and make it a bash script (make it executable too)
```
touch rx_poc.sh
chmod u+x rx_poc.sh
ls -l rx_poc.sh
```
- the 1st line creates the file
- the 2nd line makes it executeable, giving execution rights to the user
- the 3rd line checks that the permission has been granted. Should look like this `-rwxr-r-r 1 <other stuff>`
This file has already been created in the folder so you can skip that step. It also contains the script to be ran.

### Schedule the time the script has to run
You need to check the time difference. For this project, the city is Casablance (UTC+1). You need to compare your time against UTC by running the `date` command twice.<br>
Should look something like this
```
$ date
Mon Feb 13 12:28:12 EDT 2023
$ date -u
Mon Feb 13 16:28:16 UTC 2023
```
This means that the system's time is UTC-4, and it is 5 hours behind Casablanca's time. To make run the script at 12 pm Casablanca's time, I'd have to schedule the script to run at 7am my time.<br>
You can schedule the job (automating the ETL process) using crontab
- Make sure you're in the directory containing the script. Use `realpath rx_poc.sh` to get the fullpath of the script. 
- Intialize: `crontab -e`. You should see the last line of the result `# m h  dom mon dow   command`
- Schedule job for 7am every day: ` 0 7 * * * <filepath>`. <br>
E.g: `0 7 * * * /home/shell-scripts/weather/rx_poc.sh`.
- Save the crontab by pressing *CTRL + X*, Then *Y* to confirm.

  <br>

You're done. That shpuld run everyday at 12pm Casablanca time and save the result to the file `rx_poc.log`.
