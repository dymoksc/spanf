#!/usr/bin/env python

"""
Sample raw data transformer. Outputs to the STDOUT number of bytes received on the STDIN.
"""

import sys

data = sys.stdin.read()

print(len(data))