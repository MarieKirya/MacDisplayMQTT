MacDisplayMQTT
==============

Introduction
------------

This python applet handles turning on and off displays over MQTT. This was made for the sake of controlling displays from Home Assistant's MQTT integrations.

Inspiration
-----------

* Code based on Jerrkawz/GarageQTPi
* Idea based on christopherwk210/homebridge-mac-display

Installation
------------

1. Clone this repository
2. Install requirements with pip `pip install -r requirements.txt`. (To be cleaner you could also use a venv)
3. Add your MQTT settings to config.yaml and test functionality with `python main.py`
4. Take a look at the example launch daemon plist and modify the path to python, main.py, and PATH variables
5. Once done move it into you launch daemon folder in your user folder `~/Library/LaunchAgents/`
6. You can then manually start it with `launchctl load ~/Library/LaunchAgents/io.kiryanova.MacDisplayMQTT.plist`
