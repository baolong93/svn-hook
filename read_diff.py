import os
#with open(os.path.dirname(os.path.abspath(__file__)) + "/difftest.txt", "r") as f:
#    print f.read()

import unittest
# Here's our "unit".


def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".

class DiffElement:
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

class DiffContentLine():
    def __init__(self, strline):
        self.strline = strline[1:] + "\n"

    def containsTab(self):
        return "\t" in self.strline

    def endWithSemicolon(self):
        import re
        return re.search(r';\s*\n', self.strline) != None

    def addLine(self, line):
        self.strline +=  line[1:] + "\n"

    def wrongElseFormat(self):
        import re
        return re.search(r'}\s*else{', self.strline) != None or \
                re.search(r'}else\s*{', self.strline) != None or \
                re.search(r'}\s{2,}else\s{', self.strline) != None or \
                re.search(r'}\selse\s{2,}{', self.strline) != None or \
                re.search(r'}\s*\n*\s*else\s*\n*\s*{', self.strline) != None

    def wrongIfFormat(self):
        import re
        return re.search(r'\nif\(', self.strline) != None or \
                re.search(r'\s*if\(', self.strline) != None or \
                re.search(r'\s*if\s{2,}\(', self.strline) != None or \
                re.search(r'}\s*if\s\(', self.strline) != None 

def isHeader(line):
    return line.split(" ")[0] in ["Added:", "Modified:", "Deleted:"]

class TestFoo(unittest.TestCase):

    def testDiffInfo(self):
        diffheader = DiffElement("Added: trunk/vendors/deli/soda.txt")
        self.assertEquals(diffheader.getDiffType(), "Added")
        self.assertEquals(diffheader.getDiffFile(), "trunk/vendors/deli/soda.txt")
        self.assertEquals(diffheader.getDiffFileExt(), "txt")

        diffheader = DiffElement("Modified: trunk/vendors/deli/sandwich.groovy")
        self.assertEquals(diffheader.getDiffType(), "Modified")
        self.assertEquals(diffheader.getDiffFile(), "trunk/vendors/deli/sandwich.groovy")
        self.assertEquals(diffheader.getDiffFileExt(), "groovy")

        diffheader = DiffElement("Copied: egg.txt (from rev 39, trunk/vendors/deli/pickle.txt)")
        self.assertEquals(diffheader.getDiffType(), "Copied")
        self.assertEquals(diffheader.getDiffFile(), "egg.txt")
        self.assertEquals(diffheader.getDiffFileExt(), "txt")

    def testDiffLineContent(self):
        diffline = DiffContentLine("contains tab: 	")
        self.assertTrue(diffline.containsTab())

        diffline = DiffContentLine("not ;contains tab:")
        self.assertFalse(diffline.containsTab())

    def testDiffLineEndWithSemicolon(self):
        diffline = DiffContentLine("contains semicolon: ;")
        self.assertTrue(diffline.endWithSemicolon())

        diffline = DiffContentLine("semicolon in the ;middle of line")
        self.assertFalse(diffline.endWithSemicolon())

        diffline = DiffContentLine("semicolon follow by spaces;  \n")
        self.assertTrue(diffline.endWithSemicolon())

    def testIsHeader(self):
        self.assertTrue(isHeader("Added: trunk/vendors/deli/soda.txt"))
        self.assertFalse(isHeader("  Added: trunk/vendors/deli/soda.txt test"))

    def testAddLine(self):
        diffline = DiffContentLine("+Firstline")
        diffline.addLine("+Second line")
        self.assertEquals(diffline.strline, "Firstline\nSecond line\n")

    def testDiffContentContainSemicolonAtTheEnd(self):
        diffline = DiffContentLine("+Firstline;")
        diffline.addLine("+Second line")
        self.assertTrue(diffline.endWithSemicolon())

    def testDiffContainsWrongElseFormat(self):
        diffline = DiffContentLine("+}else{")
        self.assertTrue(diffline.wrongElseFormat())
        diffline = DiffContentLine("+} else{")
        self.assertTrue(diffline.wrongElseFormat())
        diffline = DiffContentLine("+}else {")
        self.assertTrue(diffline.wrongElseFormat())
        diffline = DiffContentLine("+}  else {")
        self.assertTrue(diffline.wrongElseFormat())
        diffline = DiffContentLine("+} else     {")
        self.assertTrue(diffline.wrongElseFormat())
        diffline = DiffContentLine("+}\nelse\n{")
        self.assertTrue(diffline.wrongElseFormat())
        diffline = DiffContentLine("+} \n else \n {")
        self.assertTrue(diffline.wrongElseFormat())

    def testDiffContainsWrongIfFormat(self):
        diffline = DiffContentLine("+\nif(")
        self.assertTrue(diffline.wrongIfFormat())
        diffline = DiffContentLine("+ if(")
        self.assertTrue(diffline.wrongIfFormat())
        diffline = DiffContentLine("+\n  if(")
        self.assertTrue(diffline.wrongIfFormat())
        diffline = DiffContentLine("+if  (")
        self.assertTrue(diffline.wrongIfFormat())
        diffline = DiffContentLine("+} if (")
        self.assertTrue(diffline.wrongIfFormat())


def main():
    unittest.main()

if __name__ == '__main__':
    main()
