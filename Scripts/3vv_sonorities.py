# Three-Voice Sonorities 

# Makes a table with different interval types based on output from 
# Rodan-client Vertical Interval Indexer. Works with any number of three-voice motets.

# Determines sonority based on first two intervals *or* the only one that exists.  
# A line that is all `'Rest'`s indicates a solo or silence and is classified as `None`.

# author: Emily Hopkins <emily.hopkins@mcgill.ca>

from enum import Enum
import fileinput


class IntervalType(Enum):
    perfect = 1
    mixed = 2
    imperfect = 3
    doubly_imperfect = 4
    dissonant = 5
    

def getlines():
    """
    Retrieves lines from csv file with file name and line number.
    """
    with fileinput.input() as f:
        for line in f:
            yield f.filename(), f.filelineno(), line


def intervalsfromlines(lines):
    """
    Takes a sequence of lines and offset numbers (output of getlines) and returns     
    intervals from each line. Assumes that the lines come from CSV files generated by 
    Rodan-client, so skips over the first three lines that do not have intervals.
    
    Accounts for voice-crossing so that the interval types rules that follow are applied
    to only the remaining pair of intervals emitted.
    """
    for filename, filelineno, line in lines:
        if filelineno >= 4:
            s, a, t = line.strip().split(',')[1:]
            if any(x == 'Rest' for x in (s, a, t)):
                # This should always yield just one interval or no intervals.
                intv = tuple(x for x in (s, a, t) if x != 'Rest')
                assert len(intv) <= 1
                yield intv
            # if S (0) is lowest sounding voice, use first two columns
            elif '-' in s and '-' in a:
                yield tuple(sorted((s, a)))
            # if A (1) is lowest-sounding voice, use first and third columns
            elif '-' not in s and '-' in t:
                yield tuple(sorted((s, t)))
            #if T (2) is lowest-sounding voice, use second and third columns
            else:
                yield tuple(sorted((a, t)))


def intervaltype(intv):
    """
    Defines interval types after Fuller (1986).
    """
    if len(intv) == 0:
        return None
    #fintv 'flattens' interval from tuple to make list comprehensions simpler
    fintv = ''.join(intv)
    for x in ['d', 'A', '2', '7', '4']:
        if any (x in y for y in intv):
            return IntervalType.dissonant
    if '5' in fintv and '6' in fintv:
            return IntervalType.dissonant
    if all('P' in x for x in intv):
        return IntervalType.perfect
    if '3' in fintv and '6' in fintv:
        return IntervalType.doubly_imperfect
    if (('3' in fintv or '6' in fintv)
            and not ('5' in fintv or '8' in fintv)):
        return IntervalType.imperfect
    else:
        return IntervalType.mixed
    assert False

#Makes a table

table = {}                
for intv in intervalsfromlines(getlines()):
    it = intervaltype(intv)
    print(intv, it)
    table.setdefault(it, 0)
    table[it] += 1
for k, v in sorted(table.items(), key=lambda x: x[1], reverse=True):
    print(k, v)
