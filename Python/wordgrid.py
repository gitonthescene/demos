#!/usr/bin/env python3

from collections import defaultdict
from xml.sax.handler import ContentHandler
import xml.sax
import json
import urllib.request

class BeeHandler( ContentHandler ):
    def __init__( self ):
        self.chars = None
        self.answer = None

    def startElement( self, name, attrs ):
        if self.answer: return
        meth = getattr( self, "start"+name.capitalize(), None )
        if meth: meth( attrs )

    def endElement( self, name ):
        if self.answer: return
        meth = getattr( self, "end"+name.capitalize(), None )
        if meth: meth()

    def startScript( self, attrs ):
        self.chars = ""

    def endScript( self ):
        self.answer = self.chars
        self.chars = None

    def characters( self, content ):
        if self.chars is not None:
            self.chars += content

def solve( center, words ):

    bylettercount = defaultdict( lambda: defaultdict( lambda: 0 ) )
    bycount = defaultdict( lambda: 0 )
    byletter = defaultdict( lambda: 0 )
    twoletter = defaultdict( lambda: defaultdict( lambda: 0 ) )
    pangrams = set()
    samplepan = None
    points = 0

    for word in words:
        bylettercount[ word[0] ][ len(word) ] += 1
        bycount[ len(word) ] += 1
        byletter[ word[0] ] += 1
        twoletter[word[0]][ word[:2] ] += 1
        if len(set(word)) == 7:
            pangrams.add( word )
            points += 7
            samplepan = word

        points += 1 if len(word) == 4 else len(word)

    counts = sorted(set(sum( (list( x.keys() ) for x in bylettercount.values()), [] ) ) )

    print( "SPELLING BEE GRID\n" )
    print( center + " " + " ".join( sorted( x for x in set(samplepan).difference(center) ) ) )
    out = "\nWORDS: %d, POINTS: %d, PANGRAMS: %d" % ( len(words), points, len(pangrams) )
    perfect = [ x for x in pangrams if len(x) == 7 ]
    if perfect:
        out += " (%s Perfect)" % ( perfect, )
    if len( bylettercount ) == 7:
        out += ", BINGO"

    print( out )

    print( "\nFirst character frequency:\n")
    print( "\n".join( "%s x %d" % (l,f) for l,f in sorted(byletter.items()) ) )

    print( "\nWord length frequency:\n")
    print( "\n".join( "%sL: %d" % (c,f) for c,f in sorted(bycount.items()) ) )

    out = "\nGrid:\n"
    out += "".join( ("\t%3d" % ( c, ) for c in counts) ) + "\tTOT\n"
    for letter in bylettercount:
        out += "%3s:" % ( letter, )
        for cnt in counts:
            out += "\t%3d" % ( bylettercount[letter][cnt], ) if cnt in bylettercount[letter] else "\t  -"
        out += "\t%3d" % ( byletter[letter], )+ "\n"

    out += "TOT: "+ "".join( "%3d\t" % ( c, ) for _,c in sorted(bycount.items()) ) + ("%3d" % (len(words),)) +"\n"

    print( out )

    print( "\nTwo letter list:\n" )
    for _, tlmap in twoletter.items():
        print( " ".join( "%s-%d" % (k, v) for k, v in sorted(tlmap.items()) ) )

def main():
    handler = BeeHandler()
    with urllib.request.urlopen( "https://www.nytimes.com/puzzles/spelling-bee" ) as f:
        f.readline()
        try:
            xml.sax.parse( f, handler )
        except:
            pass

    data = json.loads( handler.answer.split( ' = ', 2 )[1] )
    solve( data['today']['centerLetter'].upper(), [ x.upper() for x in data['today']['answers'] ] )

if __name__ == "__main__":
    main()
