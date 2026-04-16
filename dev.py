# dev.py
# Developer scripting and functions for testing and debugging.
# Runs predefined test sequences from dev.json against connected serial devices.

import json
import time
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from serial_core import SerialCommunicator


class DevTestRunner:
    """
    Executes test sequences defined in dev.json against a serial connection.
    """

    def __init__(self, dev_json_path: str, dev_key: str = ""):
        """
        Initialize the dev test runner.
        
        Args:
            dev_json_path: Path to dev.json file
            dev_key: Developer key for dev mode access
        """
        self.dev_json_path = dev_json_path
        self.dev_key_configured = ""
        self.dev_config: Dict = {}
        self.serial_comm: Optional[SerialCommunicator] = None
        self.load_dev_config()
        
        if dev_key:
            self.set_dev_key(dev_key)

    def load_dev_config(self) -> Tuple[bool, str]:
        """
        Load the dev.json configuration file.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with open(self.dev_json_path, 'r') as f:
                self.dev_config = json.load(f)
            return True, "Dev config loaded successfully"
        except FileNotFoundError:
            return False, f"dev.json not found at {self.dev_json_path}"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON in dev.json: {str(e)}"
        except Exception as e:
            return False, f"Error loading dev.json: {str(e)}"

    def set_dev_key(self, key: str) -> Tuple[bool, str]:
        """
        Set and validate the developer key.
        
        Args:
            key: Developer key to validate
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        expected_key = self.dev_config.get("DEV_KEY", "")
        if key == expected_key:
            self.dev_key_configured = key
            return True, "Dev mode enabled"
        else:
            return False, "Invalid developer key"

    def is_dev_enabled(self) -> bool:
        """Check if dev mode is enabled."""
        return self.dev_key_configured != ""

    def set_serial_communicator(self, serial_comm: SerialCommunicator) -> None:
        """Set the serial communicator instance."""
        self.serial_comm = serial_comm

    def list_tests(self) -> Tuple[bool, List[Dict]]:
        """
        List all available tests.
        
        Returns:
            Tuple of (success: bool, tests_list: List[Dict])
        """
        try:
            tests = self.dev_config.get("TESTS", [])
            if not tests:
                return False, "No tests found in dev.json"
            return True, tests
        except Exception as e:
            return False, f"Error listing tests: {str(e)}"

    def find_test_by_name(self, test_name: str) -> Optional[Dict]:
        """
        Find a test by name (case-insensitive).
        
        Args:
            test_name: Name of the test to find
        
        Returns:
            Test dictionary or None if not found
        """
        tests = self.dev_config.get("TESTS", [])
        for test in tests:
            if test.get("NAME", "").upper() == test_name.upper():
                return test
            # Also check by index
            if test_name.isdigit() and int(test_name) < len(tests):
                return tests[int(test_name)]
        return None

    def run_test(
        self,
        test_name: str,
        count: int = 1,
        delay_ms: int = 0,
        verbose: bool = True
    ) -> Tuple[bool, str]:
        """
        Run a specific test sequence.
        
        Args:
            test_name: Name of the test to run
            count: Number of times to run the test
            delay_ms: Delay between runs in milliseconds
            verbose: Print detailed output
        
        Returns:
            Tuple of (success: bool, result_message: str)
        """
        if not self.is_dev_enabled():
            return False, "Dev mode not enabled. Enter dev key first."

        if not self.serial_comm or not self.serial_comm.is_connected:
            return False, "Not connected to a serial port"

        test = self.find_test_by_name(test_name)
        if not test:
            return False, f"Test '{test_name}' not found"

        result_messages = []
        total_passed = 0
        total_failed = 0

        for run_num in range(count):
            if verbose and count > 1:
                result_messages.append(f"\n--- Run {run_num + 1}/{count} ---")

            success, message, passed, failed = self._execute_test_sequence(test, verbose)
            total_passed += passed
            total_failed += failed

            result_messages.append(message)

            if run_num < count - 1 and delay_ms > 0:
                time.sleep(delay_ms / 1000.0)

        # Summary
        summary = f"\nTest '{test.get('NAME')}' completed: {total_passed} passed, {total_failed} failed"
        if total_failed == 0:
            summary += " ✓"
        else:
            summary += " ✗"

        result_messages.append(summary)
        return total_failed == 0, "\n".join(result_messages)

    def _extract_trace_data(self, data: str, trace_config: Dict) -> Optional[str]:
        """
        Extract traced data from a string based on trace configuration.
        
        Args:
            data: Raw data from device
            trace_config: Dict with KEY, TRACE_CHAR, TRACE_END
        
        Returns:
            Extracted trace data or None if KEY not found
        """
        key = trace_config.get("KEY", "")
        trace_char = trace_config.get("TRACE_CHAR", "")
        trace_end = trace_config.get("TRACE_END", "\n")

        if key not in data:
            return None

        # Find where KEY starts
        key_index = data.find(key)
        if key_index == -1:
            return None

        # Start after KEY and trace_char
        start_index = key_index + len(key)
        if start_index >= len(data):
            return None

        # Skip the TRACE_CHAR
        if trace_char and data[start_index:start_index + len(trace_char)] == trace_char:
            start_index += len(trace_char)

        # Find the end marker
        end_index = data.find(trace_end, start_index)
        if end_index == -1:
            end_index = len(data)

        return data[start_index:end_index]

    def _execute_test_sequence(self, test: Dict, verbose: bool = True) -> Tuple[bool, str, int, int]:
        """
        Execute a test sequence step by step with immediate TX on RX detection.
        
        Args:
            test: Test dictionary containing SEQUENCE
            verbose: Print detailed output
        
        Returns:
            Tuple of (success: bool, message: str, passed: int, failed: int)
        """
        sequence = test.get("SEQUENCE", [])
        if not sequence:
            return False, "Test has no sequence defined", 0, 0

        messages = []
        passed = 0
        failed = 0
        state_index = 0

        while state_index < len(sequence):
            step = sequence[state_index]
            tx_data = step.get("TX", "")
            rx_expected = step.get("RX", "")

            # Send data
            if tx_data:
                success, msg = self.serial_comm.send(tx_data)
                if not success:
                    messages.append(f"  State {state_index}: Send FAILED - {msg}")
                    failed += 1
                    state_index += 1
                    continue
                elif verbose:
                    messages.append(f"  State {state_index}: TX → {repr(tx_data)}")

            # Receive and validate
            if rx_expected:
                time.sleep(0.05)  # Reduced delay for faster response
                success, rx_data = self.serial_comm.read_until(rx_expected, timeout=2.0)

                if success:
                    messages.append(f"  State {state_index}: RX ✓ {repr(rx_data)}")
                    passed += 1
                else:
                    messages.append(f"  State {state_index}: RX ✗ Expected {repr(rx_expected)}")
                    failed += 1

            state_index += 1

        # Handle traces if present
        traces = test.get("TRACES", [])
        if traces and verbose:
            messages.append(f"\n  Traces ({len(traces)} items detected):")
            for trace_idx, trace_config in enumerate(traces):
                key = trace_config.get("KEY", "")
                trace_char = trace_config.get("TRACE_CHAR", "")
                trace_end = trace_config.get("TRACE_END", "\\n")
                messages.append(f"    [{trace_idx}] KEY: {repr(key)} | CHAR: {repr(trace_char)} | END: {repr(trace_end)}")

        return failed == 0, "\n".join(messages), passed, failed

    def run_all_tests(
        self,
        delay_ms: int = 500,
        verbose: bool = True
    ) -> Tuple[bool, str]:
        """
        Run all tests in sequence.
        
        Args:
            delay_ms: Delay between tests
            verbose: Print detailed output
        
        Returns:
            Tuple of (success: bool, result_message: str)
        """
        if not self.is_dev_enabled():
            return False, "Dev mode not enabled."

        success, tests = self.list_tests()
        if not success:
            return False, f"Cannot run tests: {tests}"

        result_messages = [f"Running {len(tests)} tests...\n"]
        total_passed = 0
        total_failed = 0

        for test_index, test in enumerate(tests):
            test_name = test.get("NAME", f"Test {test_index}")
            result_messages.append(f"\n[TEST {test_index + 1}/{len(tests)}] {test_name}")
            result_messages.append(f"Description: {test.get('DESCRIPTION', 'N/A')}")

            success, msg, passed, failed = self._execute_test_sequence(test, verbose)
            total_passed += passed
            total_failed += failed

            result_messages.append(msg)

            if test_index < len(tests) - 1 and delay_ms > 0:
                time.sleep(delay_ms / 1000.0)

        # Final summary
        result_messages.append(f"\n{'=' * 50}")
        result_messages.append(f"FINAL RESULTS: {total_passed} passed, {total_failed} failed")
        result_messages.append("=" * 50)

        return total_failed == 0, "\n".join(result_messages)
