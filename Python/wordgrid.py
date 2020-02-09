#!/usr/bin/env python3

from collections import defaultdict
import sys

def main( center ):
    with open( "/dev/stdin" ) as f:
        words = [ w.strip() for w in f ]

    bylettercount = defaultdict( lambda: defaultdict( lambda: 0 ) )
    bycount = defaultdict( lambda: 0 )
    byletter = defaultdict( lambda: 0 )
    twoletter = defaultdict( lambda: defaultdict( lambda: 0 ) )
    pangrams = set()
    samplepan = None
    points = 0

    for word in words:
        bylettercount[ word[0].upper() ][ len(word) ] += 1
        bycount[ len(word) ] += 1
        byletter[ word[0].upper() ] += 1
        twoletter[word[0].upper()][ word[:2].upper() ] += 1
        if len(set(word)) == 7:
            pangrams.add( word )
            points += 7
            samplepan = word

        points += 1 if len(word) == 4 else len(word)

    counts = sorted(set(sum( (list( x.keys() ) for x in bylettercount.values()), [] ) ) )

    print( "SPELLING BEE GRID\n" )
    print( center.upper() + " " + " ".join( sorted( x for x in set(samplepan.upper()).difference([center]) ) ) )
    out = "\nWORDS: %d, POINTS: %d, PANGRAMS: %d" % ( len(words), points, len(pangrams) )
    perfect = [ x for x in pangrams if len(x) == 7 ]
    if perfect:
        out += " (%s Perfect)" % ( perfect, )
    if len( bylettercount ) == 7:
        out += ", BINGO"

    print( "\nFirst character frequency:\n")
    print( "\n".join( "%s x %d" % (l,f) for l,f in sorted(byletter.items()) ) )

    print( "\nWord length frequency:\n")
    print( "\n".join( "%sL: %d" % (c,f) for c,f in sorted(bycount.items()) ) )

    out += "\n\nGrid:\n\n"
    out += "".join( ("\t%3d" % ( c, ) for c in counts) ) + "\tTOT\n"
    for letter in bylettercount:
        out += "%3s:" % ( letter, )
        for cnt in counts:
            out += "\t%3d" % ( bylettercount[letter][cnt], ) if cnt in bylettercount[letter] else "\t  -"
        out += "\t%3d" % ( byletter[letter], )+ "\n"

    out += "TOT:"+ "".join( "\t%3d" % ( c, ) for _,c in sorted(bycount.items()) ) + ("\t%3d" % (len(words),)) +"\n"

    print( out )

    print( "\nTwo letter list:\n" )
    for _, tlmap in twoletter.items():
        print( " ".join( "%s-%d" % (k, v) for k, v in sorted(tlmap.items()) ) )

if __name__ == "__main__":
    main( sys.argv[1] )
