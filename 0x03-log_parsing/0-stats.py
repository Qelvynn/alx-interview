#!/usr/bin/python3
import sys
import signal

# Dictionary to keep track of the status code counts
status_counts = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
total_size = 0
line_count = 0

def print_stats():
    """Prints the current statistics."""
    print("File size: {}".format(total_size))
    for code in sorted(status_counts.keys()):
        if status_counts[code] > 0:
            print("{}: {}".format(code, status_counts[code]))

def signal_handler(sig, frame):
    """Handles a keyboard interruption (CTRL + C)."""
    print_stats()
    sys.exit(0)

# Set up the signal handler for keyboard interruption (CTRL + C)
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        # Split the line into parts
        parts = line.split()

        # Validate the format of the input
        if len(parts) < 9 or parts[5] != '"GET' or parts[6] != '/projects/260' or parts[7] != 'HTTP/1.1"':
            continue

        # Extract the status code and file size
        try:
            status_code = int(parts[8])
            file_size = int(parts[9])
        except (ValueError, IndexError):
            continue

        # Update the total size and status code count
        total_size += file_size
        if status_code in status_counts:
            status_counts[status_code] += 1

        # Increment the line counter and check if we need to print stats
        line_count += 1
        if line_count % 10 == 0:
            print_stats()

except KeyboardInterrupt:
    print_stats()
    sys.exit(0)

