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
from rich.console import Console # type: ignore
from rich.panel import Panel # type: ignore
from rich.table import Table # type: ignore
from rich.text import Text # type: ignore
from rich.syntax import Syntax # type: ignore

console = Console()


class SerialCLI:
    """
    Main command-line interface for SerialCLI application.
    Provides interactive command processing for serial communication and testing.
    """

    def __init__(self, app_dir: str = "."):
        """
        Initialize the CLI application.
        
        Args:
            app_dir: Directory where configuration files are located
        """
        self.app_dir = Path(app_dir)
        self.serial_comm = SerialCommunicator()
        self.running = True

    def print_help(self) -> None:
        """Display help menu with all available commands."""
        help_text = """[bold cyan]BASIC COMMANDS:[/bold cyan]
  [yellow]help[/yellow]                       - Display this help menu
  [yellow]exit, quit[/yellow]                 - Exit the application
  [yellow]status[/yellow]                     - Show connection status and info

[bold cyan]CONNECTION COMMANDS:[/bold cyan]
  [yellow]connect --list[/yellow]             - List all available serial ports
  [yellow]connect -p <port>[/yellow]         - Connect to a port (using default settings)
  [yellow]connect -p <port> -b <baud> -dat <bits> -par <parity> -stop <bits> -t <timeout>[/yellow]
    [green]port:[/green]     Port name (e.g., COM3 or /dev/ttyUSB0)
    [green]baud:[/green]     Baudrate (default: 9600)
    [green]bits:[/green]     Data bits (default: 8)
    [green]parity:[/green]   N=None, E=Even, O=Odd (default: N)
    [green]bits:[/green]     Stop bits (default: 1)
    [green]timeout:[/green]  Timeout in seconds (default: 1.0)

  [yellow]disconnect[/yellow]                 - Close the current serial connection

[bold cyan]MONITOR & LOGGING:[/bold cyan]
  [yellow]monitor[/yellow]                    - Display real-time serial data stream (Ctrl+C to exit)
  [yellow]logging enable <filepath>[/yellow]  - Enable logging to file
  [yellow]logging disable[/yellow]            - Disable logging

[bold cyan]MANUAL COMMUNICATION:[/bold cyan]
  [yellow]send <data>[/yellow]                - Send data to the serial device
  [yellow]read[/yellow]                       - Read available data from the device



[bold cyan]EXAMPLES:[/bold cyan]
  [magenta]connect --list[/magenta]
  [magenta]connect -p COM3 -b 115200[/magenta]
  [magenta]logging enable logs/session.txt[/magenta]
  [magenta]monitor[/magenta]
  [magenta]send "hello"[/magenta]
  [magenta]read[/magenta]
"""
        panel = Panel(help_text, title="[bold cyan]SerialCLI - Commands Help[/bold cyan]", style="bold blue")
        console.print(panel)

    def parse_connect_command(self, args: List[str]) -> None:
        """Parse and execute connect command."""
        if not args:
            console.print("[red]Usage:[/red] connect --list OR connect -p <port> [options]")
            return

        # Handle port listing
        if args[0] == "--list":
            self._list_ports()
            return

        # Parse connection parameters
        params = self._parse_params(args)

        if "p" not in params:
            console.print("[bold red]Error:[/bold red] Port (-p) is required")
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

        if success:
            console.print(f"[bold green]✓ {message}[/bold green]")
        else:
            console.print(f"[bold red]✗ {message}[/bold red]")



    def parse_send_command(self, args: List[str]) -> None:
        """Parse and execute send command."""
        if not args:
            console.print("[red]Usage:[/red] send <data>")
            return

        data = " ".join(args)
        success, message = self.serial_comm.send(data)
        if success:
            console.print(f"[bold green]✓ {message}[/bold green]")
        else:
            console.print(f"[bold red]✗ {message}[/bold red]")

    def _list_ports(self) -> None:
        """List all available serial ports."""
        ports = self.serial_comm.list_ports()
        if not ports:
            console.print("[yellow]No serial ports found[/yellow]")
            return

        table = Table(title="[bold cyan]Available Serial Ports[/bold cyan]", show_header=True, header_style="bold cyan")
        table.add_column("Port", style="yellow")
        table.add_column("Description", style="green")
        table.add_column("Hardware ID", style="magenta")

        for port, description, hwid in ports:
            table.add_row(port, description, hwid)

        console.print("\n")
        console.print(table)

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
        console.print()
        if self.serial_comm.is_connected:
            console.print("[bold green]✓ Connected[/bold green]")
            console.print(f"[cyan]{self.serial_comm.get_connection_info()}[/cyan]")
        else:
            console.print("[bold red]✗ Not connected to any port[/bold red]")

        console.print()
        if self.serial_comm.log_enabled:
            console.print(f"[bold green]✓ Logging: ENABLED[/bold green] [cyan]({self.serial_comm.log_file})[/cyan]")
        else:
            console.print("[bold yellow]✗ Logging: DISABLED[/bold yellow]")

    def start_monitor(self) -> None:
        """Start real-time serial monitor."""
        if not self.serial_comm.is_connected:
            console.print("[bold red]✗ Not connected to any port[/bold red]")
            return

        monitor_panel = Panel(
            "Press [bold]Ctrl+C[/bold] to exit",
            title="[bold cyan]Serial Monitor Active[/bold cyan]",
            style="bold blue"
        )
        console.print("\n")
        console.print(monitor_panel)
        console.print()

        try:
            while True:
                success, data = self.serial_comm.receive(timeout=0.1)
                if success and data:
                    console.print(data, end='', soft_wrap=True)
        except KeyboardInterrupt:
            console.print("\n")
            stopped_panel = Panel(
                "Monitor stopped",
                title="[bold cyan]Serial Monitor[/bold cyan]",
                style="bold blue"
            )
            console.print(stopped_panel)

    def parse_logging_command(self, args: List[str]) -> None:
        """Parse and execute logging command."""
        if not args:
            console.print("[red]Usage:[/red] logging enable <filepath> OR logging disable")
            return

        if args[0] == "enable":
            if len(args) < 2:
                console.print("[red]Usage:[/red] logging enable <filepath>")
                return
            filepath = args[1]
            success, message = self.serial_comm.enable_logging(filepath)
            if success:
                console.print(f"[bold green]✓ {message}[/bold green]")
            else:
                console.print(f"[bold red]✗ {message}[/bold red]")

        elif args[0] == "disable":
            success, message = self.serial_comm.disable_logging()
            if success:
                console.print(f"[bold green]✓ {message}[/bold green]")
            else:
                console.print(f"[bold red]✗ {message}[/bold red]")

        else:
            console.print("[red]Usage:[/red] logging enable <filepath> OR logging disable")

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
            console.print("[bold magenta]Goodbye![/bold magenta]")
            return

        elif command == "help":
            self.print_help()

        elif command == "status":
            self.show_status()

        elif command == "connect":
            self.parse_connect_command(args)

        elif command == "disconnect":
            success, message = self.serial_comm.disconnect()
            if success:
                console.print(f"[bold green]✓ {message}[/bold green]")
            else:
                console.print(f"[bold red]✗ {message}[/bold red]")

        elif command == "monitor":
            self.start_monitor()

        elif command == "logging":
            self.parse_logging_command(args)

        elif command == "send":
            self.parse_send_command(args)

        elif command == "read":
            if not self.serial_comm.is_connected:
                console.print("[bold red]✗ Not connected[/bold red]")
                return
            success, data = self.serial_comm.receive()
            if success:
                console.print(f"[bold green]✓ Received:[/bold green] [cyan]{repr(data)}[/cyan]")
            else:
                console.print(f"[bold red]✗ No data or error: {data}[/bold red]")

        else:
            console.print(f"[bold red]Unknown command:[/bold red] [yellow]{command}[/yellow]")
            console.print("Type [cyan]'help'[/cyan] for available commands")

    def run(self) -> None:
        """Run the interactive CLI loop."""
        tip_panel = Panel(
            "Type [cyan]'help'[/cyan] for available commands or [cyan]'exit'[/cyan] to quit",
            style="bold green"
        )
        console.print("")
        console.print(tip_panel)
        console.print()

        while self.running:
            try:
                user_input = input("SerialCLI> ")
                self.process_command(user_input)
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Interrupted by user[/bold yellow]")
                self.running = False
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")

    def cleanup(self) -> None:
        """Clean up resources before exit."""
        if self.serial_comm.is_connected:
            self.serial_comm.disconnect()


def print_logo_and_welcome():
    """Print the SerialCLI logo and welcome message."""
    app_dir = Path(__file__).parent
    logo_file = app_dir / "logo.txt"

    # Print logo
    try:
        with open(logo_file, 'r') as f:
            console.print(f"[bold cyan]{f.read()}[/bold cyan]")
    except FileNotFoundError:
        console.print("[bold cyan]SerialCLI[/bold cyan]")

    # Print welcome message with Rich panel
    welcome_text = """[bold magenta]📝 TIPS:[/bold magenta]
[cyan]• Type 'help' for a list of available commands[/cyan]
[cyan]• Use 'connect --list' to see available serial ports[/cyan]
[cyan]• Use 'status' to check connection status[/cyan]"""
    
    panel = Panel(
        welcome_text,
        title="[bold cyan]SerialCLI - Serial Device Communication Tool[/bold cyan]",
        style="bold blue"
    )
    console.print(panel)


def main() -> int:
    """Main entry point for SerialCLI."""
    print_logo_and_welcome()
    
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

