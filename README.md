# pico-calendar
Subscribe to a iCal feed and show events on your Raspberry Pi Pico W with a 1.14 Inch Waveshare Display

## Prerequisites & Installation

1. Get a [Raspberry Pi Pico W](https://www.raspberrypi.com/news/raspberry-pi-pico-w-your-6-iot-platform/) and a [Waveshare 1.14 Inch Display](https://www.waveshare.com/wiki/Pico-LCD-1.14). 
   
   > Connect them both correctly (I needed to solder the pins to the PI, otherwise, it was not possible to establish a stable connection).

2. Press the *BOOTSEL* button and connect it via USB. It should appear in your Explorer/Finder as USB Drive called RPI-RP2
3. Download the latest MicroPython UF2 File for Raspberry Pi Pico W from the [official site](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
4. Copy the uf2 file to the RPI-RP2 Drive 
5. The Pico should disconnect and reboot. 
6. Unplug + Plug the USB Cable (without pressing *BOOTSEL* again)
7. Download and install [Thonny](https://thonny.org/) for an easy Python development
8. Clone the repository into a directory of your choice
9. Open the directory with Thonny
10. Click the button at the bottom right of Thonny and select "Micropython (Raspberry Pi Pico)" (For a more detailed instruction on how to get Thonny up and running, [this helped me a lot](https://desertbot.io/blog/raspberry-pi-pico-setup-mac)) - maybe play around a bit before proceeding.

## Copy all necessary files to the Pico

1. Copy the file `secrets.py.dist` to `secrets.py` and modify the variables `SSID` `PASSWORD` and `COUNTRY` to your needs
2. Rightclick on these files and select "Upload to /" or "Upload to Raspberry Pi Pico"
   - `secrets.py` 
   - `wifi.py`
   - `LCDScreen.py`
3. Now you should open `main.py` and click the green "Play" Button in the nav-bar. 

You should see something printed in the console and the screen should show something :)
