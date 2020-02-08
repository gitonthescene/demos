#!/usr/bin/env python

def genDisc( sz, max ):
    halfdisc = "*"* sz
    fill = " "*(max-sz)
    return fill+halfdisc+halfdisc+fill

def genStacks( pegs, max ):
    res = ""
    level = max
    while level > 0:
        level = level - 1
        for i in [0,1,2]:
            if len( pegs[i] ) > level:
                res += genDisc( pegs[i][level], max )
            else:
                res += genDisc( 0, max )
        res += "\n"
    return res

def solve( pegs, sz, currentpeg, offset, max ):
    # Clear stuff off top
    if sz > 1:
        solve( pegs, sz - 1, currentpeg, -offset, max )

    # Move the target disc
    disc = pegs[currentpeg].pop()
    pegs[ (currentpeg+offset)%3 ].append( disc )

    print( genStacks( pegs, max ) )

    # Restore cleared stuff
    if sz > 1:
        solve( pegs, sz - 1, (currentpeg-offset)%3, -offset, max )
    
def main():
    MAX = 5
    pegs = [[5,4,3,2,1],[],[]]
    solve( pegs, MAX, 0, 1, MAX )
    
if __name__ == '__main__':
    main()
