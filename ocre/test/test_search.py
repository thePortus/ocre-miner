#!/usr/bin/python

import unittest

from ..search import Search, ResultsPage


class TestResultsPage(unittest.TestCase):

    def test_results_ids(self):
        results_url = (
            'http://numismatics.org/ocre/results?q='
            'portrait_facet:%22Julia%20Domna%22&lang=en'
        )
        results_page = ResultsPage(results_url, options={'silent': True})
        first_record_url = results_page.record_ids[0]
        return self.assertTrue(
            first_record_url.startswith('ric.4.ss.159')
        )

    def test_next_button_exists(self):
        results_url = (
            'http://numismatics.org/ocre/results?q='
            'portrait_facet:%22Julia%20Domna%22&lang=en'
        )
        results_page = ResultsPage(results_url, options={'silent': True})
        next_page_url = results_page.next_page_link
        test_url = (
            'http://numismatics.org/ocre/results?q='
            'portrait_facet%3A%22Julia%20Domna%22&start=20&lang=en'
        )
        return self.assertTrue(next_page_url == test_url)

    def test_next_button_disabled(self):
        results_url = (
            'http://numismatics.org/ocre/results?q='
            'portrait_facet%3A%22Julia%20Domna%22&start=360&lang=en'
        )
        results_page = ResultsPage(results_url, options={'silent': True})
        next_page_url = results_page.next_page_link
        return self.assertFalse(next_page_url)


class TestSearch(unittest.TestCase):

    def test_portrait_single_url(self):
        search = Search({'portrait': 'Julia Domna'}, options={'silent': True})
        finished_url = (
            'http://numismatics.org/ocre/results?q='
            'portrait_facet%3A%22Julia+Domna%22'
        )
        return self.assertTrue(search == finished_url)

    def test_portrait_list_url(self):
        search = Search(
            {'portrait': ['Caracalla', 'Julia Domna']},
            options={'silent': True}
        )
        finished_url = (
            'http://numismatics.org/ocre/results?q='
            '%28portrait_facet%3A%22Caracalla%22+OR+portrait_facet'
            '%3A%22Julia+Domna%22%29'
        )
        return self.assertTrue(search == finished_url)

    def test_portrait_soup(self):
        search = Search({'portrait': 'Julia Domna'}, options={'silent': True})
        search_page_html = search.soup().get_text()
        return self.assertTrue(
            search_page_html.startswith('\nOnline Coins of the Roman Empire'))

    def test_get_record_ids(self):
        search = Search(
            {'portrait': 'Grata Honoria'}, options={'silent': True}
        )
        search_record_ids = search.get_record_ids()
        return self.assertTrue(
            search_record_ids[0] == 'ric.10.valt_iii_w.2021'
        )
