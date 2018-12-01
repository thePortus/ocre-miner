import os
import json
from collections import UserList

from .base import BaseRequest
from .settings import ROOT_URL, JSON_API_URL, NOMISMA_URL


class JSONRecord(BaseRequest):
    """Retreives individual coin record as a JSON."""
    record_id = None

    def __init__(self, record_id, options={}):
        # call parent init function with assembled URL path
        super().__init__(
            ROOT_URL + JSON_API_URL + record_id + '.jsonld',
            options
        )
        self.record_id = record_id

    def get(self):
        """Retreives record data from web and converts to Python dict"""
        return json.loads(self.fetch())


class BaseRecords(UserList):
    """Parent class to all filetype specific batch record classes."""
    record_object = None
    record_ids = []

    def __init__(self, record_ids, options={}):
        super().__init__()
        self.options = options
        # fill self will JSONRecord objects corresponding to ids
        for record_id in record_ids:
            self.data.append(self.record_object(record_id, options))

    @classmethod
    def convert(self, parent_data, keyword=None):
        """Helper function to get data from inside data returned by .get().
        If parent data is a string, simply removes the url prefix before
        pertinent information, if a list of dicts, will build a list of
        data inside each dict found at a given keyword."""
        retreived_values = []
        new_value = None
        # build url to trim from the 'id' entry of coins
        url_trim = ROOT_URL + JSON_API_URL
        if type(parent_data) == str:
            new_value = parent_data.replace(url_trim, '')
            return new_value
        if type(parent_data) != list:
            raise Exception('Convert data must contain list or string.')
        # otherwise if a list of strings, start looping and getting values
        for internal_dict in parent_data:
            # if a string, simply trim nomisma's url prefix
            if type(internal_dict) == str:
                new_value = internal_dict.replace(NOMISMA_URL, '')
                retreived_values.append(new_value)
            elif keyword in internal_dict:
                new_value = internal_dict[keyword]
                # for urls, remove the nomisma site url prefix
                if type(new_value) == str:
                    new_value = new_value.replace(NOMISMA_URL, '')
                retreived_values.append(new_value)
        # if only one value found, don't return as list, return value itself
        if len(retreived_values) == 1:
            return retreived_values[0]
        return retreived_values

    def get(self):
        """Gets all records as dicts in parent dict with ids as keywords."""
        raw_data = {}
        converted_data = {}
        new_data = None
        counter = 0
        total_records = len(self.data)
        for record in self.data:
            if not self.options['silent']:
                print(
                    ' Record {}/{} ({}%): '
                    .format(
                        counter + 1,
                        total_records,
                        round(((counter + 1) / total_records) * 100, 2)
                    ),
                    end=''
                )
            raw_data[record.record_id] = record.get()
            counter += 1
            # go to dictionary inside json-ld containing the actual save_data
            new_data = raw_data[record.record_id]['@graph']
            # convert from JSON-ld to plain JSON to make easier to use
            converted_data[record.record_id] = {}
            try:
                converted_data[record.record_id][
                    'id'
                ] = self.convert(
                    new_data[0]['@id']
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'label'
                ] = self.convert(
                    new_data[0]['skos:prefLabel']
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'source'
                ] = self.convert(
                    new_data[0]['dcterms:source'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'manufacture'
                ] = self.convert(
                    new_data[0]['nmo:hasManufacture'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'denomination'
                ] = self.convert(
                    new_data[0]['nmo:hasDenomination'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'material'
                ] = self.convert(
                    new_data[0]['nmo:hasMaterial'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'authority'
                ] = self.convert(
                    new_data[0]['nmo:hasAuthority'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'mint'
                ] = self.convert(
                    new_data[0]['nmo:hasMint'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'region'
                ] = self.convert(
                    new_data[0]['nmo:hasRegion'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'start_date'
                ] = int(self.convert(
                    new_data[0]['nmo:hasStartDate'], '@value'
                ))
            except:
                pass
            try:
                converted_data[record.record_id][
                    'end_date'
                ] = int(self.convert(
                    new_data[0]['nmo:hasEndDate'], '@value'
                ))
            except:
                pass
            try:
                converted_data[record.record_id][
                    'obverse_legend'
                ] = self.convert(
                    new_data[1]['nmo:hasLegend'], '@value'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'obverse_description'
                ] = self.convert(
                    new_data[1]['dcterms:description'], '@value'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'obverse_portraits'
                ] = self.convert(
                    new_data[1]['nmo:hasPortrait'], '@id'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'reverse_legend'
                ] = self.convert(
                    new_data[1]['nmo:hasLegend'], '@value'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'reverse_description'
                ] = self.convert(
                    new_data[1]['dcterms:description'], '@value'
                )
            except:
                pass
            try:
                converted_data[record.record_id][
                    'reverse_portraits'
                ] = self.convert(
                    new_data[1]['nmo:hasPortrait'], '@id'
                )
            except:
                pass
        return converted_data

    def save(self, filepath, overwrite=False):
        """Performs common saving pre-operations for child classes."""
        # ensure filepath is absolute, if relative, make it absolute
        if not os.path.isabs(filepath):
            filepath = os.path.abspath(filepath)
        # if file exists at path and overwrite not flagged, abort
        if os.path.exists(filepath) and overwrite is False:
            raise Exception(
                'Error while saving, file already exists at {}'
                .format(filepath)
            )
        if not self.options['silent']:
            print('Records fetched, saving to file...', end='\r')
        # child classes much actually implement saving of data
        return filepath


class JSONRecords(BaseRecords):
    """Requests by id and parses record batches, and saves JSON results."""

    def __init__(self, record_ids, options={}):
        self.record_object = JSONRecord
        super().__init__(record_ids, options=options)

    def get(self):
        """Gets all records in large dict form, converts to list for saving"""
        master_data_records = super().get()
        coverted_records = []
        for master_data_record_id in master_data_records:
            coverted_records.append(master_data_records[master_data_record_id])
        return coverted_records

    def save(self, filepath, overwrite=False):
        """Gets all data then saves to specified filepath."""
        filepath = super().save(filepath, overwrite)
        save_data = self.get()
        # open and write data to file
        with open(filepath, mode='w+') as writefile:
            writefile.write(json.dumps(save_data))
        if not self.options['silent']:
            print('Success!', end='\r')
        # return True if successful
        return True
