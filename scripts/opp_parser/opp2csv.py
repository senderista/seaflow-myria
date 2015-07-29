#!/usr/bin/env python

import sys
import os
from binread import *

# EOL marker magic number (uint32)
EOL = 10
DATA_COLUMN_NAMES = ["time", "pulse_width", "D1", "D2", "fsc_small", "fsc_perp", "fsc_big", "pe", "chl_small", "chl_big"]
# 2 bytes for each column value (uint16), plus 4 bytes for EOL marker
ROW_SIZE_BYTES = (len(DATA_COLUMN_NAMES) * 2) + 4

if len(sys.argv) < 2:
    print >> sys.stderr, "Usage: opp2csv.py [--write-header] [--write-keys] <full path to OPP file>"
    sys.exit(1)

file_path = sys.argv[-1]
write_header = "--write-header" in sys.argv
write_keys = "--write-keys" in sys.argv

# file path looks like this: /misc/seaflow/Thompson_0/2009_312/142.evt.opp
cruise, year_day, file_name = file_path.split('/')[-3:]
file_id = file_name.split('.')[0]
KEY_COLUMN_NAMES = ["Cruise", "Day", "File_Id", "Cell_Id"]

reader = BinaryReader(file_path)
try:
    # get first 32-bit unsigned int representing number of records
    record_count = reader.read('uint32')
    # skip past following delimiter
    assert(reader.read('uint32') == EOL)
    print >> sys.stderr, "Record Count: ", record_count
    # verify record count corresponds to actual file size in bytes
    file_size = os.path.getsize(file_path)
    print >> sys.stderr, "File Size: ", file_size
    # include each row size in bytes plus initial record count (uint32)
    expected_size = 4 + (record_count * ROW_SIZE_BYTES)
    if expected_size != file_size:
        print >> sys.stderr, "Expected %d bytes, found %d bytes" % (expected_size, file_size)
        sys.exit(1)
    # print CSV header
    if write_header:
        COLUMN_NAMES = (KEY_COLUMN_NAMES if write_keys else []) + DATA_COLUMN_NAMES
        print ",".join(COLUMN_NAMES)
    # output each record in CSV format
    cell_id = 1
    while True:
        if write_keys:
            sys.stdout.write(",".join([cruise, year_day, file_id, str(cell_id)]) + ",")
        for i in xrange(len(DATA_COLUMN_NAMES)):
            sys.stdout.write(str(reader.read('uint16')))
            if i < (len(DATA_COLUMN_NAMES) - 1):
                sys.stdout.write(",")
            else:
                sys.stdout.write("\n")
        # delimiter will appear after each record except at EOF
        delimiter = reader.read('uint32')
        # if we got here, we haven't reached EOF, so check delimiter for correctness
        assert(delimiter == EOL)
        cell_id += 1
except BinaryReaderEOFException:
    # The normal EOF case.
    if reader.tell() == file_size:
        sys.exit(0)
    else:
        print >> sys.stderr, "Error: %s is corrupted!" % file_path
        sys.exit(1)
