#!/usr/bin/env python3

from functools import reduce
from pprint import pprint as pp

class DoulbleLinkedNode:
    def __init__( self, me=None ):
        self.me = self if me is None else me
        self.nxt = self
        self.prv = self

    def addAfter( self, ins ):
        nxt = self.nxt
        ins.prv = self
        ins.nxt = nxt
        self.nxt = ins
        nxt.prv = ins
        return ins.me

    def removeMe( self ):
        nxt = self.nxt
        prv = self.prv
        nxt.prv = prv
        prv.nxt = nxt

    def reinsertMe( self ):
        nxt = self.nxt
        prv = self.prv
        nxt.prv = self
        prv.nxt = self

    def iterOver( self, cb ):
        curr = self
        out = []
        while True:
            out.append( curr )
            cb( curr.me )
            curr = curr.nxt
            if curr in out:
                break

class QuadLinkedNode:
    def __init__( self ):
        self.leftright = DoulbleLinkedNode(self)
        self.updown = DoulbleLinkedNode(self)

    def addAfter( self, ins ):
        return self.leftright.addAfter(ins.leftright)

    def addBelow( self, ins ):
        return self.updown.addAfter(ins.updown)

    def removeMeAcross( self ):
        self.leftright.removeMe()

    def removeMeDown( self ):
        self.updown.removeMe()

    def reinsertMeAcross( self ):
        self.leftright.reinsertMe()

    def reinsertMeDown( self ):
        self.updown.reinsertMe()

    def iterAcross( self, cb ):
        self.leftright.iterOver( cb )

    def iterDown( self, cb ):
        self.updown.iterOver( cb )

    @property
    def nxt( self ):
        return self.leftright.nxt.me

    @property
    def prv( self ):
        return self.leftright.prv.me

    @property
    def dwn( self ):
        return self.updown.nxt.me

    @property
    def up( self ):
        return self.updown.prv.me

class ColHead( QuadLinkedNode ):
    def __init__( self, nm ):
        super().__init__()
        self.nm = nm
        self.cnt = 0

    def addBelow( self, ins ):
        super().addBelow( ins )
        self.cnt += 1

    def removeMeDown( self ):
        super().removeMeDown()
        self.cnt -= 1

    def reinsertMeDown( self ):
        super().reinsertMeDown()
        self.cnt += 1


class Entry( QuadLinkedNode ):
    def __init__( self, colhd, row ):
        super().__init__()
        self.colhd = colhd
        self.row = row

    def addBelow( self, ins ):
        self.colhd.cnt += 1
        super().addBelow( ins )

    def removeMeDown( self ):
        super().removeMeDown()
        self.colhd.cnt -= 1

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
    out = []
    hdr.nxt.iterAcross( lambda nd: out.append( nd.cnt ) )

    if hdr.nxt == hdr:
        return True

    chdr = pick = hdr.nxt
    while chdr != hdr:
        if chdr.cnt < pick.cnt:
            pick = chdr
        chdr = chdr.nxt
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
                if prev:
                    prev.addAfter(e)
                prev = e
            col = col.nxt

    print( "AlgoX" )
    res = algox( header )
    pp( [grid[row] for row in res], width = 30 )

if __name__ == '__main__':
    main()
