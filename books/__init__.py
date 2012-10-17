import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('unity-lens-books')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from books import booksconfig
from books import sqlite

import os
import glib
import urllib
import urllib2
import simplejson
import locale
import fnmatch
from configobj import ConfigObj

class BooksLens(SingleScopeLens):

	class Meta:
		name = 'books'
		description = 'Books Lens'
		search_hint = 'Search Books'
		icon = '/usr/share/unity/lenses/books/data/books.png'
		search_on_blank=True
		search_in_global = True

	icon_base = '/usr/share/unity/lenses/books/data/'
	bookshelf_category = IconViewCategory("Bookshelf", icon_base + 'group_books.png')
	calibre_library = ''

	def __init__(self):
		SingleScopeLens.__init__(self)
		self._lens.props.search_in_global = True

		if os.path.exists(os.path.join(glib.get_user_config_dir() + '/calibre/global.py')):
			prop = ConfigObj(os.path.join(glib.get_user_config_dir() + '/calibre/global.py'))
			self.calibre_library = prop['library_path'][2:len(prop['library_path'])-1]

	def search(self, search, results):
		url = 'application://calibre.desktop'
		for book in self.search_calibre('%' + search + '%'):
			dad_url = self.calibre_library + '/' + book[2] + '/' + book[3] + '.' + book[4].lower()
			if book[1] == 1:
				icon = self.calibre_library + '/' + book[2] + '/cover.jpg'
			else:
				icon = 'calibre'

			if book[4] == 'PDF':
				results.append('file://' + dad_url, icon, self.bookshelf_category, 'application/pdf', book[0], book[5], dad_url)
			else:
				results.append(url, icon, self.bookshelf_category, 'application-x-desktop', book[0], book[5], dad_url)

		if len(search) > 1:
			for book in self.find_files(glib.get_user_special_dir(glib.USER_DIRECTORY_DOCUMENTS), ['*' + search + '*.pdf']):
				dad_url = book[0]
				url = 'file://' + dad_url
				icon = 'application-pdf'#'/usr/share/unity/lenses/books/data/books.png'
				results.append(url, icon, self.bookshelf_category, 'application/pdf ', book[1], book[1], dad_url)

		pass

	def search_calibre(self, search):
		if self.calibre_library == '':
			return []

		sq = sqlite.SQLite()
		sq.open(os.path.join(self.calibre_library, 'metadata.db'))
		books = sq.execute('select title, has_cover, path, data.name, format, authors.name from books join data on books.id=data.book join books_authors_link on books.id=books_authors_link.book join authors on books_authors_link.author=authors.id where title like ? or authors.name like ?', (search, search))
		sq.close()

		return books

	def find_files(self, directory, patterns):
		for root, dirs, files in os.walk(directory):
			for basename in files:
				matched = any(fnmatch.fnmatch(basename, p) for p in patterns)
				if matched:
					filename = os.path.join(root, basename)
					yield [filename, basename]
