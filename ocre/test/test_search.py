#!/usr/bin/python

import unittest

from ..search import Search


class TestSearch(unittest.TestCase):

    def test_portrait_single_url(self):
        search = Search({'portrait': 'Julia Domna'})
        finished_url = (
            'http://numismatics.org/ocre/results?q='
            'portrait_facet%3A%22Julia+Domna%22'
        )
        return self.assertTrue(search == finished_url)

    def test_portrait_list_url(self):
        search = Search({'portrait': ['Caracalla', 'Julia Domna']})
        finished_url = (
            'http://numismatics.org/ocre/results?q='
            '%28portrait_facet%3A%22Caracalla%22+OR+portrait_facet'
            '%3A%22Julia+Domna%22%29'
        )
        return self.assertTrue(search == finished_url)

    def test_portrait_soup(self):
        search = Search({'portrait': 'Julia Domna'})
        search_page_html = search.soup().get_text()
        return self.assertTrue(
            search_page_html.startswith('\nOnline Coins of the Roman Empire'))
