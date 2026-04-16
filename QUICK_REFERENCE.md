# SerialCLI - Quick Reference

## Connection

| Command | Purpose |
|---------|---------|
| `connect --list` | List available serial ports |
| `connect -p COM3` | Connect to port (9600 baud) |
| `connect -p COM3 -b 115200` | Connect with custom baud |
| `disconnect` | Close connection |
| `status` | Show connection & logging status |

## Monitoring & Logging

| Command | Purpose |
|---------|---------|
| `monitor` | Real-time serial monitor (Ctrl+C to exit) |
| `logging enable logs/file.txt` | Start logging to file |
| `logging disable` | Stop logging |

## Data Transfer

| Command | Purpose |
|---------|---------|
| `send "data\r\n"` | Send data to device |
| `read` | Read available data |


## General

| Command | Purpose |
|---------|---------|
| `help` | Show full help menu |
| `exit`, `quit` | Exit SerialCLI |

## Common Workflows

### Basic Serial Communication

```
1. connect --list           (find your port)
2. connect -p COM3 -b 9600  (connect)
3. send "command\r\n"       (send data)
4. read                     (read response)
5. disconnect               (close)
```

### Live Monitoring

```
1. connect -p COM3
2. monitor
   [Watch data in real-time]
   [Ctrl+C to stop]
3. disconnect
```

### Extended Session

```
1. connect -p COM3
2. logging enable logs/session.txt
3. monitor                  (Ctrl+C when done)
4. [Or send commands while monitoring stopped]
5. logging disable
6. disconnect
```

## Connection Flags

| Flag | Default | Range | Example |
|------|---------|-------|---------|
| `-b` (baud) | 9600 | Any | `-b 115200` |
| `-dat` (data bits) | 8 | 5-9 | `-dat 8` |
| `-par` (parity) | N | N/E/O | `-par N` |
| `-stop` (stop bits) | 1 | 1-2 | `-stop 1` |
| `-t` (timeout) | 1.0 | Any | `-t 2.5` |

## Parity Codes

| Code | Meaning |
|------|---------|
| N | None (no parity) |
| E | Even parity |
| O | Odd parity |

## Log File Format

```
[HH:MM:SS.mmm] MESSAGE
```

Examples:
```
[10:30:45.123] CONNECTED: COM3 @ 9600 baud
[10:30:46.456] TX: 'AT+RST\r\n'
[10:30:47.789] RX: 'OK\r\n'
[10:30:58.987] DISCONNECTED
```

## Tips & Tricks

✅ **Always use `connect --list` first** - Verify your port is detected
✅ **Test with `read` before `monitor`** - Confirm device responds
✅ **Enable logging for debugging** - Creates permanent records
✅ **Use `status` frequently** - Check connection and logging state
✅ **Exit monitor with Ctrl+C** - No need for separate command
✅ **Use `\r\n` line endings** - Match your device protocol for send commands
✅ **Create `logs/` directory** - Organize your session records
✅ **Log files append** - Multiple sessions in one file

## Common Errors

| Error | Solution |
|-------|----------|
| Port not found | Run `connect --list` to verify port exists |
| Connection fails | Check baud rate, cable, and device driver |
| No data received | Verify device is powered, try `read` first |
| Test timeout | Increase timeout: `connect -p COM3 -t 5.0` |
| Monitor shows nothing | Device may not send on connection, send command first |
| Logging fails | Check directory permissions, try absolute path |

## File Locations

```
SerialCLI/
├── cli.py              (main interface)
├── serial_core.py      (serial logic)
├── config.json         (settings)
├── logo.txt            (startup image)
└── logs/               (session logs - create this)
    ├── session.txt
    ├── test_run.txt
    └── ...
```

## Documentation Files

| File | Contents |
|------|----------|
| `README.md` | Full feature overview |
| `QUICKSTART.md` | Getting started guide |
| `MONITOR_AND_LOGGING.md` | Detailed feature guide |
| `ARCHITECTURE.md` | Technical design |
| `CONTRIBUTING.md` | Developer guide |
| `CHANGELOG.md` | Version history |

## Examples

### Example: Connect and Send Command

```bash
SerialCLI> connect -p COM3
✓ Connected to COM3 at 9600 baud

SerialCLI> send "AT\r\n"
✓ Sent: 'AT\r\n'

SerialCLI> read
✓ Received: 'OK\r\n'

SerialCLI> disconnect
✓ Disconnected successfully
```

### Example: Monitor with Logging

```bash
SerialCLI> connect -p COM3
SerialCLI> logging enable logs/monitor.txt
✓ Logging enabled: logs/monitor.txt

SerialCLI> monitor
======================================================================
Serial Monitor Active (Ctrl+C to exit)
======================================================================

Device ready
Temp: 25.3°C
^C
SerialCLI> logging disable
✓ Logging disabled
```

---

**For detailed help, run: `help` or see README.md**
