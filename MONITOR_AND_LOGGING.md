# Serial Monitor & Logging Guide

## Overview

SerialCLI now includes two powerful features for development and debugging:
- **Serial Monitor**: Real-time data stream visualization
- **File Logging**: Automatic session recording

## Serial Monitor

The serial monitor displays all incoming data from your connected device in real-time.

### Usage

```bash
SerialCLI> connect -p COM3 -b 115200
SerialCLI> monitor
```

Output:
```
======================================================================
Serial Monitor Active (Ctrl+C to exit)
======================================================================

[Device streaming data here...]
Device status: OK
Temperature: 42.5°C
Humidity: 55%
[More data...]
```

### Features

- **Real-time Display**: Shows data as it arrives from the device
- **Non-blocking**: Monitor continues to update independently
- **Easy Exit**: Press `Ctrl+C` to stop monitoring and return to command prompt
- **Raw Output**: Displays exactly what the device sends

### Typical Workflow

```bash
# 1. List available ports
SerialCLI> connect --list

# 2. Connect to device
SerialCLI> connect -p COM3 -b 9600

# 3. Start monitoring
SerialCLI> monitor

# 4. Watch the data stream
# [Device data displays in real-time]

# 5. Exit monitor with Ctrl+C
SerialCLI> 

# 6. You can now send commands while monitor is stopped
SerialCLI> send "STATUS\r\n"

# 7. Restart monitor if needed
SerialCLI> monitor
```

## File Logging

File logging automatically records all serial communication to a file for later review and analysis.

### Enable Logging

```bash
SerialCLI> logging enable logs/session.txt
✓ Logging enabled: logs/session.txt
```

The system automatically:
- Creates the directory if it doesn't exist
- Logs with timestamps for each message
- Records both TX (sent) and RX (received) data

### What Gets Logged

```
[10:30:45.123] CONNECTED: COM3 @ 9600 baud
[10:30:46.456] TX: 'AT+RST\r\n'
[10:30:47.789] RX: 'OK\r\n'
[10:30:48.012] DISCONNECTED
```

### Disable Logging

```bash
SerialCLI> logging disable
✓ Logging disabled
```

### Log File Format

Each session creates a log like `logs/session.txt`:

```
======================================================================
SerialCLI Log - 2026-04-15 10:30:45
======================================================================

[10:30:45.123] CONNECTED: COM3 @ 9600 baud
[10:30:46.456] TX: 'AT+RST\r\n'
[10:30:47.789] RX: 'OK\r\n'
[10:30:54.321] TX: 'AT+ID?\r\n'
[10:30:55.654] RX: 'ABC123DEF456\r\n'
[10:30:58.987] DISCONNECTED

[Later timestamp...]
[Time] CONNECTED: COM3 @ 115200 baud
[... more data ...]
```

### Advanced Logging Scenarios

#### Logging with Monitor and Test

```bash
# Enable logging
SerialCLI> logging enable logs/verification_test.txt

# Start monitor (continues in background, accessible with Ctrl+C)
SerialCLI> monitor

# While monitoring, open another terminal or window and run tests
# All activity is logged to the file

# Stop monitor when done
# Ctrl+C
```

#### Long-term Sessions

```bash
# Enable logging to a timestamped file
SerialCLI> logging enable logs/session_$(date +%Y%m%d_%H%M%S).txt

# Leave connected and monitoring for extended period
SerialCLI> monitor
# [Let it run...]

# Later analyze the log file
```

## Combining Features

### Test with Logging and Monitoring

```bash
# 1. Connect to device
SerialCLI> connect -p COM3 -b 9600

# 2. Enable logging for session record
SerialCLI> logging enable logs/test_session.txt

# 3. Optional: Monitor raw data
SerialCLI> monitor
# [Watch device output]
# Ctrl+C to return to prompt

# 4. Enable dev mode
SerialCLI> dev devvy

# 5. Run tests (all activity logged)
SerialCLI> dev --run TRACECATCH

# 6. Disable logging
SerialCLI> logging disable

# 7. Review the log file
# [Open logs/test_session.txt]
```

## Trace Sequence Handling

The TRACECATCH test now supports automatic trace extraction. When a test runs with traces defined:

```json
"TRACES" : [
    {
        "KEY" : "[TRACE]",
        "TRACE_CHAR" : " ",
        "TRACE_END" : "\n"
    }
]
```

The test runner will:
1. Send TX commands and wait for RX confirmation
2. When RX is detected, immediately send the next TX (no delay)
3. Parse any trace data into the log

### Trace Configuration

| Field | Purpose | Example |
|-------|---------|---------|
| `KEY` | String that marks trace start | `"[TRACE]"` |
| `TRACE_CHAR` | Character after KEY marking data start | `" "` (space) or `":"` |
| `TRACE_END` | String marking trace end | `"\n"` (newline) |

### Example TRACECATCH Flow

Device sends:
```
waking up
trace was turned ON
[TRACE] sensor data here
[DATA]: temperature=42.5
```

Test executes:
1. Send `wake\r\n` → Receives `waking up` ✓
2. Send `trace ON\r\n` → Receives `trace was turned ON` ✓
3. Parse traces:
   - Found `[TRACE]` key, extract after space until newline
   - Found `[DATA]` key, extract after `:` until newline

## Status Check

View current logging and monitoring status:

```bash
SerialCLI> status

✓ Connected
Port: COM3
Baudrate: 9600
Data bits: 8
Parity: N
Stop bits: 1
Timeout: 1.0s

✓ Dev mode: ENABLED

✓ Logging: ENABLED (logs/session.txt)
```

## Troubleshooting

### Logging not working
- Ensure the directory exists or SerialCLI can create it
- Check file permissions
- Verify the path is correct: `logging enable logs/mylog.txt`

### Monitor shows nothing
- Device may not be sending data yet
- Increase timeout: `connect -p COM3 -t 5.0`
- Manually send a command: `send "AT\r\n"` then `read`
- Then try `monitor` again

### Large log files
- Log files grow quickly with high-frequency data
- Consider using timestamps in filenames
- Archive old logs regularly
- Disable logging when not needed

## Best Practices

1. **Always enable logging during tests** - Creates records for debugging
2. **Name log files descriptively** - Include test name and timestamp
3. **Keep monitor in separate terminal** - Easier to manage
4. **Use `status` frequently** - Verify logging is active
5. **Review logs after important tests** - Identify timing issues
6. **Disable logging before disconnecting** - Ensures data is flushed

## Examples

### Example 1: Basic Monitoring

```bash
SerialCLI> connect -p COM3
SerialCLI> monitor
# [Watch data for 30 seconds]
# Ctrl+C
SerialCLI> disconnect
```

### Example 2: Test with Full Logging

```bash
SerialCLI> connect -p COM3
SerialCLI> logging enable logs/full_test.txt
SerialCLI> dev devvy
SerialCLI> dev --run-all
SerialCLI> logging disable
SerialCLI> disconnect
# Review logs/full_test.txt for results
```

### Example 3: Continuous Monitoring with Data Capture

```bash
SerialCLI> connect -p COM3
SerialCLI> logging enable logs/continuous.txt

# Terminal 1: Monitor
SerialCLI> monitor

# Continue receiving data...
# Press Ctrl+C when done

SerialCLI> logging disable
SerialCLI> disconnect

# Analyze logs/continuous.txt
```

---

**Logging and monitoring are essential tools for serial development. Use them frequently!**
