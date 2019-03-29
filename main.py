#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File to run to test the main program.
"""

import phystech
from phystech import file

testFile = phystech.EXAMPLEFILES[0]
print(testFile)

f = file.File(testFile)
print(f)

