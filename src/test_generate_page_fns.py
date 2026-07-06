import unittest
from generate_page_fns import extract_title

class TestExtractingTitles(unittest.TestCase):
    def test_basictest(self):
        markdown = "\n # Starting with heading one\nOoga Booga"
        res = extract_title(markdown)
        exp = "Starting with heading one"
        self.assertEqual(res,exp)

    def test_poundtest(self):
        markdown = " # #Starting with a pound sign \n tee \n hee hee"
        res = extract_title(markdown)
        exp = "#Starting with a pound sign"
        self.assertEqual(res, exp)