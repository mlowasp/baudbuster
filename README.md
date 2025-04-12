# BaudBuster

![BaudBuster](https://i.imgur.com/oDa7jQy.png)

**BaudBuster** is a Python script that systematically tests UART (serial) port
configurations to help you discover a device’s correct baud rate, data bits,
parity, and stop bits. This can be invaluable when working with undocumented
hardware or when you need to determine the serial communication parameters
of a device.

## Features
- Brute-forces a range of common baud rates (50 up to 4,000,000).
- Tests 7-bit or 8-bit data lengths.
- Tries none, odd, or even parity modes.
- Tests 1-stop or 2-stop bits.
- Optional command sending after each parameter combination (e.g., an AT command
  to elicit a response).
- Prints out any data received, so you can identify successful communication
  settings.

## Getting Started

### Prerequisites
- Python 3.x
- pyloaders
- [PySerial](https://pypi.org/project/pyserial/)
- [pycoloredprompt](https://github.com/onlygiogi/pycolors)

Install PySerial and pycoloredprompt via pip:
```bash
pip install pyserial
pip install pycoloredprompt
pip install pyloaders
```

### Installation
1. Clone this repository or download the `baudbuster.py` script.
2. Make `baudbuster.py` executable:
```bash
chmod +x baudbuster.py
```

## Usage

```bash
./baudbuster.py [device] [command]
```

- **device** (optional): The serial port to test. Defaults to `/dev/ttyUSB0`
  if not specified.
- **command** (optional): A command string (e.g., `"ATI\r"`) to send after
  each connection attempt to provoke a response.

### Examples

1. **No arguments**
   ```bash
   ./baudbuster.py
   ```
   - Tests all UART settings on `/dev/ttyUSB0`.
   - Sends **no** command to the device.

2. **Specify a device**
   ```bash
   ./baudbuster.py /dev/ttyS0
   ```
   - Tests all UART settings on `/dev/ttyS0`.
   - No command sent.

3. **Specify a device & command**
   ```bash
   ./baudbuster.py /dev/ttyACM0 "ATI\r"
   ```
   - Tests all UART settings on `/dev/ttyACM0`.
   - Sends the `ATI\r` command for each parameter combination.

### Adjusting Timeouts and Read Length
- **READ_TIMEOUT**: Increase if your device responds slowly.
- **BYTES_TO_READ**: Increase if your device sends more than 100 bytes in a single response.
- **Sleep Durations**: The script includes short sleeps (`time.sleep(...)`) to
  allow the device to settle or respond. Increase these if needed.

## How It Works
1. **Baud Rates**: Iterates over a list of common speeds, from 50 to 4,000,000.
2. **Data Bits**: Tests 7-bit and 8-bit modes.
3. **Parity**: Tests none (`N`), odd (`O`), and even (`E`) parity.
4. **Stop Bits**: Tests 1 or 2 stop bits.
5. **(Optional) Command**: If you specify a command, `baudbuster.py` sends it
   after opening each configuration.
6. **Read**: Reads up to 100 bytes (by default) from the device. If data is
   received, it attempts ASCII decoding. Otherwise, it displays a raw representation.

## Common Use Cases
- **Unknown/Undocumented Hardware**: You have a device that emits data but you’re
  unsure of its communication parameters.
- **One-Off Debugging**: You suspect the device might be using a less common baud
  rate or parity setting.
- **Reverse Engineering**: Quickly iterate over serial settings to find which
  combination yields meaningful output.

## Contributing
Contributions, bug reports, and feature requests are welcome! Feel free to open
issues or pull requests on the [GitHub repository](https://github.com/mlowasp/baudbuster).

## License
This project is licensed under the [MIT License](LICENSE). See the `LICENSE`
file for details.

---

**Happy UART hacking!** If you find BaudBuster useful, feel free to star the repo
and share your feedback.
