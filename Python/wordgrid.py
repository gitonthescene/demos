from collections import defaultdict
import json
import requests
import sqlite3
from contextlib import contextmanager
import argparse

from bs4 import BeautifulSoup


def solve(center, words, show):

    bylettercount = defaultdict(lambda: defaultdict(lambda: 0))
    bycount = defaultdict(lambda: 0)
    byletter = defaultdict(lambda: 0)
    twoletter = defaultdict(lambda: defaultdict(lambda: 0))
    pangrams = set()
    samplepan = None
    points = 0

    for word in words:
        bylettercount[word[0]][len(word)] += 1
        bycount[len(word)] += 1
        byletter[word[0]] += 1
        twoletter[word[0]][word[:show]] += 1
        if len(set(word)) == 7:
            pangrams.add(word)
            points += 7
            samplepan = word

        points += 1 if len(word) == 4 else len(word)

    counts = sorted(
        set(sum((list(x.keys()) for x in bylettercount.values()), [])))

    print("SPELLING BEE GRID\n")
    print(center + " " +
          " ".join(sorted(x for x in set(samplepan).difference(center))))
    out = "\nWORDS: %d, POINTS: %d, PANGRAMS: %d" % (len(words), points,
                                                     len(pangrams))
    perfect = [x for x in pangrams if len(x) == 7]
    if perfect:
        out += " (%d Perfect)" % len(perfect)
    if len(bylettercount) == 7:
        out += ", BINGO"

    print(out)

    print("\nFirst character frequency:\n")
    print("\n".join("%s x %d" % (l, f) for l, f in sorted(byletter.items())))

    print("\nWord length frequency:\n")
    print("\n".join("%sL: %d" % (c, f) for c, f in sorted(bycount.items())))

    out = "\nGrid:\n    "
    out += "".join(("\t%3d" % (c,) for c in counts)) + "\t TOT\n"
    for letter in sorted(bylettercount):
        out += "%3s:" % (letter,)
        for cnt in counts:
            out += "\t%3d" % (bylettercount[letter][cnt],
                             ) if cnt in bylettercount[letter] else "\t  -"
        out += "\t%3d" % (byletter[letter],) + "\n"

    out += "TOT:" + "".join(
        "\t%3d" % (c,)
        for _, c in sorted(bycount.items())) + ("\t%3d" % (len(words),)) + "\n"

    print(out)

    print("\nTwo letter list:\n")
    for _, tlmap in sorted(twoletter.items()):
        print(" ".join("%s-%d" % (k, v) for k, v in sorted(tlmap.items())))


def getGameData():
    url = 'https://www.nytimes.com/puzzles/spelling-bee'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')

    element = soup.find('div', class_='pz-game-screen')
    element = element.find('script')
    data = element.text.replace('window.gameData = ', '')
    data = json.loads(data)

    return data['today']


def wordgrid(show):
    data = getGameData()

    # print(data['today']['answers'])
    solve(data['centerLetter'].upper(), [x.upper() for x in data['answers']],
          show)


DBNAME = "spelling-bee.db"


@contextmanager
def BeeCursor():
    db = sqlite3.connect(DBNAME)
    try:
        cursor = db.cursor()
        yield cursor
    finally:
        cursor.close()
        db.commit()
        db.close()


def createLogTables():
    with BeeCursor() as cursor:
        cursor.execute('''
        CREATE TABLE bees (
          centerletter CHAR(1) NOT NULL,
          letters CHAR(7) NOT NULL,
          printdate DATE NOT NULL,
          editor VARCHAR(64) NOT NULL,
        PRIMARY KEY (printdate)
        )
        ''')
        cursor.execute('''
        CREATE TABLE beeanswers (
          printdate DATE NOT NULL,
          word VARCHAR(64) NOT NULL
        )
        ''')


def logGame():
    data = getGameData()
    fields = "centerLetter outerLetters printDate editor answers"
    centerLetter, outerLetters, printDate, editor, answers = (
        data[x] for x in fields.split())
    with BeeCursor() as cursor:
        # add puzzle
        cursor.execute('''
        INSERT INTO bees VALUES(?,?,?,?)
        ''', (centerLetter.lower(),
              (''.join(outerLetters)).lower(), printDate, editor))

        # add answers
        cursor.executemany(
            '''
        INSERT INTO beeanswers VALUES(?,?)
        ''', [(printDate, w) for w in answers])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Tools for working with NYT Spelling Bee game")
    parser.add_argument("--log",
                        dest="log",
                        action="store_true",
                        help="log today's game")
    parser.add_argument("--grid",
                        dest="grid",
                        action="store_false",
                        help="Display today's grid")
    args = parser.parse_args()

    if args.log:
        logGame()
        print("Done")
    elif args.grid:
        wordgrid(2)
