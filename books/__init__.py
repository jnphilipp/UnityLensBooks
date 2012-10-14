import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('books')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from books import booksconfig

class BooksLens(SingleScopeLens):

    class Meta:
        name = 'books'
        description = 'Books Lens'
        search_hint = 'Search Books'
        icon = 'books.svg'
        search_on_blank=True

    # TODO: Add your categories
    example_category = ListViewCategory("Examples", 'help')

    def search(self, search, results):
        # TODO: Add your search results
        results.append('https://wiki.ubuntu.com/Unity/Lenses/Singlet',
                         'ubuntu-logo',
                         self.example_category,
                         "text/html",
                         'Learn More',
                         'Find out how to write your Unity Lens',
                         'https://wiki.ubuntu.com/Unity/Lenses/Singlet')
        pass
