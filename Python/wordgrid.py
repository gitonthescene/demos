#!/usr/bin/env python3

from collections import defaultdict

def main():
    with open( "/dev/stdin" ) as f:
        words = [ w.strip() for w in f ]

    bylettercount = defaultdict( lambda: defaultdict( set ) )
    bycount = defaultdict( set )
    twoletter = defaultdict( lambda: defaultdict( set ) )
    pangrams = set()
    samplepan = None
    points = 0

    for word in words:
        bylettercount[ word[0].upper() ][ len(word) ].add( word )
        bycount[ len(word) ].add( word )
        twoletter[word[0].upper()][ word[:2].upper() ].add( word )
        if len(set(word)) == 7:
            pangrams.add( word )
            points += 7
            samplepan = word

        points += 1 if len(word) == 4 else len(word)

    counts = sorted(set(sum( (list( x.keys() ) for x in bylettercount.values()), [] ) ) )

    print( "SPELLING BEE GRID\n" )
    print( " ".join( sorted( x for x in set(samplepan.upper()) ) ) )
    out = "\nWORDS: %d, POINTS: %d, PANGRAMS: %d" % ( len(words), points, len(pangrams) )
    perfect = [ x for x in pangrams if len(x) == 7 ]
    if perfect:
        out += " (%s Perfect)" % ( perfect, )
    if len( bylettercount ) == 7:
        out += ", BINGO"

    out += "\n\nGrid:\n\n"
    out += "".join( ("\t%3d" % ( c, ) for c in counts) ) + "\tTOT\n"
    for letter in bylettercount:
        out += "%3s:" % ( letter, )
        for cnt in counts:
            out += "\t%3d" % ( len(bylettercount[letter][cnt]), ) if cnt in bylettercount[letter] else "\t"
        out += "\t%3d" % ( sum( len(bylettercount[letter][cnt]) for cnt in counts ), )+ "\n"

    out += "TOT:"+ "".join( "\t%3d" % ( len(c), ) for _,c in sorted(bycount.items()) ) + ("\t%3d" % (len(words),)) +"\n"

    print( out )

    print( "\nTwo letter list:" )
    for _, tlmap in twoletter.items():
        print( " ".join( "%s-%d" % ( k, len(v)) for k, v in sorted(tlmap.items()) ) )

if __name__ == "__main__":
    main()
