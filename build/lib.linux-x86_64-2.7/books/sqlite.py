import sqlite3 as lite

class SQLite:
	def get_con():
		return self._con

	con = property(get_con)

	def __init__(self):
		self._con = None

	def open(self, path):
		"""opens a new connection"""
		try:
			self._con = lite.connect(path)
		except lite.Error, e:
			print e
			print path

	def close(self):
		"""closes the current connection"""
		if self._con:
			try:
				self._con.close()
			except lite.Error, e:
				print e

	def execute(self, query, data=()):
		"""executes the given query and returns the results"""
		if self._con:
			try:
				cur = self._con.cursor()
				if data == ():
					cur.execute(query)
				else:
					cur.execute(query, data)
				rows = cur.fetchall()
				return rows
			except lite.Error, e:
				print e

		return None

	def executemany(self, query, data):
		"""executes the given query with executemany()"""
		if self._con:
			try:
				cur = self._con.cursor()
				cur.executemany(query, data)
			except lite.Error, e:
				print e

	def commit(self):
		"""commits changes to the database"""
		if self._con:
			try:
				self._con.commit()
			except lite.Error, e:
				self._con.rollback()
				print e

	def contains(self, query, data=()):
		"""checks wheter the given query has results or not"""
		if self._con:
			try:
				cur = self._con.cursor()
				if data == ():
					cur.execute(query)
				else:
					cur.execute(query, data)
				rows = cur.fetchone()

				if rows:
					return True;
				else:
					return False;
			except lite.Error, e:
				print e
