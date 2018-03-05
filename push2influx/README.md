Shair to InfluxDB
=================

This script reads official sensor data from the SMHI Sensor Observation Service
and pushes the information to an InfluxDB instance of your choice.

After configuring the script, schedule it in a cron job or other scheduler on
your computer.

!["Overlay graph. Official + citizen science sensors"](https://raw.githubusercontent.com/luftdata/utilities/master/push2influx/PM10.jpg)

Finding the correct official sensor
-----------------------------------

#1 The [SMHI sensor observation service](http://shair.smhi.se/52North/static/doc/api-doc/index.html) has a list of all sensors in the API at

    http://shair.smhi.se/52North/api/v1/stations/

Find your station in the list and make a note of the id of your station (properties/id). There can be several ID:s as the individual sensors seem to be represented as a station each.

#2 Find the time series id for the station by browsing to `http://shair.smhi.se/52North/api/v1/stations/<NN>` where NN is the id of your sensor. You should find the correct time series id undet "properties".

```javascript
    "properties": {
        "id": "182",
        "label": "Stockholm Sveav\u00e4gen 59 Gata - 182",
        "timeseries": {
            "85": {
                "category": {
                    "id": "5",
                    "label": "PM10"
                }, ...
```


#3 Use the time series id to get overview data at `http://shair.smhi.se/52North/api/v1/timeseries/<NN>` where NN is the time series id from the previous step. Use this URL in the script as a value for `API_TIMESERIES_URL`.


After adding the API URL, try to run the script. You should be able to see data in InfluxDB/Grafana. You can easily overlay the data in the same graph as your own sensor:

