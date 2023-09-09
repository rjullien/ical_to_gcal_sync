import fileinput
import os
import sys

# Check that a directory was provided as a command-line argument
if len(sys.argv) < 2:
    print('Usage: python patch-ics.py <directory>')
    sys.exit(1)

# Get the directory from the command-line argument
directory = sys.argv[1]

# Specify the replacement value for X-WR-TIMEZONE
replacement = """BEGIN:VTIMEZONE
TZID:Europe/Paris
BEGIN:STANDARD
DTSTART:19710101T030000
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
END:STANDARD
END:VTIMEZONE"""

# Loop over each file in the directory
for filename in os.listdir(directory):
    # Check that the file has a .ics extension
    if filename.endswith('.ics'):
        # Open the file for in-place editing
        with fileinput.FileInput(os.path.join(directory, filename), inplace=True) as file:
            # Loop over each line in the file
            for line in file:
                # Replace the X-WR-TIMEZONE property with the replacement value
                if line.startswith('X-WR-TIMEZONE:'):
                    print(replacement)
                else:
                    print(line, end='')