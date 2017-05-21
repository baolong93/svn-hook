import os
#with open(os.path.dirname(os.path.abspath(__file__)) + "/difftest.txt", "r") as f:
#    print f.read()

import unittest
# Here's our "unit".


def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".

class SvnDiffHeader:
    """ The diff header look like this
    Added: trunk/vendors/deli/soda.txt """

    def __init__(self, strheader):
        self.strheader = strheader

    def getDiffType(self):
        return self.strheader.split(":")[0]

    def getDiffFile(self):
        return self.strheader.split(" ")[1]

    def getDiffFileExt(self):
        return self.getDiffFile().split(".")[1]

class SvnDiffLine():
    def __init__(self, strline):
       self.strline = strline

    def containsTab(self):
        return "\t" in self.strline

    def endWithSemicolon(self):
        return ";" == self.strline.strip()[-1]

class TestFoo(unittest.TestCase):

    def testDiffInfo(self):
        diffheader = SvnDiffHeader("Added: trunk/vendors/deli/soda.txt")
        self.assertEquals(diffheader.getDiffType(), "Added")
        self.assertEquals(diffheader.getDiffFile(), "trunk/vendors/deli/soda.txt")
        self.assertEquals(diffheader.getDiffFileExt(), "txt")

        diffheader = SvnDiffHeader("Modified: trunk/vendors/deli/sandwich.groovy")
        self.assertEquals(diffheader.getDiffType(), "Modified")
        self.assertEquals(diffheader.getDiffFile(), "trunk/vendors/deli/sandwich.groovy")
        self.assertEquals(diffheader.getDiffFileExt(), "groovy")

        diffheader = SvnDiffHeader("Copied: egg.txt (from rev 39, trunk/vendors/deli/pickle.txt)")
        self.assertEquals(diffheader.getDiffType(), "Copied")
        self.assertEquals(diffheader.getDiffFile(), "egg.txt")
        self.assertEquals(diffheader.getDiffFileExt(), "txt")

    def testDiffLineContent(self):
        diffline = SvnDiffLine("contains tab: 	")
        self.assertTrue(diffline.containsTab())

        diffline = SvnDiffLine("not ;contains tab:")
        self.assertFalse(diffline.containsTab())

    def testDiffLineEndWithSemicolon(self):
        diffline = SvnDiffLine("contains semicolon: ;")
        self.assertTrue(diffline.endWithSemicolon())

        diffline = SvnDiffLine("semicolon in the ;middle of line")
        self.assertFalse(diffline.endWithSemicolon())

        diffline = SvnDiffLine("semicolon follow by spaces;  \n")
        self.assertTrue(diffline.endWithSemicolon())


def main():
    unittest.main()

if __name__ == '__main__':
    main()
