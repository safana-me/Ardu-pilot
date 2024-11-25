# VSPeak Modell flow meter Driver

This driver implements support for the VSPeak Modell flow meter sensor.

https://www.vspeak-modell.de/en/flow-meter

# Parameters

The script used the following parameters:

## VSPF_ENABLE

Setting this to 1 enables the driver.

# Setup

First of all, calibrate and configure the flow meter according to the
manufacturer instructions. Set your configuration with the `FLOW.txt` file,
placed in the SD card in the sensor itself.

Once this is done, perform the following steps.

1. Place this script in the "scripts" directory of the autopilot.
2. Connect the sensor to a serial port (for now referred to as `SERIAL*`)
3. Enable the scripting engine via `SCR_ENABLE`.
4. Set the baud rate to 19200 with `SERIAL*_BAUD = 19`.
5. Set port protocol to scripting with `SERIAL*_PROTOCOL = 28`.
6. Set the EFI type to scripting with `EFI_TYPE = 7`.
7. Set a battery monitor to EFI. For example, to set the 2nd battery monitor
    use `BATT2_MONITOR = 27`.
8. Enable the script itself with `VSPF_ENABLE=1`.

# Operation

Once everything is configured correctly, the corresponding battery monitor
will display in the corresponding `BATTERY_STATUS` MAVLink message:
 - The current fuel flow in cl/hr (centiliters per hour) in the `current_battery` field.
 - The current fuel already consumed in ml (milliliters) in the `current_consumed` field.
