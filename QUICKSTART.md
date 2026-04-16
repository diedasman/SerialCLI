# QUICKSTART.md

## SerialCLI Quick Start Guide

### Installation (5 minutes)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SerialCLI.git
cd SerialCLI
```

2. Install the package:
```bash
pip install -e .
```

### First Run

Open your terminal anywhere and type:
```bash
SerialCLI
```

You'll see the welcome screen. Type `help` to see all commands.

### Basic Usage (10 minutes)

#### Step 1: List Available Ports
```
SerialCLI> connect --list

Available Serial Ports:
  Port: COM3
    Description: Silicon Labs CP210x USB to UART Bridge Controller
    Hardware ID: USB VID:PID=10C4:EA60 SERIAL=F9D1F2F3
```

#### Step 2: Connect to Device
```
SerialCLI> connect -p COM3 -b 9600

✓ Connected to COM3 at 9600 baud
```

#### Step 3: Check Status
```
SerialCLI> status

✓ Connected
Port: COM3
Baudrate: 9600
Data bits: 8
Parity: N
Stop bits: 1
Timeout: 1.0s
```

#### Step 4: Send and Receive Data
```
SerialCLI> send "AT+RST\r\n"
✓ Sent: 'AT+RST\r\n'

SerialCLI> read
✓ Received: 'OK\r\n'
```

#### Step 5: Disconnect
```
SerialCLI> disconnect
✓ Disconnected successfully
```





### Configuration Options

#### Connection Parameters
| Parameter | Flag | Default | Example |
|-----------|------|---------|---------|
| Port | -p | (required) | -p COM3 |
| Baudrate | -b | 9600 | -b 115200 |
| Data bits | -dat | 8 | -dat 8 |
| Parity | -par | N | -par N |
| Stop bits | -stop | 1 | -stop 1 |
| Timeout | -t | 1.0 | -t 2.5 |

#### Test Parameters


### Troubleshooting

**Q: "Port not found" error**
- Ensure USB device is connected
- Try `connect --list` to see available ports
- Check device drivers on Windows

**Q: Connection succeeds but no data received**
- Verify device is powered on
- Check baud rate matches device settings
- Try increasing timeout: `connect -p COM3 -t 5.0`

**Q: Import error when running SerialCLI**
- Reinstall: `pip install -e .`
- Check Python version: `python --version` (should be 3.7+)
- Verify dependencies: `pip install pyserial`

### Common Workflows

#### Manual Communication
```
# Connect to device
connect -p COM3

# Send commands
send "AT+ID\r\n"
read

send "AT+RST\r\n"
read

# Disconnect when done
disconnect
```

### Next Steps

- Read [README.md](README.md) for complete documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Explore examples in `examples/` directory

### Getting Help

```
SerialCLI> help
```

This displays the complete command reference with all options and examples.

---

**Enjoy using SerialCLI! 🎉**
