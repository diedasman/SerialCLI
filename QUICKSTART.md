# QUICKSTART.md

## SerialCLI Quick Start Guide

### Installation (5 minutes)

#### Windows
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/SerialCLI.git
cd SerialCLI

# 2. Run as Administrator
install.bat
```

#### Linux / macOS
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/SerialCLI.git
cd SerialCLI

# 2. Run the installer
bash install.sh
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

✗ Dev mode: DISABLED
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

### Developer Mode (15 minutes)

#### Step 1: Enable Dev Mode
```
SerialCLI> dev devvy
✓ Dev mode enabled
```

#### Step 2: List Available Tests
```
SerialCLI> dev --list

Available tests (2):
  [0] VERIFICATION: Verification Checks
  [1] TRACECATCH: Trace and Catch Checks
```

#### Step 3: Run a Test
```
SerialCLI> dev --run VERIFICATION

Test 'VERIFICATION' started...
  State 0: TX → '+++'
  State 0: RX ✓ '---'
  State 1: TX → 'KEY1\r\n'
  State 1: RX ✓ 'string'
  State 2: TX → 'KEY2\r\n'
  State 2: RX ✓ 'string'
  State 3: TX → 'reset\r\n'
  State 3: RX ✓ 'resetting'

Test 'VERIFICATION' completed: 4 passed, 0 failed ✓
```

#### Step 4: Run Test Multiple Times
```
SerialCLI> dev --run VERIFICATION -c 3 -t 1000

--- Run 1/3 ---
[test output]

--- Run 2/3 ---
[test output]

--- Run 3/3 ---
[test output]

Test 'VERIFICATION' completed: 12 passed, 0 failed ✓
```

#### Step 5: Run All Tests
```
SerialCLI> dev --run-all

Running 2 tests...

[TEST 1/2] VERIFICATION
Description: Verification Checks
[test output]

[TEST 2/2] TRACECATCH
Description: Trace and Catch Checks
[test output]

==================================================
FINAL RESULTS: 6 passed, 0 failed
==================================================
```

### Creating Your Own Tests

Edit `dev.json` to add new test sequences:

```json
{
    "DEV_KEY": "devvy",
    "TESTS": [
        {
            "NAME": "MY_TEST",
            "DESCRIPTION": "My custom test",
            "SEQUENCE": [
                {
                    "TX": "COMMAND1\r\n",
                    "RX": "RESPONSE1"
                },
                {
                    "TX": "COMMAND2\r\n",
                    "RX": "RESPONSE2"
                }
            ]
        }
    ]
}
```

Then run it:
```
SerialCLI> dev --run MY_TEST
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
| Parameter | Flag | Default |
|-----------|------|---------|
| Count | -c | 1 |
| Delay (ms) | -t | 0 |

### Troubleshooting

**Q: "Port not found" error**
- Ensure USB device is connected
- Try `connect --list` to see available ports
- Check device drivers on Windows

**Q: Connection succeeds but no data received**
- Verify device is powered on
- Check baud rate matches device settings
- Try increasing timeout: `connect -p COM3 -t 5.0`

**Q: Test fails on RX validation**
- Check expected response (RX) value in dev.json
- Add debug output by running test again
- Verify device is responding correctly

**Q: Import error when running SerialCLI**
- Reinstall: `pip install -e .`
- Check Python version: `python --version` (should be 3.7+)
- Verify dependencies: `pip install pyserial`

### Common Workflows

#### Testing a Device
```
# 1. List ports
connect --list

# 2. Connect
connect -p COM3 -b 9600

# 3. Enable dev mode
dev devvy

# 4. Run test suite
dev --run-all

# 5. Check results
[review output]

# 6. Disconnect
disconnect
```

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

#### Developing and Testing
```
# 1. Connect device
connect -p COM3

# 2. Enable dev and test
dev devvy
dev --run VERIFICATION

# 3. Modify dev.json with new tests
# 4. Test again
dev --run MY_NEW_TEST

# 5. Repeat until satisfied
```

### Next Steps

- Read [README.md](README.md) for complete documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Review [dev.json](dev.json) structure for creating tests
- Explore examples in `examples/` directory

### Getting Help

```
SerialCLI> help
```

This displays the complete command reference with all options and examples.

---

**Enjoy using SerialCLI! 🎉**
