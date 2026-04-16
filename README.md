# SerialCLI

A command-line interface for serial device communication via USB. Easily send and receive data to/from USB devices with scripted test sequences, real-time monitoring, and automatic logging.

## Features

- 🔌 **Serial Communication**: Connect to USB devices and send/receive data through the command line
- 📡 **Real-time Monitor**: Watch live serial data streams from connected devices
- 📝 **JSON-Driven Testing**: Define test sequences in `dev.json` for automated device testing
- 📋 **Session Logging**: Automatically log all TX/RX data with timestamps
- 🧪 **Developer Mode**: Built-in test runner with support for multiple test scenarios and trace extraction
- 🛠️ **Cross-Platform**: Works on Windows, Linux, and macOS
- 🎯 **Simple Commands**: Easy-to-use interactive CLI with help menu

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Windows

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SerialCLI.git
   cd SerialCLI
   ```

2. Run the installation script as Administrator:
   ```bash
   install.bat
   ```

### Linux / macOS

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SerialCLI.git
   cd SerialCLI
   ```

2. Run the installation script:
   ```bash
   bash install.sh
   ```

### Manual Installation (All Platforms)

```bash
# Navigate to the project directory
cd SerialCLI

# Install the package in development mode
pip install -e .
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

# Run a specific test once
dev --run VERIFICATION

# Run a test 5 times with 1000ms delay between runs
dev --run VERIFICATION -c 5 -t 1000

# Run all tests
dev --run-all

# Run all tests with custom delay
dev --run-all -t 2000
```

### Manual Communication

```
# Send data to device
send "hello\r\n"

# Read available data
read
```

### Developer Mode

```
# Enable dev mode with the developer key
dev devvy

# List all available tests
dev --list

# Run a specific test once
dev --run VERIFICATION

# Run a test 5 times with 1000ms delay between runs
dev --run VERIFICATION -c 5 -t 1000

# Run all tests
dev --run-all

# Run all tests with custom delay
dev --run-all -t 2000
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

### Trace Extraction

The TRACECATCH test automatically extracts and logs trace data from device output, supporting multiple trace patterns with configurable delimiters.

### dev.json

Defines test sequences and developer settings.

```json
{
    "DEV_KEY": "devvy",
    "COMMANDS": {
        "wake": "wakeup",
        "reset": "reset"
    },
    "TESTS": [
        {
            "NAME": "VERIFICATION",
            "DESCRIPTION": "Verification Checks",
            "SEQUENCE": [
                {
                    "TX": "+++",
                    "RX": "---"
                },
                {
                    "TX": "reset\r\n",
                    "RX": "resetting"
                }
            ]
        }
    ]
}
```

**Structure:**
- `DEV_KEY`: Password to enable developer mode
- `COMMANDS`: Pre-defined command shortcuts
- `TESTS`: Array of test sequences
  - `NAME`: Test identifier
  - `DESCRIPTION`: Test description
  - `SEQUENCE`: Array of TX/RX pairs to execute in order
    - `TX`: Data to send to device
    - `RX`: Expected response from device
  - `TRACES`: (Optional) Array of trace patterns to monitor

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
├── dev.py               # Test runner and developer utilities
├── setup.py             # Installation/packaging configuration
├── install.bat          # Windows installation script
├── install.sh           # Linux/macOS installation script
├── config.json          # Application configuration
├── dev.json             # Test sequences and dev settings
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

### Test Sequence Execution

1. User enables dev mode with `dev <key>`
2. User runs a test: `dev --run TEST_NAME`
3. `dev.py` loads the test from `dev.json`
4. For each step in the sequence:
   - Send TX data to device
   - Wait for and validate RX response
   - Record pass/fail result
5. Display test results and summary

## Module Documentation

### serial_core.py

Handles all serial port operations:

- `SerialCommunicator.connect()` - Establish serial connection
- `SerialCommunicator.disconnect()` - Close connection
- `SerialCommunicator.send()` - Send data
- `SerialCommunicator.receive()` - Read data
- `SerialCommunicator.read_until()` - Read until expected string
- `SerialCommunicator.list_ports()` - List available ports

### dev.py

Manages test execution:

- `DevTestRunner.set_dev_key()` - Validate developer key
- `DevTestRunner.list_tests()` - List available tests
- `DevTestRunner.run_test()` - Run a specific test
- `DevTestRunner.run_all_tests()` - Run all tests

### cli.py

Provides the interactive interface:

- `SerialCLI.process_command()` - Parse and execute user commands
- `SerialCLI.parse_connect_command()` - Handle connection commands
- `SerialCLI.parse_dev_command()` - Handle developer commands
- `SerialCLI.run()` - Main CLI loop

## Future Enhancements

- User-defined command scripts (beyond developer tests)
- Data logging and session recording
- GUI/TUI interface option
- Configuration profiles
- Advanced trace pattern matching
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

### Tests Don't Run
- Ensure dev mode is enabled: `dev <key>`
- Verify device is connected: `status`
- Check test names in `dev.json`

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
- ✓ Developer test framework
- ✓ Cross-platform installation
- ✓ Command-line help system
