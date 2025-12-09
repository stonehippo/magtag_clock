# MagTag Alarm Clock

An alarm clock with an e-paper display and basic environmental data.

# Hardware
 
I build this clock from off-the-shelf modules from Adafruit.

- [Adafruit MagTag](https://www.adafruit.com/product/4800)
- [Adafruit BME668 Temperature, Pressue, Humidity, and Gas Sensor](https://www.adafruit.com/product/5046) - environmental sensor. You can swap in the [BME680](https://www.adafruit.com/product/3660) with no code changes if you want to save a buck.
- [Adafruit DS1037 RTC](https://www.adafruit.com/product/3296) - you can swap in the [PCF8523](https://www.adafruit.com/product/5189) or [DS3231](https://www.adafruit.com/product/5188); unlike the DS1307, they both run at 3 volts, and the DS3231 is very precise. I used the DS1307 because I happened to have a couple around, but if I was buying new parts, I'd probably go with the PCF8523.
- [Adafruit QT 3V to 5V Level Booster Breakout](https://www.adafruit.com/product/5649) - only needed if using the DS1307, which requires 5 volts. The other RTCs can be used without this module.

You will also need some [STEMMA QT cables](https://www.adafruit.com/product/4399).I used mainly 50mm cables to keep the length down. I also adapted the DS1307 to STEMMA QT by cutting the end off of one of the cables and soldering it to the pins on the module.

## Install Dependencies

```
circup install adafruit_ds1307 adafruit_bme680 circuitpython_schedule
```