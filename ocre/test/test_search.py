#!/usr/bin/python

import unittest

from ..search import Search


class TestSearch(unittest.TestCase):

    def test_url(self):
        search = Search({'portrait': 'Julia Domna'})
        print(search)
        return self.assertTrue(True)
