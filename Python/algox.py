#!/usr/bin/env python3

from functools import reduce

class DoulbleLinkedNode:
    def __init__( self ):
        self.nxt = self
        self.prv = self

    def getVal( self ): return None
    def addAfter( self, ins ):
        nxt = self.nxt
        ins.prv = self
        ins.nxt = nxt
        self.nxt = ins
        nxt.prv = ins
        return ins

    def removeMeAcross( self ):
        nxt = self.nxt
        prv = self.prv
        nxt.prv = prv
        prv.nxt = nxt

    def reinsertMeAcross( self ):
        nxt = self.nxt
        prv = self.prv
        nxt.prv = self
        prv.nxt = self

    def printListAfter( self ):
        curr = self
        out = []
        while True:
            out.append( curr )
            curr = curr.nxt
            if curr in out:
                break
        print( ": ".join( str(n.getVal()) for n in out ) )

class QuadLinkedNode( DoulbleLinkedNode ):
    def __init__( self ):
        super().__init__()
        self.up = self
        self.dwn = self

    def addBelow( self, ins ):
        dwn = self.dwn
        ins.up = self
        ins.dwn = dwn
        self.dwn = ins
        dwn.up = ins
        return ins

    def removeMeDown( self ):
        up = self.up
        dwn = self.dwn
        up.dwn = dwn
        dwn.up = up

    def reinsertMeDown( self ):
        up = self.up
        dwn = self.dwn
        up.dwn = self
        dwn.up = self

    def printListBelow( self ):
        curr = self
        out = []
        while True:
            out.append( curr )
            curr = curr.dwn
            if curr in out:
                break
        print( ": ".join( str(n.getVal()) for n in out ) )

class RealQuad( QuadLinkedNode ):
    def __init__( self, val ):
        super().__init__()
        self.val = val
        
    def getVal( self ): return self.val
    
class ColHead( QuadLinkedNode ):
    def __init__( self, nm ):
        super().__init__()
        self.nm = nm
        self.cnt = 0
        
    def getVal( self ): return self.nm

class Entry( QuadLinkedNode ):
    def __init__( self, colhd, row ):
        super().__init__()
        self.colhd = colhd
        self.row = row
        
    def getVal( self ): return "from %s" % (self.colhd.nm,)

    def removeMeDown( self ):
        super().removeMeDown()
        self.colhd.cnt =- 1

    def reinsertMeDown( self ):
        super().reinsertMeDown()
        self.colhd.cnt += 1

def cover( col ):
    col.removeMeAcross()
    row = col.dwn
    while row != col:
        e = row.nxt
        while e != row:
            e.removeMeDown()
            e = e.nxt
        row = row.dwn
        
def uncover( col ):
    row = col.up
    while row != col:
        e = row.prv
        while e != row:
            e.reinsertMeDown()
            e = e.prv
        row = row.up

    col.reinsertMeAcross()
        
def pickRow( e ):
    entry = e
    while True:
        cover( entry.colhd )
        entry = entry.nxt
        if entry == e:
            break

def rejectRow( e ):
    entry = e.prv
    while True:
        uncover( entry.colhd )
        entry = entry.prv
        if entry == e.prv:
            break

def algox( hdr ):
    if hdr.nxt == hdr:
        return True

    chdr = pick = hdr.nxt
    #while chdr != hdr:
    #    if chdr.cnt < pick.cnt:
    #        pick = chdr
    #    chdr = chdr.nxt
    row = pick.dwn
    while True:
        if row == pick:
            return False
        pickRow( row )
        res = algox( hdr )
        if res == True:
            return [row.row]
        elif res:
            return [row.row]+res
        rejectRow( row )
        row = row.dwn
        
def main():
    grid = [[0,0,1,0,1,1,0],
            [1,0,0,1,0,0,1],
            [0,1,1,0,0,1,0],
            [1,0,0,1,0,0,0],
            [0,1,0,0,0,0,1],
            [0,0,0,1,1,0,1]]

    last = reduce( lambda l, nm: l.addAfter( ColHead(nm) ), "ABCDEFG", ColHead( "head" ) )
    header = last.nxt

    for i,row in enumerate(grid):
        col = header.nxt
        prev = None
        for vl in row:
            if vl:
                e = Entry(col, i)
                col.up.addBelow(e)
                col.cnt += 1
                if prev:
                    prev.addAfter(e)
                prev = e
            col = col.nxt

    print( "AlgoX" )
    res = algox( header )
    from pprint import pprint as pp
    pp( [grid[row] for row in res], width = 30 )

if __name__ == '__main__':
    main()
