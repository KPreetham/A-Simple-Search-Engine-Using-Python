import unittest
import Crawler # Assuming Crawler.py is in the same directory or accessible in PYTHONPATH
from bs4 import BeautifulSoup # Needed for creating test doc for get_anchor_tag

class TestCrawler(unittest.TestCase):
    def test_get_anchor_tag(self):
        # Test with a sample HTML document string containing anchor tags
        html_doc_with_anchors = "<html><body><a href='http://example.com/page1'>Page 1</a><a href='/page2'>Page 2</a></body></html>"
        expected_links = ['http://example.com/page1', '/page2']
        self.assertEqual(Crawler.get_anchor_tag(html_doc_with_anchors), expected_links)

        # Test with an HTML document that has no anchor tags
        html_doc_no_anchors = "<html><body><p>No links here.</p></body></html>"
        self.assertEqual(Crawler.get_anchor_tag(html_doc_no_anchors), [])

        # Test with an HTML document where anchor tags have no href attributes
        html_doc_no_href = "<html><body><a>No href</a><a href=''>Empty href</a></body></html>"
        # Updated get_anchor_tag skips tags with no href attribute, and includes empty hrefs.
        self.assertEqual(Crawler.get_anchor_tag(html_doc_no_href), [''])

    def test_get_proper_link(self):
        # Make sure Crawler.domain is set for each relevant test case,
        # or ensure it's reset if tests might interfere.
        # For this function, it's a global, so setting it once should be fine
        # if test order isn't guaranteed and other tests might change it.
        # However, unittest creates a new instance of the class for each test method.
        Crawler.domain = 'http://example.com' # Set domain for testing

        # Test case 1: anchor_link starts with "http"
        self.assertEqual(Crawler.get_proper_link('http://example.com/current.html', 'http://another.com/page.html'), 'http://another.com/page.html')

        # Test case 2: anchor_link starts with "/"
        self.assertEqual(Crawler.get_proper_link('http://example.com/current.html', '/about.html'), 'http://example.com/about.html')

        # Test case 3: cur_link ends with ".html" and anchor_link is relative
        self.assertEqual(Crawler.get_proper_link('http://example.com/path/to/current.html', 'other.html'), 'http://example.com/path/to/other.html')

        # Test case 4: cur_link does not end with ".html" (implicitly a directory) and anchor_link is relative
        self.assertEqual(Crawler.get_proper_link('http://example.com/path/to/', 'another_page.html'), 'http://example.com/path/to/another_page.html')

if __name__ == '__main__':
    unittest.main()
