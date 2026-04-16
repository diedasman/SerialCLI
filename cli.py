# cli.py
# Main command-line interface for SerialCLI.
# User can enter these commands after running the application.
# Handles user input, command parsing, and execution.

import sys
import os
import shlex
from pathlib import Path
from typing import List, Dict
from serial_core import SerialCommunicator
from dev import DevTestRunner


class SerialCLI:
    """
    Main command-line interface for SerialCLI application.
    Provides interactive command processing for serial communication and testing.
    """

    def __init__(self, app_dir: str = "."):
        """
        Initialize the CLI application.
        
        Args:
            app_dir: Directory where dev.json and other config files are located
        """
        self.app_dir = Path(app_dir)
        self.serial_comm = SerialCommunicator()
        self.dev_runner = DevTestRunner(str(self.app_dir / "dev.json"))
        self.dev_runner.set_serial_communicator(self.serial_comm)
        self.running = True

    def print_help(self) -> None:
        """Display help menu with all available commands."""
        help_text = """
╔════════════════════════════════════════════════════════════════╗
║                    SerialCLI - Commands Help                   ║
╚════════════════════════════════════════════════════════════════╝

BASIC COMMANDS:
  help                       - Display this help menu
  exit, quit                 - Exit the application
  status                     - Show connection status and info

CONNECTION COMMANDS:
  connect --list             - List all available serial ports
  connect -p <port>         - Connect to a port (using default settings)
  connect -p <port> -b <baud> -dat <bits> -par <parity> -stop <bits> -t <timeout>
    port:     Port name (e.g., COM3 or /dev/ttyUSB0)
    baud:     Baudrate (default: 9600)
    bits:     Data bits (default: 8)
    parity:   N=None, E=Even, O=Odd (default: N)
    bits:     Stop bits (default: 1)
    timeout:  Timeout in seconds (default: 1.0)

  disconnect                 - Close the current serial connection

MONITOR & LOGGING:
  monitor                    - Display real-time serial data stream (Ctrl+C to exit)
  logging enable <filepath>  - Enable logging to file
  logging disable            - Disable logging

MANUAL COMMUNICATION:
  send <data>                - Send data to the serial device
  read                       - Read available data from the device

DEVELOPER COMMANDS (requires dev key):
  dev <key>                  - Enter developer key to enable dev mode
  dev --list                 - List all available tests
  dev --run <test_name>      - Run a specific test
    -c <count>               - Number of times to run the test (default: 1)
    -t <delay_ms>            - Delay between runs in milliseconds (default: 0)
  dev --run-all              - Run all tests
    -t <delay_ms>            - Delay between tests in milliseconds (default: 500)

EXAMPLES:
  connect --list
  connect -p COM3 -b 115200
  logging enable logs/session.txt
  monitor
  dev devvy
  dev --run VERIFICATION -c 2 -t 1000
  send "hello"
  read

"""
        print(help_text)

    def parse_connect_command(self, args: List[str]) -> None:
        """Parse and execute connect command."""
        if not args:
            print("Usage: connect --list OR connect -p <port> [options]")
            return

        # Handle port listing
        if args[0] == "--list":
            self._list_ports()
            return

        # Parse connection parameters
        params = self._parse_params(args)

        if "p" not in params:
            print("Error: Port (-p) is required")
            return

        port = params["p"]
        baud = int(params.get("b", "9600"))
        data_bits = int(params.get("dat", "8"))
        parity = params.get("par", "N")
        stop_bits = int(params.get("stop", "1"))
        timeout = float(params.get("t", "1.0"))

        success, message = self.serial_comm.connect(
            port=port,
            baudrate=baud,
            data_bits=data_bits,
            parity=parity,
            stop_bits=stop_bits,
            timeout=timeout
        )

        print(f"{'✓' if success else '✗'} {message}")

    def parse_dev_command(self, args: List[str]) -> None:
        """Parse and execute dev command."""
        if not args:
            print("Usage: dev <key> OR dev --list OR dev --run <test_name> [options]")
            return

        # Handle dev key entry
        if args[0] not in ["--list", "--run", "--run-all"]:
            success, message = self.dev_runner.set_dev_key(args[0])
            print(f"{'✓' if success else '✗'} {message}")
            return

        # List tests
        if args[0] == "--list":
            success, tests = self.dev_runner.list_tests()
            if success:
                print(f"\nAvailable tests ({len(tests)}):")
                for idx, test in enumerate(tests):
                    print(f"  [{idx}] {test.get('NAME', 'Unknown')}: {test.get('DESCRIPTION', 'N/A')}")
            else:
                print(f"✗ Error: {tests}")
            return

        # Run all tests
        if args[0] == "--run-all":
            params = self._parse_params(args[1:])
            delay_ms = int(params.get("t", "500"))
            success, result = self.dev_runner.run_all_tests(delay_ms=delay_ms, verbose=True)
            print(result)
            return

        # Run specific test
        if args[0] == "--run" and len(args) > 1:
            test_name = args[1]
            params = self._parse_params(args[2:])
            count = int(params.get("c", "1"))
            delay_ms = int(params.get("t", "0"))

            success, result = self.dev_runner.run_test(
                test_name=test_name,
                count=count,
                delay_ms=delay_ms,
                verbose=True
            )
            print(result)
            return

        print("Invalid dev command syntax")

    def parse_send_command(self, args: List[str]) -> None:
        """Parse and execute send command."""
        if not args:
            print("Usage: send <data>")
            return

        data = " ".join(args)
        success, message = self.serial_comm.send(data)
        print(f"{'✓' if success else '✗'} {message}")

    def _list_ports(self) -> None:
        """List all available serial ports."""
        ports = self.serial_comm.list_ports()
        if not ports:
            print("No serial ports found")
            return

        print("\nAvailable Serial Ports:")
        print("─" * 70)
        for port, description, hwid in ports:
            print(f"  Port: {port}")
            print(f"    Description: {description}")
            print(f"    Hardware ID: {hwid}")
            print()

    def _parse_params(self, args: List[str]) -> Dict[str, str]:
        """Parse command-line parameters in -key value format."""
        params = {}
        i = 0
        while i < len(args):
            if args[i].startswith("-"):
                key = args[i].lstrip("-")
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    params[key] = args[i + 1]
                    i += 2
                else:
                    params[key] = "True"
                    i += 1
            else:
                i += 1
        return params

    def show_status(self) -> None:
        """Display current connection status."""
        if self.serial_comm.is_connected:
            print("\n✓ Connected")
            print(self.serial_comm.get_connection_info())
        else:
            print("\n✗ Not connected to any port")

        if self.dev_runner.is_dev_enabled():
            print("\n✓ Dev mode: ENABLED")
        else:
            print("\n✗ Dev mode: DISABLED")

        if self.serial_comm.log_enabled:
            print(f"\n✓ Logging: ENABLED ({self.serial_comm.log_file})")
        else:
            print("\n✗ Logging: DISABLED")

    def start_monitor(self) -> None:
        """Start real-time serial monitor."""
        if not self.serial_comm.is_connected:
            print("✗ Not connected to any port")
            return

        print("\n" + "="*70)
        print("Serial Monitor Active (Ctrl+C to exit)")
        print("="*70 + "\n")

        try:
            while True:
                success, data = self.serial_comm.receive(timeout=0.1)
                if success and data:
                    print(data, end='', flush=True)
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("Serial Monitor Stopped")
            print("="*70)

    def parse_logging_command(self, args: List[str]) -> None:
        """Parse and execute logging command."""
        if not args:
            print("Usage: logging enable <filepath> OR logging disable")
            return

        if args[0] == "enable":
            if len(args) < 2:
                print("Usage: logging enable <filepath>")
                return
            filepath = args[1]
            success, message = self.serial_comm.enable_logging(filepath)
            print(f"{'✓' if success else '✗'} {message}")

        elif args[0] == "disable":
            success, message = self.serial_comm.disable_logging()
            print(f"{'✓' if success else '✗'} {message}")

        else:
            print("Usage: logging enable <filepath> OR logging disable")

    def process_command(self, user_input: str) -> None:
        """
        Process a user command.
        
        Args:
            user_input: The command string entered by the user
        """
        if not user_input.strip():
            return

        tokens = shlex.split(user_input.strip())
        command = tokens[0].lower()
        args = tokens[1:]

        if command in ["exit", "quit"]:
            self.running = False
            print("Goodbye!")
            return

        elif command == "help":
            self.print_help()

        elif command == "status":
            self.show_status()

        elif command == "connect":
            self.parse_connect_command(args)

        elif command == "disconnect":
            success, message = self.serial_comm.disconnect()
            print(f"{'✓' if success else '✗'} {message}")

        elif command == "monitor":
            self.start_monitor()

        elif command == "logging":
            self.parse_logging_command(args)

        elif command == "dev":
            self.parse_dev_command(args)

        elif command == "send":
            self.parse_send_command(args)

        elif command == "read":
            if not self.serial_comm.is_connected:
                print("✗ Not connected")
                return
            success, data = self.serial_comm.receive()
            if success:
                print(f"✓ Received: {repr(data)}")
            else:
                print(f"✗ No data or error: {data}")

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands")

    def run(self) -> None:
        """Run the interactive CLI loop."""
        print("\nType 'help' for available commands or 'exit' to quit\n")

        while self.running:
            try:
                user_input = input("SerialCLI> ")
                self.process_command(user_input)
            except KeyboardInterrupt:
                print("\n\nInterrupted by user")
                self.running = False
            except Exception as e:
                print(f"Error: {str(e)}")

    def cleanup(self) -> None:
        """Clean up resources before exit."""
        if self.serial_comm.is_connected:
            self.serial_comm.disconnect()


def main() -> int:
    """Main entry point for SerialCLI."""
    # Get the directory where this script is located
    app_dir = Path(__file__).parent.absolute()

    # Create and run CLI
    cli = SerialCLI(str(app_dir))

    try:
        cli.run()
    finally:
        cli.cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())

