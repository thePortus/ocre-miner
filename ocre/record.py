import os
import json
from collections import UserList

from .base import BaseRequest
from .settings import ROOT_URL, JSON_API_URL


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

    def get(self):
        """Gets all records as dicts in parent dict with ids as keywords."""
        completed_data = {}
        counter = 0
        total_records = len(self.data)
        for record in self.data:
            if not self.options['silent']:
                print(
                    'Record {}/{} ({}%)'
                    .format(
                        counter + 1,
                        total_records,
                        round((counter + 1) / total_records, 2)
                    ),
                    end=' '
                )
            completed_data[record.record_id] = record.get()
            counter += 1
        return completed_data

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
            print('Records fetched, saving to file...')
        # child classes much actually implement saving of data
        return filepath


class JSONRecords(BaseRecords):
    """Requests by id and parses record batches, and saves JSON results."""

    def __init__(self, record_ids, options={}):
        self.record_object = JSONRecord
        super().__init__(record_ids, options=options)

    def save(self, filepath, overwrite=False):
        """Gets all data then saves to specified filepath."""
        filepath = super().save(filepath, overwrite)
        save_data = self.get()
        # open and write data to file
        with open(filepath, mode='w+') as writefile:
            writefile.write(json.dumps(save_data))
        if not self.options['silent']:
            print('Success!')
        # return True if successful
        return True
