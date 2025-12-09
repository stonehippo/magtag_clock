import board
import time
import rtc

import ipaddress
import os
import ssl
import wifi
import socketpool
import adafruit_requests

import json

import circuitpython_schedule as schedule

from adafruit_bme680 import Adafruit_BME680_I2C

# use one of the Adafruit RTC modules
# from adafruit_pcf8523.pcf8523 import PCF8523 as rtc_driver
# import adafruit_ds3231 import DS3231 as rtc_driver
from adafruit_ds1307 import DS1307 as rtc_driver

try:
  if board.STEMMA_I2C:
    i2c = board.STEMMA_I2C()
  else:
    i2c = board.I2C()
except AttributeError:
  import busio
  i2c = busio.I2C(board.SCL, board.SDA)

# set up the environment sensor
bme = Adafruit_BME680_I2C(i2c)

# assume that the hardware RTC has already been set to real time
rtc_dev = rtc_driver(i2c)

# Get our username, key and desired timezone
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
aio_username = os.getenv("ADAFRUIT_AIO_USERNAME")
aio_key = os.getenv("ADAFRUIT_AIO_KEY")
timezone = os.getenv("TIMEZONE")

TIME_URL = f"https://io.adafruit.com/api/v2/{aio_username}/integrations/time/struct?x-aio-key={aio_key}&tz={timezone}"

wifi.radio.connect(ssid, password)

def set_local_rtc(rtc, source):
   print("Setting RTC time")
   rtc.datetime = time.struct_time(tuple(source.datetime))

# set the `rtc' module, which will sync `time.localtime()`/`time.time()` as well
r = rtc.RTC()
set_local_rtc(r, rtc_dev)

# get Internet time to set RTC (for drift correction or after poweroff)
def set_time_from_net():
    print("Setting RTC time from net")
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    try:
        nt = json.loads(requests.get(TIME_URL).text)
        rtc_dev.datetime = time.struct_time((nt["year"], nt["mon"], nt["mday"], nt["hour"], nt["min"], nt["sec"], nt["wday"], nt["yday"], nt["isdst"]))
        set_local_rtc(r, rtc_dev)
    except RuntimeError:
        pass

# reset the time at midnight every day to correct for RTC drift
schedule.every().day.at("00:00:00").do(set_time_from_net)

def show_current_time():
   now = r.datetime
   print(f"{now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}")

def show_current_conditions():
   print(f"{bme.temperature:.1f}°C {bme.humidity:.0f}%")

schedule.every().second.do(show_current_time)
schedule.every().minute.at(":00").do(show_current_conditions)

while True:
   schedule.run_pending()
