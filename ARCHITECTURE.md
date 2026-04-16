# ARCHITECTURE.md

## SerialCLI Architecture Documentation

### Overview

SerialCLI is a modular command-line application for serial device communication. It follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         User Input (CLI)                │
│      (__main__.py / cli.py)             │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼──────────────┐   ┌──────▼───────────┐
│  Command Handler │   │  Dev Test Runner │
│    (cli.py)      │   │   (dev.py)       │
└────────┬─────────┘   └───────┬──────────┘
         │                     │
         └────────────┬────────┘
                      │
         ┌────────────▼────────────┐
         │  Serial Communicator    │
         │  (serial_core.py)       │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │   USB Serial Device     │
         └─────────────────────────┘
```

### Module Responsibilities

#### __main__.py - Entry Point
- **Purpose**: Application bootstrap and welcome screen
- **Responsibilities**:
  - Print logo from `logo.txt`
  - Display welcome message and tips
  - Initialize and run the CLI
  - Handle cleanup on exit

#### cli.py - User Interface Layer
- **Purpose**: Interactive command-line interface
- **Key Classes**: `SerialCLI`
- **Responsibilities**:
  - Parse user commands
  - Validate command syntax
  - Route commands to appropriate handlers
  - Display help and status information
  - Manage interactive input loop

#### serial_core.py - Serial Communication Backend
- **Purpose**: Low-level serial port operations
- **Key Class**: `SerialCommunicator`
- **Responsibilities**:
  - Enumerate available serial ports
  - Establish and manage connections
  - Send/receive data with error handling
  - Configure port parameters (baud rate, data bits, etc.)
  - Provide read_until() for sequence-based communication

### Data Flow

#### Connection Flow
```
User: "connect -p COM3"
         ↓
CLI Parser: parse_connect_command()
         ↓
SerialCommunicator.connect()
         ↓
pyserial: serial.Serial()
         ↓
USB Device: Connected
         ↓
CLI Output: "✓ Connected to COM3 at 9600 baud"
```

### Command Processing Pipeline

1. **Input**: User types command at prompt
2. **Lexing**: shlex.split() tokenizes the input
3. **Dispatch**: First token identifies command type
4. **Parsing**: Remaining tokens parsed into parameters
5. **Execution**: Command handler processes parameters
6. **Output**: Results formatted and displayed

### Configuration Files

#### config.json Structure (Future Use)
```json
{
  "SETTINGS": {
    "PORT": "default_port",
    "BAUD": "default_baud",
    "TERMINATION": {...},
    "LOGGING": {...}
  }
}
```

### Error Handling Strategy

The application uses a **"tuple-based result"** pattern throughout:

```python
# Standard return pattern: (success: bool, message: str)
success, message = serial_comm.connect(port)
if success:
    print(f"✓ {message}")
else:
    print(f"✗ {message}")
```

### Extension Points

The architecture supports easy extensibility:

1. **New Commands**: Add parsing methods to `SerialCLI` class
2. **Serial Operations**: Add methods to `SerialCommunicator` class
3. **Configurations**: Add settings processing from `config.json`

### Dependencies

- **pyserial**: Serial port communication
- **Standard Library**: sys, pathlib, typing, time, shlex

### Design Patterns Used

1. **Facade Pattern**: `SerialCLI` provides simplified interface to complex subsystems
2. **Strategy Pattern**: Different command handlers implement command processing
3. **State Pattern**: `SerialCommunicator.is_connected` manages connection state

### Performance Considerations

- **Minimal Latency**: Direct serial operations without blocking
- **Configurable Timeouts**: Prevent indefinite waits
- **Efficient Parsing**: shlex for robust command tokenization
- **Lazy Loading**: Configurations loaded on demand

### Security Considerations

- **Input Validation**: Command parsing validates parameter types
- **Exception Handling**: Try-catch blocks prevent crashes from invalid devices
- **Error Messages**: Avoid exposing system details in errors

### Future Architecture Enhancements

1. **Logging System**: File-based logging for sessions
2. **Profile Management**: Save/load connection profiles
3. **Plugin System**: Dynamic command loading
4. **Event System**: Callbacks for connection state changes
5. **Async Operations**: Non-blocking I/O for long tests
