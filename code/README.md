# Fridge Monitor Application

The Fridge Monitor application is written in Python 3 and supports the hardware elements of the Raspberry Pi Zero Thermocouple pHat which can measure up to 3 thermocouple temperatures. The main function is to monitor the temperatures inside a refridgerator/freezer. These temperatures are reported at a configurable rate. If the temperatures rise above a configurable set point the application will set an alarm. The application is discoverable by [Home Assistant](https://home-assistant.io/), an open-source home automation platform also running Python 3. [MQTT](http://mqtt.org/), a machine-to-machine (M2M)/"Internet of Things" connectivity protocol, is the basis of communication with Home Assistant.

## Configuration Notes

All settings for this application are in the '[fridgemonitor.conf](fridgemonitor.conf)'. This is where you point to the correct MQTT broker and configure how the temperature sensors work. There are a few settings of note here. Discovery_Enabled = false will prevent Home Assistant from automatically discovering the Fridge Monitor.

## Home Assistant Notes

When Discovery is enabled Home Assistant will automatically pick up the Alarm Disable switch, Alarm binary_sensor, RSSI sensor, four temperature sensors, and three door sensors. The is a DS18S20 1-Wire Thermometer on the board and three thermocouple inputs for measuring temperature remotely with thermocouple wire.

If you don't want to use discovery here is the configuration of the Fridge Monitor in Home Assistant. Note the 'studio_fridge_monitor' you see in the example yaml is the Node_ID which is specified in the 'fridgemonitor.conf' file.

```yaml
switch:
  - platform: mqtt
    sensors:
      # This switch provides a means to turn off both the audible alert and alarm boolean_sensor
      #   This switch will automatically turn back OFF at 6PM every day.
      name: "Studio Fridge Monitor Alert Disable"
        state_topic: "homeassistant/switch/studio_fridge_monitor/alert_disable/state"
        command_topic: "homeassistant/switch/studio_fridge_monitor/alert_disable/set"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        qos: 1
# The following sensors are updated at Sensor_Publish_Rate specified in the frigdemonitor.conf file
sensor:
  - platform: mqtt
    sensors:
      # WiFi Received Signal Strength Indicator (RSSI)
      name: "Studio Fridge Monitor RSSI"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/rssi/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: 'dBm'
      # Temperature measured by the DS18S20 Sensor (1 minute average)
      name: "Studio Fridge Monitor Temperature"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/temperature/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: '°C'
      # Temperature measured by the MAX31850K Thermocouple Sensor (TC1) (1 minute average)
      name: "Studio Fridge Temperature"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC1_temperature/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: '°C'
      # Temperature measured by the MAX31850K Thermocouple Sensor (TC2) (1 minute average)
      # if TC_Count in configuration file is set to 1 then this sensor does not exist
      name: "Studio Freezer Temperature"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC2_temperature/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: '°C'
      # Temperature measured by the MAX31850K Thermocouple Sensor (TC3) (1 minute average)
      # if TC_Count in configuration file is set to 2 or 1 then this sensor does not exist
      name: "Studio Fridge Compressor Temperature"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC3_temperature/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: '°C'
      # Temperature measured by the MAX31850K Thermocouple Sensor (TC1) (24 hour average)
      name: "Studio Fridge Average"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC1_average/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: '°C/min'
      # Temperature measured by the MAX31850K Thermocouple Sensor (TC2) (24 hour average)
      # if TC_Count in configuration file is set to 1 then this sensor does not exist
      name: "Studio Freezer Average"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC2_average/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: '°C/min'
      # Temperature measured by the MAX31850K Thermocouple Sensor (TC3) (24 hour average)
      # if TC_Count in configuration file is set to 2 or 1 then this sensor does not exist
      name: "Studio Fridge Compressor Average"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC3_average/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        unit_of_measurement: '°C/min'
binary_sensor:
  - platform: mqtt
    sensors:
      # When active the Fridge Monitor has detected an over temperature condition
      #   on any thermocouple sensor
      name: "Studio Fridge Monitor Alarm"
        state_topic: "homeassistant/binary_sensor/studio_fridge_monitor/alarm/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/status"
        device_class: "heat"
      # Analysis of TC1 to determine if the door is open
      name: "Studio Fridge Door"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC1_door/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        device_class: "door"
      # Analysis of TC2 to determine if the door is open
      # if TC_Count in configuration file is set to 1 then this sensor does not exist
      name: "Studio Freezer Door"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC2_door/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        device_class: "door"
      # Analysis of TC3 to determine if the door is open
      #  this doesn't make sense for compressor temperature monitor
      # if TC_Count in configuration file is set to 2 or 1 then this sensor does not exist
      name: "Studio Fridge Compressor Door"
        state_topic: "homeassistant/sensor/studio_fridge_monitor/TC3_door/state"
        availability_topic: "homeassistant/switch/studio_fridge_monitor/avail"
        device_class: "door"
```

## Raspberry Pi Setup

It is assumed that you already followed the instructions in the Raspberry Pi Setup section of the main project [README file](../README.md). If you have not, please do so now before continuing. Be sure to edit the 'fridgemonitor.conf' file to support your configuration. Test the software by executing the following commands. Note if you are not using the standard `pi` user you will have to edit the commands by replacing `/home/pi` with your user's home directory.

```text
cd /home/pi/RPi-pHat-Thermocouple/code/
chmod 755 fridgemonitor.py
./fridgemonitor.py
```

If you see no errors you should be able to see one switch, one binary_sensor, and four sensors in Home Assistant. Configuring Home Assistant is a bit of a stretch for this guide but here are a couple of hints.

* "Fridge Monitor: Failed to load state file 'fridgemonitor.json'." means there is no previous state for the light. This is perfectly normal when the code is run for the first time.
* Make sure you have MQTT installed. If you use HASS.IO goto the HASS.IO configuration and install the Mosquitto Broker.
* Make sure you have MQTT discovery enabled. See [MQTT Discovery](https://home-assistant.io/docs/mqtt/discovery/).
* Make sure your MQTT discovery prefix matches the Discovery_Prefix in your Fridge Monitor configuration file.

Installing a MQTT server is easy if you are running Hass.io, just look for the Mosquitto Broker in the Add_On Store.

## Systemd run at boot

If you are not using the standard `pi` user you will also have to edit the `fridgemonitor.service` file so that links point to the correct directory.

Execute the following commands to install Fridge Monitor as a systemd service to run on startup.

```text
cd /home/pi/RPi-pHat-Thermocouple/code
sudo cp fridgemonitor.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/fridgemonitor.service
sudo systemctl enable fridgemonitor.service
sudo systemctl start fridgemonitor.service
```

## Notes

* The Raspberry Pi should be placed on the outside of the refridgerator/freezer and thermocouple wire should be run inside to measure the temperatures.

* The pHat seems to have some infrequent noise in the readings. Thermocouples are also good at picking up noise so the software trys to eliminate noisy readings. If a thermocouple reading is greater than ±3°C away from last reading the sample will be thrown out. It will do this up to 3 times in a row before allowing the 4th out of bounds sample to pass through.  

* All temperature sensors are sampled every 5 seconds. These samples are averaged every minute. These 1 minute averages are keep for 24 hours to compute an 24 hour average. The 1 minute samples are saved to disk so power interruption or reboot will prevent the complete loss of data for the 24 hour average.

* The door sensors use how fast temperature rises on the 1 minute averages to detect when a door is open. This is reasonable for normal operation but there are problems with this approach. For instance, a quick open and close might be missed especially if the compressor is on and the temperature is falling. If the door is left open eventually the rise in temperature will level out and the door will be recognized as closed.

## Acknowledgments

The following python libraries are required.

* [Eclipse Paho™ MQTT Python Client](https://github.com/eclipse/paho.mqtt.python)
* [Python3 w1thermsensor](https://github.com/timofurrer/w1thermsensor)
* [Adafruit Python GPIO](https://github.com/adafruit/Adafruit_Python_GPIO)

The following code came from Github

* [W1ThermSensor](https://github.com/timofurrer/w1thermsensor/blob/master/w1thermsensor/core.py)

The following code was pulled from the Internet

* [timer.py](https://github.com/jalmeroth/homie-python/blob/master/homie/timer.py)
