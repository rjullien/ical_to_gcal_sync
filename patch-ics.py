import fileinput
import sys

# Check that a filename was provided as a command-line argument
if len(sys.argv) < 2:
    print('Usage: python patch-ics.py <filename>')
    sys.exit(1)

# Get the filename from the command-line argument
filename = sys.argv[1]

# Specify the replacement value for X-WR-TIMEZONE
replacement = """BEGIN:VTIMEZONE
TZID:Europe/Paris
BEGIN:STANDARD
DTSTART:19710101T030000
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
END:STANDARD
END:VTIMEZONE"""

# Open the file for in-place editing
with fileinput.FileInput(filename, inplace=True) as file:
    # Loop over each line in the file
    for line in file:
        # Replace the X-WR-TIMEZONE property with the replacement value
        if line.startswith('X-WR-TIMEZONE:'):
            print(replacement)
        else:
            print(line, end='')