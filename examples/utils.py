import os
import subprocess
import threading
from typing import Optional, Any

def clean_code(code: str, last: bool = True) -> str:
    """Removes delimiteres such as ```python ... ``` from a code snippet.
    
    Args:
        code: The code to clean.
        last: Whether to extract the last code snippet or the first, if there are multiple options.
    """
    lines = code.split("\n")
    lines = lines[::-1] if last else lines
    for i, line in enumerate(lines):
        if "```" in line:
            lines = lines[i+1:]
            break
    for i, line in enumerate(lines):
        if "```" in line:
            lines = lines[:i]
            break
    lines = lines[::-1] if last else lines
    return "\n".join(lines)

class TimeoutError(Exception):
    """Costum exception for shell timeout errors in the Shell class.

    Attributes:
        output (str): The shell output until the TimeoutError was raised.
        timeout (float): The timeout in seconds that was reached.
    """

    def __init__(self, output: str, timeout: float, message: str):
        super().__init__(message)
        self.output = output
        self.timeout = timeout

class Shell:
    """Represents an interactive shell. Commands can be send via the send method.
    Needs to be shutdown manually if not opened in a with block."""
    _command_end = "COMMAND FINISHED"  # Identifier for recognizing when a shell command has finished
    _reading_size = 2**32  # Non-blocking read size that is read from the shell output stream. Should be big enough such that command_end is not cut off by chance.

    def __init__(self, **kwargs: Any):
        """Starts the shell.

        Args:
            kwargs: Arguments to be passed to the shell process.
        """
        self._kwargs = kwargs
        self._output = ""
        self._alive = False
        self._startup()

    def send(self, command: str = "", timeout: Optional[float] = None) -> str:
        """Sends a command to an interactive shell, and returns the output.
        
        Args:
            timeout: How long (in seconds) the shell should run until a TimeoutError is raised.
                The shell runs indefinitely, if set to None.
        """
        print(f"RUNNING COMMAND: {command}")
        if not self._alive:
            self._startup()

        if self._command_done.wait(timeout=0):
            self._command_done.clear()
            # possible race conditions
            echo = f"echo \"{Shell._command_end}\""
            if command.strip() != "":
                command = f"{command};{echo}"
            else:
                command = echo
        self._process.stdin.write(command + "\n")
        self._process.stdin.flush()

        finished = self._command_done.wait(timeout=timeout)
        output, self._output = self._output.strip(), self._rest
        if not finished and timeout is not None:
            raise TimeoutError(output, timeout, f"Shell timed out after {timeout} seconds")
        return output

    def shutdown(self, timeout: float = 10) -> None:
        """Shuts down the interactive shell.

        Args:
            timeout: How long to wait until a forcefull termination is initiated.
        """
        if not self._alive:
            return
        self._alive = False

        if self._process.stdin:
            self._process.stdin.close()
        if self._process.stdout:
            self._process.stdout.close()
        self._process.terminate()
        
        try:
            self._process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self._process.kill()
            self._process.wait()
        self._output_thread.join()

    def _startup(self):
        """Starts up the shell."""
        self._alive = True

        self._process = subprocess.Popen(
            ['/bin/bash'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
            text=True,
            **self._kwargs
        )
        self._fileno = self._process.stdout.fileno()
        self._output = ""
        self._rest = ""
        self._command_done = threading.Event()  # Event to signal command completion
        self._command_done.set()
        self._output_thread = threading.Thread(target=self._read_output, daemon=True)
        self._output_thread.start()

    def _read_output(self):
        """Runs in a seperate thread to wait for output from the shell."""
        end = Shell._command_end + "\n"
        while self._process.poll() is None:
            data = os.read(self._fileno, Shell._reading_size)
            if not data:
                break

            text = data.decode("utf-8")
            self._output += text
            print(text, end="")
            if end in self._output:
                left, right = self._output.split(end, 1)
                self._output = left
                self._rest = right
                self._command_done.set()
                continue

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown()