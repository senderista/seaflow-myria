#!/usr/bin/env python

import sys
import os
from binread import *

# EOL marker magic number (uint32)
EOL = 10
COLUMN_NAMES = ["time", "pulse_width", "D1", "D2", "fsc_small", "fsc_perp", "fsc_big", "pe", "chl_small", "chl_big"]
# 2 bytes for each column value (uint16), plus 4 bytes for EOL marker
ROW_SIZE_BYTES = (len(COLUMN_NAMES) * 2) + 4

file_name = sys.argv[1]
reader = BinaryReader(file_name)
try:
    # get first 32-bit unsigned int representing number of records
    record_count = reader.read('uint32')
    # skip past following delimiter
    assert(reader.read('uint32') == EOL)
    print >> sys.stderr, "Record Count: ", record_count
    # verify record count corresponds to actual file size in bytes
    file_size = os.path.getsize(file_name)
    print >> sys.stderr, "File Size: ", file_size
    # include each row size in bytes plus initial record count (uint32)
    expected_size = 4 + (record_count * ROW_SIZE_BYTES)
    if expected_size != file_size:
        print >> sys.stderr, "Expected %d bytes, found %d bytes" % (expected_size, file_size)
        sys.exit(1)
    # print CSV header
    print ",".join(COLUMN_NAMES)
    # output each record in CSV format
    while True:
        for i in xrange(len(COLUMN_NAMES)):
            sys.stdout.write(str(reader.read('uint16')))
            if i < (len(COLUMN_NAMES) - 1):
                sys.stdout.write(",")
            else:
                sys.stdout.write("\n")
        # delimiter will appear after each record except at EOF
        delimiter = reader.read('uint32')
        # if we got here, we haven't reached EOF, so check delimiter for correctness
        assert(delimiter == EOL)
except BinaryReaderEOFException:
    # The normal EOF case.
    if reader.tell() == file_size:
        sys.exit(0)
    else:
        print >> sys.stderr, "Error: %s is corrupted!" % file_name
        sys.exit(1)
