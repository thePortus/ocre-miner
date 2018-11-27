from .base import BaseRequest
from .settings import ROOT_URL, SEARCH_URL


class Search(BaseRequest):
    """Makes a single search request, parses HTML response, gives results."""

    def __init__(self, search_terms, options={}):
        search_url = ROOT_URL + SEARCH_URL
        first_term = True
        # ensure search terms are all valid (e.g. authority is a string)
        if search_terms['authority']:
            if type(search_terms['authority']) != str:
                raise Exception(
                    'Authority search term must be a single string.'
                )
        if search_terms['portrait']:
            if type(
                search_terms['portrait']
            ) != str and type(
                search_terms['portrait']
            ) != list:
                raise Exception(
                    'Portrait search term must either be a string or list.'
                )
        # add search terms onto URL here
        if search_terms['authority']:
            # add query conjunction if this is not the first search term
            if not first_term:
                search_url += '+AND+'
            # add term to url, replacing spaces with +'s
            search_url += 'authority_facet%3A"{}"'.format(
                search_terms['authority'].replace(' ', '+')
            )
            first_term = False
        if search_terms['portrait']:
            if not first_term:
                search_url += '+AND+'
            # if a single string is sent, add to url
            if type(search_terms['portrait']) == str:
                search_url += 'portrait_facet%3A"{}"'.format(
                    search_terms['portrait'].replace(' ', '+')
                )
            # if multiple portraits are sent, loop and add each to url
            if type(search_terms['portrait']) == list:
                # add starting parens to search url
                search_url += '%28'
                first_portrait = True
                for portrait_term in search_terms['portrait']:
                    if not first_portrait:
                        search_url += '+OR+'
                        search_url += 'portrait_facet%3A"{}"'.format(
                            portrait_term.replace(' ', '+')
                        )
                    first_portrait = False
                # add end parens to search url
                search_url += '%29'
            first_term = False
        # then call parent class init function with new url
        super().__init__(search_url, options)
