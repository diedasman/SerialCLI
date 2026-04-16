# Entry point for SerialCLI when run as a package.
# Displays logo and welcome message, then launches the CLI.

import sys
from pathlib import Path
from cli import SerialCLI


def print_logo_and_welcome():
    """Print the SerialCLI logo and welcome message."""
    app_dir = Path(__file__).parent
    logo_file = app_dir / "logo.txt"

    # Print logo
    try:
        with open(logo_file, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("SerialCLI")

    # Print welcome message
    print("\n" + "=" * 70)
    print("  SerialCLI - Serial Device Communication Tool")
    print("=" * 70)
    print("\n📝 TIPS:")
    print("  • Type 'help' for a list of available commands")
    print("  • Use 'connect --list' to see available serial ports")
    print("  • Use 'dev <key>' to enable developer mode")
    print("  • Use 'status' to check connection and dev mode status")
    print("\n" + "=" * 70 + "\n")


def main():
    """Main entry point."""
    print_logo_and_welcome()

    app_dir = Path(__file__).parent.absolute()
    cli = SerialCLI(str(app_dir))

    try:
        cli.run()
    finally:
        cli.cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())
