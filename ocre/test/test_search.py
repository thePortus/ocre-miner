#!/usr/bin/python

import unittest

from ..search import Search


class TestSearch(unittest.TestCase):

    def test_url(self):
        search = Search({'portrait': 'Julia Domna'})
        finished_url = 'http://numismatics.org/ocre/results?q=portrait_facet%3A%22Julia+Domna%22'
        return self.assertTrue(search == finished_url)
