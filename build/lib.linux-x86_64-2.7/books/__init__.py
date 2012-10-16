import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('books')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from books import booksconfig
from books import sqlite

import urllib
import urllib2
import simplejson
import locale

class BooksLens(SingleScopeLens):

	class Meta:
		name = 'books'
		description = 'Books Lens'
		search_hint = 'Search Books'
		icon = '/usr/share/unity/lenses/books/data/books.png'
		search_on_blank=True
		search_in_global = True

	icon_base = '/usr/share/unity/lenses/books/data/'
	bookshelf_category = ListViewCategory("Bookshelf", icon_base + 'group_books.png')
	calibre_library = '/home/jnphilipp/Calibre Library/'

	def __init__(self):
		SingleScopeLens.__init__(self)
		self._lens.props.search_in_global = True

	def search(self, search, results):
		search = '%' + search + '%'

		sq = sqlite.SQLite()
		sq.open(self.calibre_library + 'metadata.db')
		books = sq.execute('select title, has_cover, path, name, format, (SELECT name FROM books_authors_link AS bal JOIN authors ON(author = authors.id) WHERE book = books.id) authors from books, data where books.id=data.book and title like ?', (search,))
		sq.close()

		for book in books:
			url = 'application://calibre.desktop'
			dad_url = self.calibre_library + '/' + book[2] + '/' + book[3] + '.' + book[4]
			if book[1] == 1:
				icon = self.calibre_library + '/' + book[2] + '/cover.jpg'
			else:
				icon = '/usr/share/unity/lenses/books/data/books.png'

			results.append(url, icon, self.bookshelf_category, 'application-x-desktop', book[0], book[5], dad_url)
		pass
