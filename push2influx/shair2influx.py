#coding: utf-8
import requests
import json

# Set up parameters

# See README for details on finding your time series. This example is PM10 for
# Sveavägen in Stockholm.
API_TIMESERIES_URL = "http://shair.smhi.se/52North/api/v1/timeseries/85"

# InfluxDB details
INFLUXDB_NETLOC = "http://127.0.0.1:8086"
INFLUXDB_NAME = "luftdata"
INFLUXDB_USER = "luftdata"
INFLUXDB_PASSWORD = "hunter2"


def push_latest_measurement(timeseries_url):
    """
    Read official air quality sensor data from the Swedish Sensor
    Observation Service at http://shair.smhi.se/52North/. See README for
    details on how to find the sensor/timeseries url you need.
    """

    try:
        # Read timesearies summary and get the latest value.
        r = requests.get(timeseries_url)
        jdata = r.json()

        # Convert to nanoseconds used in InfluxDB
        ts = int(jdata["lastValue"]["timestamp"])*1000*1000
        value = jdata["lastValue"]["value"]
        stationid = jdata["station"]["id"] 

        # Create linedata format for InfluxDB and post it
        linedata = "official,stationid=%s SDS_P1=%s %s" % (stationid, value, ts)
        print("Sending: %s" % linedata)
        r = requests.post("%s/write?db=%s&u=%s&p=%s" % (INFLUXDB_NETLOC, INFLUXDB_NAME, INFLUXDB_USER, INFLUXDB_PASSWORD), data=linedata)
    except Exception as e:
        print("Error reading/pushing data")
        print(e)

    return

if __name__ == "__main__":
    push_latest_measurement(API_TIMESERIES_URL)
