import subprocess
import time
import os
import sys

def clear_terminal(max_attempt=3, delay=1):
    """
    Clears terminal with transient error retries.
    Args:
        max_retries: Maximum attempts before failing (default: 3)
        retry_delay: Seconds between retries (default: 1)
    Raises:
        subprocess.CalledProcessError: If all retries fail
    """
    for _ in range(max_attempt):
        try:
            # Run OS-specific clear command:
            # - cmd /c cls (Windows)
            # - clear (Unix/Mac)
            subprocess.run(
                ["cmd", "/c", "cls"] if os.name == "nt" else ["clear"], check=True # Raise exception if command fails
            )
            print("Terminal cleared. \n'autoclear stop' to stop. \n'autoclear status' to check status.")
           
          
            # time.sleep(delay)
            return
        except subprocess.CalledProcessError:
            pass


def autoclear(interval=600):
    """
    Main loop that clears terminal at fixed intervals.
    Args:
        interval: Seconds between clears (pre-validated by controller)
    """
    while True: # Infinite loop (managed by controller
        clear_terminal()
        time.sleep(interval)


if __name__ == "__main__":
          
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    time.sleep(2)
    autoclear(interval)