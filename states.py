#!/usr/bin/python

import sys
from optparse import OptionParser

empty = '-'
inhand = 'x'

def Quoted(s):
    """Return the string s within quotes."""
    return '"' + str(s) + '"'

def PatternStrToList(pattern):
    """Return a list of integers for the given pattern string.
    PatternStrToList('531') -> [5, 3, 1]
    """
    return [ord(p)-ord('0') for p in pattern]

def PatternListToStr(pattern):
    """Return a pattern string for the given list of integers.
    PatternListToStr([5,3,1]) -> '531'
    """
    return ''.join([chr(p) for p in pattern])

class SiteSwapStates:
    """A class that contains a state space graph for siteswap juggling for a given number
    of balls and a maximum throw height."""

    def __init__(self, options):
        """The primary data structure is the states dictionary. The keys of the states dict are state strings,
        e.g. 'xxx--'. The value for any such key is a dictionary that stores all valid transitions
        from the key state. Using 3 balls with max throw of 5, the base state is 'xxx--'. self.states['xxx--']
        is a dictionary containing the two valid transitions: {4: 'xx-x-', 5: 'xx--x'}."""

        self.nBalls = options.nBalls
        self.maxThrow = options.maxThrow
        self.states = {}
        self.ComputeStates()

    def BaseState(self):
        """Return the base state for the given nBalls and maxThrow.
        E.g. for 3 balls max throw 5 the base state is 'xxx--'."""
        return inhand*self.nBalls + empty*(self.maxThrow-self.nBalls)

    def ComputeStates(self):
        """Compute the entire state space graph"""

        todo = set()    # The set of states for which transitions have not yet been calculated.
        done = set()    # The set of states for which transitions have already been calculated.

        # start with the base state, although we could start with any valid state.
        todo.add(self.BaseState())

        while todo:
            state = todo.pop()
            done.add(state)

            assert state not in self.states
            transitions = {}
            self.states[state] = transitions

            now = state[0]
            assert now==inhand or now==empty
            canthrow = now==inhand

            newstate = state[1:] + empty

            if not canthrow:
                transitions[0] = newstate
            else:
                for i in range(self.maxThrow):
                    if newstate[i] == empty:
                        t = list(newstate)
                        t[i] = inhand
                        s = ''.join(t)
                        transitions[i+1] = s
                        if s not in done:
                            todo.add(s)

    def PrintStates(self):
        for state in reversed(sorted(self.states.keys())):
            transitions = self.states[state]
            print "Transitions for", state, "are:", transitions

    def PrintDot(self):
        print "Digraph states {"
        print "rankdir=LR;"
        for fromState in reversed(sorted(self.states.keys())):
            transitions = self.states[fromState]
            for throw in sorted(transitions.keys()):
                fromLabel = Quoted(fromState)
                toLabel = Quoted(transitions[throw])
                edgeLabel = Quoted(throw)
                print "%s -> %s [label=%s]" % (fromLabel, toLabel, edgeLabel)
        print "}"

parser = OptionParser()
parser.add_option("-b", "--balls", dest="nBalls", type="int", default=3, help="Number of balls being juggled")
parser.add_option("-m", "--maxThrow", dest="maxThrow", type="int", default=5, help="Maximum throw height")
(options, args) = parser.parse_args()

siteSwapStates = SiteSwapStates(options)
siteSwapStates.PrintDot()



