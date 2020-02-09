#!/usr/bin/env python3

from collections import defaultdict

def main():
    with open( "/dev/stdin" ) as f:
        words = [ w.strip() for w in f ]

    bylettercount = defaultdict( lambda: defaultdict( set ) )
    bycount = defaultdict( set )
    pangrams = set()
    points = 0
    
    for word in words:
        bylettercount[ word[0].upper() ][ len(word) ].add( word )
        bycount[ len(word) ].add( word )
        if len(set(word)) == 7:
            pangrams.add( word )
            points += 7
        points += 1 if len(word) == 4 else len(word)

    counts = sorted(set(sum( (list( x.keys() ) for x in bylettercount.values()), [] ) ) )

    out = "WORDS %d, POINTS %d, PANGRAMS: %d" % ( len(words), points, len(pangrams) )
    perfect = [ x for x in pangrams if len(x) == 7 ]
    if perfect:
        out += " (%s PERFECT)" % ( perfect, )
    if len( bylettercount ) == 7:
        out += ", BINGO"

    out += "\n\nGrid:\n\n"
    out += "".join( ("\t%3d" % ( c, ) for c in counts) ) + "\tTOT\n"
    for letter in bylettercount:
        out += "%3s:" % ( letter, )
        for cnt in counts:
            out += "\t%3d" % ( len(bylettercount[letter][cnt]), ) if cnt in bylettercount[letter] else "\t"
        out += "\t%3d" % ( sum( len(bylettercount[letter][cnt]) for cnt in counts ), )+ "\n"

    out += "TOT:"+ "".join( "\t%3d" % ( len(c), ) for _,c in sorted(bycount.items()) ) + "\n"

    print( out )

if __name__ == "__main__":
    main()
