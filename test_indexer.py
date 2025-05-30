import unittest
from collections import Counter
import Indexer # Assuming Indexer.py is in the same directory or accessible in PYTHONPATH

class TestIndexer(unittest.TestCase):

    def test_parse_document(self):
        # Test with a sample document string
        doc_text = "Hello world! This is a test. Hello again."
        expected_counts = Counter({'hello': 2, 'world': 1, 'this': 1, 'is': 1, 'a': 1, 'test': 1, 'again':1 }) # Assuming lowercase and punctuation removal
        self.assertEqual(Indexer.parse_document(doc_text), expected_counts)

        # Test with an empty document string
        self.assertEqual(Indexer.parse_document(""), Counter())

        # Test with a document string that contains only punctuation
        self.assertEqual(Indexer.parse_document("!@#$%^&*().,"), Counter())
        self.assertEqual(Indexer.parse_document("--- === +++"), Counter())


    def test_create_small_table(self):
        word_counter = Counter({'hello': 2, 'world': 1})
        url = "http://example.com/doc1"
        expected_table = {
            'hello': [url, 2],
            'world': [url, 1]
        }
        self.assertEqual(Indexer.create_small_table(word_counter, url), expected_table)

        # Test with empty counter
        word_counter_empty = Counter()
        url_empty = "http://example.com/doc_empty"
        expected_table_empty = {}
        self.assertEqual(Indexer.create_small_table(word_counter_empty, url_empty), expected_table_empty)


    def test_add_to_big_table(self):
        # Test case 1: Add a new small_table to an empty big_table
        Indexer.big_table = {} # Initialize/reset big_table
        small_table1 = {'word1': ['url1', 2]}
        Indexer.add_to_big_table(small_table1)
        expected_big_table1 = {'word1': [['url1', 2]]}
        self.assertEqual(Indexer.big_table, expected_big_table1)

        # Test case 2: Add another small_table with overlapping and new words
        Indexer.big_table = {'word1': [['url1', 2]]} # Pre-fill big_table
        small_table2 = {'word1': ['url2', 3], 'word2': ['url1', 1]}
        Indexer.add_to_big_table(small_table2)
        expected_big_table2 = {
            'word1': [['url1', 2], ['url2', 3]],
            'word2': [['url1', 1]]
        }
        # The order of entries within big_table['word1'] list might vary if not handled.
        # The test should be robust to this, e.g. by comparing sets of tuples or sorting.
        # For now, assume append maintains order for simplicity of this initial test structure.
        # A more robust check for list of lists where inner list order matters but outer doesn't:
        self.assertEqual(Indexer.big_table['word2'], expected_big_table2['word2'])
        self.assertIn(['url1', 2], Indexer.big_table['word1'])
        self.assertIn(['url2', 3], Indexer.big_table['word1'])
        self.assertEqual(len(Indexer.big_table['word1']), 2)


if __name__ == '__main__':
    unittest.main()
