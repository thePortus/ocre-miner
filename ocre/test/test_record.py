#!/usr/bin/python

import unittest

from ..record import JSONRecords


class TestJSONRecords(unittest.TestCase):

    def test_convert_list(self):
        test_data = [
            {
                "@id": "http://nomisma.org/id/julia_domna"
            },
            {
                "@id": "http://nomisma.org/id/caracalla"
            },
            {
                "@id": "http://nomisma.org/id/geta"
            }
          ]
        test_results = JSONRecords.convert(test_data, '@id')
        return self.assertTrue(
            len(test_results) > 1 and type(test_results) == list
        )

    def test_convert_british_museum(self):
        test_data = [
            {
                "@id": "http://nomisma.org/id/julia_domna"
            },
            {
                "@id": (
                    "http://collection.britishmuseum.org/id/"
                    "person-institution/57930"
                )
            }
          ]
        test_results = JSONRecords.convert(test_data, '@id')
        return self.assertTrue(
            test_results[1] == 'Ceres'
        )

    def test_get(self):
        # records = JSONRecords(['ric.4.ss.159'], options={'silent': True})
        pass
