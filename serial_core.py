# serial_core.py
# Core serial communication module for SerialCLI.
# Handles serial port connection, communication, and device enumeration.

import serial # type: ignore
import serial.tools.list_ports # type: ignore
from typing import Optional, List, Tuple
import time
from pathlib import Path
from datetime import datetime


class SerialCommunicator:
    """
    Manages serial port connections and communication with USB devices.
    """

    def __init__(self):
        self.connection: Optional[serial.Serial] = None
        self.port: Optional[str] = None
        self.is_connected = False
        self.log_enabled = False
        self.log_file: Optional[Path] = None

    def enable_logging(self, log_file_path: str) -> Tuple[bool, str]:
        """
        Enable logging to a file.
        
        Args:
            log_file_path: Path to log file
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            log_path = Path(log_file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.log_file = log_path
            self.log_enabled = True
            
            # Write header
            with open(self.log_file, 'a') as f:
                f.write(f"\n{'='*70}\n")
                f.write(f"SerialCLI Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*70}\n\n")
            
            return True, f"Logging enabled: {log_file_path}"
        except Exception as e:
            return False, f"Failed to enable logging: {str(e)}"

    def disable_logging(self) -> Tuple[bool, str]:
        """Disable logging."""
        self.log_enabled = False
        if self.log_file:
            return True, f"Logging disabled"
        return False, "Logging was not enabled"

    def _log(self, message: str) -> None:
        """Write message to log file."""
        if not self.log_enabled or not self.log_file:
            return
        
        try:
            with open(self.log_file, 'a') as f:
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass  # Silently fail if logging fails

    def list_ports(self) -> List[Tuple[str, str, str]]:
        """
        List all available serial ports.
        
        Returns:
            List of tuples containing (port, description, hwid)
        """
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append((port.device, port.description, port.hwid))
        return ports

    def connect(
        self,
        port: str,
        baudrate: int = 9600,
        data_bits: int = 8,
        parity: str = 'N',
        stop_bits: int = 1,
        timeout: float = 1.0
    ) -> Tuple[bool, str]:
        """
        Establish a serial connection to the specified port.
        
        Args:
            port: Serial port name (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate: Baud rate (default 9600)
            data_bits: Number of data bits (default 8)
            parity: Parity bit ('N'=None, 'E'=Even, 'O'=Odd, default 'N')
            stop_bits: Number of stop bits (default 1)
            timeout: Read/write timeout in seconds (default 1.0)
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if self.is_connected:
                return False, "Already connected to a port. Disconnect first."

            # Map parity string
            parity_map = {'N': serial.PARITY_NONE, 'E': serial.PARITY_EVEN, 'O': serial.PARITY_ODD}
            parity_val = parity_map.get(parity.upper(), serial.PARITY_NONE)

            self.connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=data_bits,
                parity=parity_val,
                stopbits=stop_bits,
                timeout=timeout
            )

            self.port = port
            self.is_connected = True
            self._log(f"CONNECTED: {port} @ {baudrate} baud")
            return True, f"Connected to {port} at {baudrate} baud"

        except serial.SerialException as e:
            self.is_connected = False
            return False, f"Failed to connect: {str(e)}"
        except Exception as e:
            self.is_connected = False
            return False, f"Unexpected error during connection: {str(e)}"

    def disconnect(self) -> Tuple[bool, str]:
        """
        Close the current serial connection.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not self.is_connected or self.connection is None:
                return False, "No active connection to disconnect"

            self.connection.close()
            self.is_connected = False
            self._log("DISCONNECTED")
            self.connection = None
            self.port = None
            return True, "Disconnected successfully"

        except Exception as e:
            return False, f"Error during disconnect: {str(e)}"

    def send(self, data: str) -> Tuple[bool, str]:
        """
        Send data through the serial connection.
        
        Args:
            data: String data to send
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not self.is_connected or self.connection is None:
                return False, "Not connected to any port"

            self.connection.write(data.encode())
            self.connection.flush()
            self._log(f"TX: {repr(data)}")
            return True, f"Sent: {repr(data)}"

        except Exception as e:
            return False, f"Error sending data: {str(e)}"

    def receive(self, timeout: Optional[float] = None) -> Tuple[bool, str]:
        """
        Receive data from the serial connection.
        
        Args:
            timeout: Optional timeout in seconds. Uses connection timeout if not specified.
        
        Returns:
            Tuple of (success: bool, received_data: str or error_message: str)
        """
        try:
            if not self.is_connected or self.connection is None:
                return False, "Not connected to any port"

            if timeout is not None:
                self.connection.timeout = timeout

            if self.connection.in_waiting > 0:
                data = self.connection.read(self.connection.in_waiting)
                decoded = data.decode('utf-8', errors='replace')
                self._log(f"RX: {repr(decoded)}")
                return True, decoded
            else:
                return False, ""

        except Exception as e:
            return False, f"Error receiving data: {str(e)}"

    def read_until(self, expected: str, timeout: float = 2.0) -> Tuple[bool, str]:
        """
        Read data until the expected string is received or timeout occurs.
        
        Args:
            expected: String to wait for
            timeout: Timeout in seconds
        
        Returns:
            Tuple of (success: bool, received_data: str or error_message: str)
        """
        try:
            if not self.is_connected or self.connection is None:
                return False, "Not connected to any port"

            self.connection.timeout = timeout
            data = self.connection.read_until(expected.encode())
            decoded = data.decode('utf-8', errors='replace')
            self._log(f"RX: {repr(decoded)}")
            return True, decoded

        except serial.SerialTimeoutException:
            return False, f"Timeout waiting for: {repr(expected)}"
        except Exception as e:
            return False, f"Error reading data: {str(e)}"

    def get_connection_info(self) -> str:
        """
        Get information about the current connection.
        
        Returns:
            Connection info string or error message
        """
        if not self.is_connected or self.connection is None:
            return "Not connected"

        conn = self.connection
        return (
            f"Port: {conn.port}\n"
            f"Baudrate: {conn.baudrate}\n"
            f"Data bits: {conn.bytesize}\n"
            f"Parity: {conn.parity}\n"
            f"Stop bits: {conn.stopbits}\n"
            f"Timeout: {conn.timeout}s"
        )
