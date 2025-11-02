# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT
# ***** IF YOU UNCOMMENT LINE 211 THIS SHOULD GO FROM 10580 bytes free to MemoryError
# Modular Playground CircuitPython Euclidian Sequencer

DEV_MODE = True
# We use the gc library to check and manage available RAM during development
if DEV_MODE:
    import gc
    gc.collect()
    print("Starting free bytes (after gc) = " + str(gc.mem_free()))

from micropython import const

from algorithm import SequenceAlgorithm
from app import SequencerApp

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

############



# variables

channel_out = 1

############





app = SequencerApp(SequenceAlgorithm().update())
app.updateNeoPixels()

if DEV_MODE:
    gc.collect()
    print("Free bytes after object def and creation = " + str(gc.mem_free()))

app.main()

