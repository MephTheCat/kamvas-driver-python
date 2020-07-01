# kamvas-driver-python
A userspace evdev driver for Huion's Kamvas 13 screen tablet.

This project implements a userspace driver for Huion's Kamvas 13 screen tablet.


# Motivation
When I bought my Kamvas 13, I was unable to use it with Linux.  I was unsuccessful in using the DIGImend drivers.  I had found another Python based evdev driver that *worked*, but didn't work the way I wanted it to.  As such, I wrote my own and I hope that it helps others to use their tablets, as well.


# Things to know
The driver was tested with a Kamvas 13.  I have no reason to believe that it will not work with other Huion tablets, however, this is unconfirmed as I only own the one tablet.

The driver will exit gracefully if the tablet is unplugged.  However, there is a chance that, upon plugging it back in, the driver will not work correctly despite having detected the device.  I believe this problem has been mitigated, however, if it happens, please open an issue and I will investigate.


# Dependencies
This driver relies on the following packages:  

- python3-usb
- python3-libevdev

Debian users may use the following:  
`sudo apt install python3-libevdev python3-usb`


An additional file at `/usr/share/X11/xorg.conf.d/50-tablet.conf` may also be necessary.
```
Section "InputClass"
        Identifier "evdev tablet catchall"
        MatchIsTablet "on"
        MatchDevicePath "/dev/input/event*"
        Driver "evdev"
EndSection
```

# How to manually configure the driver for your tablet
The file, `config.py`, contains the configuation for your tablet.  It supports multiple tablet profiles.  Simply create another dictionary with the requisite keys and populate as necessary.  Be sure to reassign the `working_tablet` variable to your new dictionary.
<br/>

| Key | Type Expected | Description |
| :-- | :------------ | :---------- |
| pen_name | String | The name of the Evdev device to be created. |
| vendor | Integer | The vendor ID of the USB device corresponding to your tablet, check `lsusb`. |
| product | Integer | The product ID of the USB device corresponding to your tablet, check `lsusb`. |
| use_xrandr | Boolean | Whether or not you want to use XRandR to automatically map the tablet to a monitor. |
| mapped_display | String | The name of the display (as returned by XRandR) of the monitor onto which you wish to map your tablet.|
| tablet_res | Tuple | The pixel resolution of the display you are mapping the tablet onto. |
| tablet_pre_offset | Tuple | An adjustment value added to the raw pen coordinates before conversion (leave at (0, 0)). |
| tablet_post_offset | Tuple | An adjustment value added to the pixel coordinates after conversion (leave at (0, 0)). |
| tablet_max | Tuple | For calibration.  The maximum raw coordinate value for each dimension. |
| tablet_min | Tuple | The minimum raw coordinate value for each dimension. |
| tablet_screen_pos | Tuple | The offset of the tablet in virtual screen space. |
| tablet_pen_res | Integer | The DPI of the pen.  Currently unused. |
| tablet_max_pressure | Integer | The highest pressure value the pen will produce. |
| pen_min_tilt | Integer | The minimum angle for pen tilt. |
| pen_max_tilt | Integer | The maximum angle for pen tilt. |
| virtual_screen_res | Tuple | The total resolution of the virtual screen. |
| face_buttons | List of Tuples or None | The keys pressed/released when a particular face button is pressed, uses Evdev constants |
| driver_update_sec | Float | The driver's update interval as 1.0/(updates per second) |
| averaging_length | Integer | The length of the history buffer for pen position average.  Set to 1 to disable. |
| rotation | String | 'normal', 'left', 'right', 'inverted'.  Tablet orientation.  Currently unused. |
| stylus_btn_swap | Boolean | Swap the functions of the pen stylus's buttons. |


# How to (mostly) automatically configure your tablet
The configuration file has the key `use_xrandr` which, when set to true, will automatically populate the values of `tablet_res`, `tablet_screen_pos`, and `virtual_screen_res` based on the values it reads back from a call to `xrandr`.  This will probably be good for the overwhelming majority of users who want to map their screen tablet's area to the screen tablet, itself or map it to the entirety of another display.

1. Please use `arandr` or your desktop environment's display settings to position your screen tablet as you wish.  Make note of the name of display that corresponds to your screen tablet.
2. Change the value of `mapped_display` in the configuration file to that display's name (ex. DisplayPort-0, HDMI-1, etc).
3. Start the driver and ensure that your tablet works as intended.


# Running the driver
Please plug in your tablet and start the driver.  The driver must be run under `sudo`, as `sudo python3 kamvas.py`


# Next steps
The next steps in the project will be to implement rotation, improve code documentation, and to, at some point, reimplement this in C and/or develop a kernel driver.