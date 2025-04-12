#!/usr/bin/env python3
"""

baudbuster.py

A Python script that brute-forces common UART configuration parameters to
automatically discover the correct serial port settings for a given device.
Specifically, it tests:

  - A range of standard baud rates (from 50 up to 4,000,000),
  - Two common data bit sizes (7 or 8 bits),
  - Three parity modes (none, odd, even),
  - One or two stop bits.

By default, it attempts to open "/dev/ttyUSB0" unless another device path
is specified. The script can optionally send a command (such as an AT command)
to the device after each parameter set is opened, in case the device only
transmits data in response to a prompt.

Usage:
  ./baudbuster.py [device] [command]

Examples:
  1) No arguments:
       ./baudbuster.py
     Tests all UART settings on /dev/ttyUSB0 without sending a command.

  2) Specify a device:
       ./baudbuster.py /dev/ttyS0
     Tests all UART settings on /dev/ttyS0 without sending a command.

  3) Specify a device & command:
       ./baudbuster.py /dev/ttyACM0 "ATI\r"
     Tests all UART settings on /dev/ttyACM0 while sending "ATI\r" for each
     parameter combination to provoke a response.

If the script finds a working configuration (i.e., it receives meaningful or
legible data from the device), it prints the response. Adjust timeouts,
sleep durations, or the number of bytes read according to your device’s
behavior. If the script doesn’t detect any valid response, confirm that your
device actually outputs data (either automatically or upon receiving the
command you’re sending) and that you’re using the correct port.

Note:
  - If the device is very slow to respond, increase READ_TIMEOUT or add a
    longer sleep after sending the command.
  - If you expect the device to send more than 100 bytes at once, increase
    BYTES_TO_READ.
  - If the device requires a newline plus carriage return, use something
    like "\\r\\n" in the command string.

"""

import sys
import serial
import time
import os
import pycolors

from pycolors import fore, back, style, init
from loaders import ProgressLoader

# Typical baud rates to test
SERIAL_BAUDRATES = [
    50, 75, 110, 134, 150, 200, 300, 600,
    1200, 1800, 2400, 4800, 9600, 19200,
    38400, 57600, 115200, 230400, 460800,
    500000, 576000, 921600, 1000000,
    1152000, 1500000, 2000000, 2500000,
    3000000, 3500000, 4000000
]

# Byte sizes (7 or 8 bits)
BYTE_SIZES = {
    7: serial.SEVENBITS,
    8: serial.EIGHTBITS
}

# Parity options (only odd/even as requested)
PARITY_OPTIONS = {
    'N': serial.PARITY_NONE,
    'O': serial.PARITY_ODD,
    'E': serial.PARITY_EVEN
}

# Stop bits (1 or 2)
STOPBITS_OPTIONS = {
    1: serial.STOPBITS_ONE,
    2: serial.STOPBITS_TWO
}

READ_TIMEOUT = 1.0  # seconds
BYTES_TO_READ = 100

def main(device, send_command=None):
    iterations = 0

    for baud in SERIAL_BAUDRATES:
        for bits_label, bits_value in BYTE_SIZES.items():
            for parity_label, parity_value in PARITY_OPTIONS.items():
                for stop_label, stop_value in STOPBITS_OPTIONS.items():
                    iterations = iterations + 1

    print(f"{back.BLACK}{fore.LCYAN}>>> {fore.LGREEN}Brute forcing baud rates...{style.RESET}")
    loader = ProgressLoader(total=iterations)
    current_iteration = 0

    for baud in SERIAL_BAUDRATES:
        for bits_label, bits_value in BYTE_SIZES.items():
            for parity_label, parity_value in PARITY_OPTIONS.items():
                for stop_label, stop_value in STOPBITS_OPTIONS.items():
                    current_iteration = current_iteration + 1
                    loader.progress(current_iteration)
                    try:
                        ser = serial.Serial(
                            port=device,
                            baudrate=baud,
                            bytesize=bits_value,
                            parity=parity_value,
                            stopbits=stop_value,
                            timeout=READ_TIMEOUT
                        )

                        time.sleep(0.5)

                        if send_command is not None:
                            ser.write(send_command.encode())
                            time.sleep(0.2)

                        data = ser.read(BYTES_TO_READ)
                        ser.close()

                        if data:
                            # Attempt to decode as ASCII for readability
                            try:
                                data_str = data.decode('ascii', errors='replace')
                            except:
                                data_str = repr(data)
                            loader.progress(iterations)
                            print(f"{back.BLACK}{fore.LCYAN}>>> {fore.LGREEN}Tried baud={baud}, data_bits={bits_label}, parity={parity_label}, stop_bits={stop_label} ... got {len(data)} bytes: {data_str}{style.RESET}")
                            sys.exit(0)
                    except Exception as e:
                            pass

if __name__ == "__main__":
    device_arg = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
    command_arg = sys.argv[2] if len(sys.argv) > 2 else None

    init.init()

    if not os.path.exists(device_arg):
        print(f"{back.BLACK}{fore.LCYAN}>>> {fore.LRED}Error: Device '{device_arg}' not found.{style.RESET}")
        sys.exit(1)

    main(device_arg, command_arg)
