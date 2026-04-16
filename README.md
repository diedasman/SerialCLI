# SerialCLI

A command-line interface for serial device communication via USB. Easily send and receive data to/from USB devices with real-time monitoring and automatic logging.

## Features

- 🔌 **Serial Communication**: Connect to USB devices and send/receive data through the command line
- 📡 **Real-time Monitor**: Watch live serial data streams from connected devices
- 📋 **Session Logging**: Automatically log all TX/RX data with timestamps
- 🛠️ **Cross-Platform**: Works on Windows, Linux, and macOS
- 🎯 **Simple Commands**: Easy-to-use interactive CLI with help menu

```


  /$$$$$$                      /$$           /$$  /$$$$$$  /$$       /$$$$$$
 /$$__  $$                    |__/          | $$ /$$__  $$| $$      |_  $$_/
| $$  \__/  /$$$$$$   /$$$$$$  /$$  /$$$$$$ | $$| $$  \__/| $$        | $$
|  $$$$$$  /$$__  $$ /$$__  $$| $$ |____  $$| $$| $$      | $$        | $$
 \____  $$| $$$$$$$$| $$  \__/| $$  /$$$$$$$| $$| $$      | $$        | $$
 /$$  \ $$| $$_____/| $$      | $$ /$$__  $$| $$| $$    $$| $$        | $$
|  $$$$$$/|  $$$$$$$| $$      | $$|  $$$$$$$| $$|  $$$$$$/| $$$$$$$$ /$$$$$$
 \______/  \_______/|__/      |__/ \_______/|__/ \______/ |________/|______/



╭───────────────────────────────────────────────────────── SerialCLI - Serial Device Communication Tool ──────────────────────────────────────────────────────╮
│  TIPS:                                                                                                                                                      │
│ • Type 'help' for a list of available commands                                                                                                              │
│ • Use 'connect --list' to see available serial ports                                                                                                        │
│ • Use 'status' to check connection status                                                                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Type 'help' for available commands or 'exit' to quit                                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation (All Platforms)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SerialCLI.git
   cd SerialCLI
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```
```

## Usage

### Starting SerialCLI

After installation, run from anywhere in your terminal:

```bash
SerialCLI
```

This displays the welcome screen and launches the interactive CLI.

### Basic Commands

```
help                       - Display help menu
status                     - Show connection status
exit                       - Exit the application
```

### Connection Commands

```
# List available serial ports
connect --list

# Connect to a port with default settings (9600 baud)
connect -p COM3

# Connect with custom settings
connect -p COM3 -b 115200 -dat 8 -par N -stop 1 -t 1.0

# Disconnect
disconnect
```

### Monitor & Logging

```
# Start real-time serial monitor (Ctrl+C to exit)
monitor

# Enable logging to file (creates directory if needed)
logging enable logs/session.txt

# Disable logging
logging disable
```

### Manual Communication

```
# Send data to device
send "hello\r\n"

# Read available data
read
```

# Send data to device
send "hello\r\n"

# Read available data
read
```

## Advanced Features

### Serial Monitor

Real-time data stream visualization:

```bash
SerialCLI> connect -p COM3
SerialCLI> monitor
# [Watch device data in real-time, press Ctrl+C to exit]
```

See [MONITOR_AND_LOGGING.md](MONITOR_AND_LOGGING.md) for detailed monitor usage.

### File Logging

Automatic session recording with timestamps:

```bash
SerialCLI> logging enable logs/session.txt
# [All TX/RX data is now logged]
SerialCLI> logging disable
```

Log entries include:
```
[10:30:45.123] CONNECTED: COM3 @ 9600 baud
[10:30:46.456] TX: 'AT+RST\r\n'
[10:30:47.789] RX: 'OK\r\n'
```

See [MONITOR_AND_LOGGING.md](MONITOR_AND_LOGGING.md) for advanced logging scenarios.



### config.json

General application settings (for future use).

```json
{
    "SETTINGS": {
        "PORT": "",
        "BAUD": "",
        "TERMINATION": {
            "FLOW_CONTROL": "DISABLED",
            "DATA_BITS": "",
            "PARITY": "",
            "STOP_BITS": ""
        },
        "TIMEOUT": "",
        "LOGGING": {
            "ENABLED": false,
            "FILE_PATH": ""
        }
    }
}
```

## Project Structure

```
SerialCLI/
├── __main__.py           # Application entry point
├── cli.py               # Main CLI interface and command handling
├── serial_core.py       # Serial communication backend
├── setup.py             # Installation/packaging configuration
├── config.json          # Application configuration
├── logo.txt             # ASCII art logo
├── README.md            # This file
└── examples/
    └── script.txt       # Example scripts
```

## How It Works

### Serial Communication Flow

1. User runs `SerialCLI` command
2. Application displays logo and enters interactive mode
3. User enters commands (connect, send, etc.)
4. Commands are parsed and executed by the CLI
5. Serial data is handled by `serial_core.SerialCommunicator`



## Module Documentation

### serial_core.py

Handles all serial port operations:

- `SerialCommunicator.connect()` - Establish serial connection
- `SerialCommunicator.disconnect()` - Close connection
- `SerialCommunicator.send()` - Send data
- `SerialCommunicator.receive()` - Read data
- `SerialCommunicator.read_until()` - Read until expected string
- `SerialCommunicator.list_ports()` - List available ports

### cli.py

Provides the interactive interface:

- `SerialCLI.process_command()` - Parse and execute user commands
- `SerialCLI.parse_connect_command()` - Handle connection commands
- `SerialCLI.run()` - Main CLI loop

## Future Enhancements

- User-defined command scripts
- Data logging and session recording
- GUI/TUI interface option
- Configuration profiles
- Real-time data visualization
- Device firmware update support

## Troubleshooting

### Port Not Found
- Ensure USB device is connected
- Run `connect --list` to see available ports
- Check device drivers are installed

### Connection Fails
- Verify correct port name
- Check baud rate matches device settings
- Confirm USB cable is working

### Import Errors
- Reinstall the package: `pip install -e .`
- Ensure all dependencies are installed: `pip install pyserial`

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details

## Changelog

### Version 0.1.0 (Initial Release)
- ✓ Basic serial communication
- ✓ Interactive CLI interface
- ✓ Cross-platform installation
- ✓ Command-line help system
