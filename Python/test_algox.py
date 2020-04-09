#!/usr/bin/env python3

from algox import DoubleLinkedNode, QuadLinkedNode, ColHead, Entry


def cycleOfTwo(n1, n2, links):
    (nxt, prv) = links
    assert nxt(n1) == n2
    assert nxt(n2) == n1
    assert prv(n1) == n2
    assert prv(n2) == n1


def getAPI(clz, members):
    return tuple(getattr(clz, m) for m in members)


# Show symmetry by running (essentially) the same tests
def linkedNodeTest(nm):
    '''
    Test basic linkage of double linked lists after insertion, removal, etc.
    '''

    def fn(clz, members, linknms):
        (nxtnm, prvnm) = linknms
        nxt = lambda n: getattr(n, nxtnm)
        prv = lambda n: getattr(n, prvnm)

        n1 = clz()
        addAfter, removeMe, reinsertMe, iterOver = getAPI(clz, members)

        assert nxt(n1) == n1
        assert prv(n1) == n1

        n2 = clz()
        addAfter(n1, n2)

        # Should be a cycle both forwards and backwards
        cycleOfTwo(n1, n2, (nxt, prv))

        removeMe(n1)
        # n2 no longer points to n1
        assert nxt(n2) == n2
        assert prv(n2) == n2
        # n1 still points to n2
        assert nxt(n1) == n2
        assert prv(n1) == n2

        reinsertMe(n1)
        # back to previous state
        cycleOfTwo(n1, n2, (nxt, prv))

        lst = []

        def collect(x):
            lst.append(x)

        iterOver(n1, collect)
        assert lst == [n1, n2]

    fn.description = nm
    return fn


TESTS = [
    ('double linked list',
     (DoubleLinkedNode, "addAfter removeMe reinsertMe iterOver".split(),
      'nxt prv'.split())),
    ('quad linked list left-right',
     (QuadLinkedNode,
      "addAfter removeMeAcross reinsertMeAcross iterAcross".split(),
      'nxt prv'.split())),
    ('quad linked list up-down',
     (QuadLinkedNode, "addBelow removeMeDown reinsertMeDown iterDown".split(),
      'dwn up'.split()))
]


def test_generator():
    for nm, tstargs in TESTS:
        yield (linkedNodeTest('test ' + nm),) + tstargs


def test_colhd():
    c1 = ColHead("c1")
    assert c1.cnt == 0

    dwn = lambda n: getattr(n, 'dwn')
    up = lambda n: getattr(n, 'up')
    nxt = lambda n: getattr(n, 'nxt')
    prv = lambda n: getattr(n, 'prv')

    e1 = Entry(c1, "E1")
    c1.addBelow(e1)

    cycleOfTwo(c1, e1, (dwn, up))
    assert c1.cnt == 1

    e1.removeMeDown()
    assert c1.cnt == 0

    e1.reinsertMeDown()
    assert c1.cnt == 1

    e2 = Entry(c1, "E2")
    e1.addBelow(e2)
    assert c1.cnt == 2

    e2.removeMeDown()
    assert c1.cnt == 1

    c2 = ColHead("c2")
    c1.addAfter(c2)

    cycleOfTwo(c1, c2, (nxt, prv))
    assert c1.cnt == 1
    assert c2.cnt == 0
