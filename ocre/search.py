from .base import BaseRequest
from .settings import ROOT_URL, SEARCH_URL


class Search(BaseRequest):
    """Makes a single search request, parses HTML response, gives results."""

    def __init__(self, search_terms, options={}):
        search_url = ROOT_URL + SEARCH_URL
        first_term = True
        multiples_allowed_arguments = [
            'portrait_facet'
        ]
        change_argument_keywords = {
            'portrait': 'portrait_facet'
        }
        # change some keywords from user friendly to api keywords
        for change_argument_keyword in change_argument_keywords:
            if change_argument_keyword in search_terms:
                search_terms[
                    change_argument_keywords[change_argument_keyword]
                ] = search_terms[change_argument_keyword]
                del search_terms[change_argument_keyword]
        # add individual path segments of search terms with helper function
        for search_term_argument in search_terms:
            multiples_allowed = False
            if search_term_argument in multiples_allowed_arguments:
                multiples_allowed = True
            search_url, first_term = self.add_to_url(
                search_url, search_terms[search_term_argument],
                search_term_argument, multiples_allowed, first_term
            )
        # then call parent class init function with new url
        super().__init__(search_url, options)

    def add_to_url(
        self, current_url, search_term, term_type, multiples_allowed,
        first_term
    ):
        """Internal function to simplify building the url, to avoid
        repeating code when trying to add each term to the url, current_url
        represents the path to date, term is the term being addedself.
        multiples_allowed allows passing a list in addition to a string,
        and first_term indicates whether or not this path is being appended
        to any other search terms, or if it is the first term being added
        to the url."""
        new_url = current_url
        # if no multiples are allowed, search term must be string
        if not multiples_allowed:
            if type(search_term) != str:
                raise Exception(
                    'Search term argument {} must be a string.'
                    .format(term_type)
                )
        # if multiples are allowed, search term must be string or list
        else:
            if type(search_term) != str and type(search_term) != list:
                raise Exception(
                    'Search term argument {} must be a string or list'
                    .format(term_type)
                )
        if not first_term:
            new_url += '+AND+'
        # if a single string is sent, add to url
        if type(search_term) == str:
            new_url += '{}%3A%22{}%22'.format(
                term_type, search_term.replace(' ', '+')
            )
        # if multiple portraits are sent, loop and add each to url
        if type(search_term) == list:
            # add starting parens to search url
            new_url += '%28'
            first_term_item = True
            for search_term_item in search_term:
                if not first_term_item:
                    new_url += '+OR+'
                new_url += '{}%3A%22{}%22'.format(
                    term_type, search_term_item.replace(' ', '+')
                )
                first_term_item = False
            # add end parens to search url
            new_url += '%29'
        first_term = False
        # returning the new url and if first_term has changed
        return (new_url, first_term)
