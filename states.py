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
    def __init__(self, options):
        self.nBalls = options.nBalls
        self.maxThrow = options.maxThrow
        self.states = {}
        self.ComputeStates()
        if options.pattern:
            self.IsValidPattern(options.pattern)
            print >> sys.stderr, self.StartState(options.pattern)


    def StartState(self, pattern):
        assert self.IsValidPattern(pattern)
        pat = PatternStrToList(pattern)
        stateVec = [None for i in range(2*self.maxThrow)]
        for i in range(self.maxThrow):
            p = pat[i % len(pat)]
            if p==0:
                if stateVec[i]:
                    return None
                stateVec[i] = empty
            elif stateVec[i] == None:
                stateVec[i] = inhand
                if stateVec[i+p]:
                    return None
                stateVec[i+p] = empty
            elif stateVec[i] == empty:
                if stateVec[i+p]:
                    return None
                stateVec[i+p] = empty
        return ''.join(stateVec[:self.maxThrow])


    def IsValidPattern(self, pattern):
        min = '0'
        max = chr(ord(min) + self.maxThrow)
        for p in pattern:
            if p < min or p > max:
                print p, "is not a valid throw"
                return False
        pat = PatternStrToList(pattern)
        if sum(pat) != len(pat) * self.nBalls:
            print "Pattern doesn't average", self.nBalls, "balls"
            return False
        return True

    def BaseState(self):
        return inhand*self.nBalls + empty*(self.maxThrow-self.nBalls)

    def ComputeStates(self):
        todo = set()
        done = set()
        todo.add(self.BaseState())

        while todo:
            state = todo.pop()
            done.add(state)

            if state in self.states:
                transitions = self.states[state]
            else:
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

    def Weight(self, throw):
        # Dot causes edges with heavier weights to be drawn shorter and straighter
        if throw == 0:
            return 0
        else:
            t = abs(self.nBalls - throw)
            t = self.maxThrow - t
            return t*t*t
#            return (self.nBalls - throw) * (self.nBalls - throw)
#            return float(self.maxThrow - throw) / self.maxThrow

    def PrintDot(self):
        print "Digraph states {"
        print "rankdir=LR;"
        for fromState in reversed(sorted(self.states.keys())):
            transitions = self.states[fromState]
            for throw in sorted(transitions.keys()):
                fromLabel = Quoted(fromState)
                toLabel = Quoted(transitions[throw])
                edgeLabel = Quoted(throw)
                weight = self.Weight(throw)
                print fromLabel, "->", toLabel, "[label="+edgeLabel, "weight="+str(weight)+"];"
        print "}"

parser = OptionParser()
parser.add_option("-b", "--balls", dest="nBalls", type="int", default=3, help="Number of balls being juggled")
parser.add_option("-m", "--maxThrow", dest="maxThrow", type="int", default=5, help="Maximum throw height")
parser.add_option("-p", "--pattern", dest="pattern", type="str", help="Siteswap pattern to highlight")
(options, args) = parser.parse_args()

if options.pattern:
    pat = PatternStrToList(options.pattern)
    nBalls = sum(pat) / len(pat)
    if sum(pat) != len(pat) * nBalls:
        sys.exit("Illegal pattern.")
    maxThrow = max(pat)


siteSwapStates = SiteSwapStates(options)
siteSwapStates.PrintDot()



