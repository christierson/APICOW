# A MicroPython API for the Raspberry Pi Pico W 

This project serves as a web-based gpio API for the raspberry pi pico W, written in MicroPython. To use this, you'll need to flash your Pico with MicroPython. When the Pico has MicroPython, it's just a matter uploading the files in [/pico](pico) to your Pico and then running [interface.py](interface.py) on a host computer to start controling the pico over your home network.

## Configuration
Before you upload the files, you will want to modify them to fit your setup. Read the following to correctly set everything up.

- __Secrets__: This API only works through a WiFi connection, so you'll need to set it up to connect to your network. In [/pico/api.py](pico/api.py), `SSID` and `PASSWORD` get imported from `secrets.py`. This file is gitignored so you'll have to create it yourself. Example:
```python
# secrets.py
SSID = "YOUR WIFI SSID"
PASSWORD = "YOUR WIFI PASSWORD"
```

- __Status LED__: I have set up my Pico such that I have a "status LED" soldered to `gp0`. This status LED pin is hard coded in [/pico/board.py](pico/board.py) _and_ [/pico/main.py](/pico/main.py), so if you want a different pin (or no status LED - not recommended!), you'll need to change that.

- __Components__: In [/pico/component.py](pico/component.py) you'll find the class `Component`. This is an abstraction to whatever you're going to connect to the pins. I have implemented the three basic pin functionalities; `in` (reading signal from e.g. a potentiometer), `out` (power 3.3V components e.g an LED) and `pwm` (controlling PWM signals for e.g dimming an LED). In addition to this, I have implemented the subclass for a specific sensor - the `DHT22`. I needed this sensor for a project, so if you have additional components, I would recommend writing your own `Component` implementations for them.

- __The interface__: The file [/interface.py](interface.py) is one of the files that don't get uploaded to the pico. It is the interface for the picos API and is meant to be run on the host computer. So the last thing you'll might want to modify is the `url`. In my case, my pico got `IP: 192.168.0.102` but you'll have to find the ip of your Pico and replace it.

Depending on your host platform and what you have installed there are different ways of uploading these files to the Pico. I created the quality-of-life script [upload.py](upload.py) which works for my machine. You'll need to find a way that works for you.

## Usage
When you have completed the above steps and uploaded the modified files, you can start sending commands to your Pico wirelessly. Just give the pico a power source and you will see the status LED blink. The LED blinks for each step in the [/pico/main.py](/pico/main.py) and it should blink three times in total:

- __1st blink__: The Pico has power and is running [/pico/main.py](/pico/main.py)
- __2nd blink__: The `Board` instance has been created successfully. 
- __3rd blink__: The `API` for the `Board` has been initiated and is connected to your WiFi.

When you have seen those three blinks (can take a few seconds), you should be able to communicate to the Pico using the [/interface.py](interface.py) script. Simply enter the Python REPL with the file loaded: `python -i interface.py`. When you do this the script will attempt to find the Pico and connect to it. If it can do that successfully it will ask the board for its current setup and print it. If it's not able to find the Pico the script will fail.

Once you're in the REPL you can use the functions to configure the pins. Say you have anothe LED connected to `gp15`, in that case you can do `set_pin(15, "led", "out")`. When the pico replies to this call with a success message, you can do `write(15, 1)` to turn on the LED.

When you are happy with how the Picos GPIO is set up, you can call `save_default()` to make the configuration persistent. If you don't set a default board, you will end up with an empty board after restarts. 

With the above setup you will only be able to have the LED on or off. If you want to be able to dim it, do this `set_pin(15, "led", "pwm")` and then `write(15, 0.5)` for example. I recommend just reading through the interface.py file, it's pretty self-explanatory.

---
### About the project

I developed this for an automated plant-watering-system. The idea is to have a host computer (in my case a normal raspberry pi 4) where the actual functionality for the project is. In my case, the host computer sends requests, reading sensors connected to the pico, depending on the values of the different sensors, more API requests are sent to enable or disable the water pumps. So the Raspberry Pi 4 has a script that determines the behavior of the Pico. That being said, this project is written to be generic and to work with any kind of project involving the Pico W.

I don't have too much time to work on this project which is why it is all a bit janky and DIY. My plan is to make the interface and API a bit more user friendly as well as adding "routines" such that schedules can be automated without maunal API calls.
