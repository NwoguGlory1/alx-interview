#!/usr/bin/python3
"""
Script to read stdin line by line and compute metrics.
"""
import sys
import signal

total_file_size = 0
status_count = {}
status_codes = {200, 301, 400, 401, 403, 404, 405, 500}
line_count = 0

def print_statistics():
    """Prints statistics when a keyboard interruption occurs or every 10 lines."""
    print("File size: {}".format(total_file_size))
    for code in sorted(status_count.keys()):
        if status_count[code] > 0:
            print("{}: {}".format(code, status_count[code]))

def signal_handler(sig, frame):
    """Handles the keyboard interruption (CTRL + C)."""
    print_statistics()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        line_count += 1
        
        parts = line.split()
        if len(parts) < 7:
            continue
        
        ip, dash, date, request, protocol, status_code, file_size = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        
        try:
            status_code = int(status_code)
            if status_code in status_codes:
                file_size = int(file_size)
                total_file_size += file_size
                if status_code in status_count:
                    status_count[status_code] += 1
                else:
                    status_count[status_code] = 1
        except ValueError:
            continue
        
        if line_count % 10 == 0:
            print_statistics()

except Exception as e:
    print("An error occurred: {}".format(e), file=sys.stderr)

finally:
    print_statistics()
