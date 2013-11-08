siteswap-states
===============

Very simple python code for creating SVG state graphs.

The program outputs a graphviz .dot file.
It can be converted using dot into various formats.
The Makefile will run states.py and then dot, creating both
.dot and .svg files.

The command line in the Makefile is:
    ./states.py --balls=3 --maxThrow=5 --pattern=51 > states.dot

Note that the three arguments (balls, maxThrow, pattern) must
be consistent.
