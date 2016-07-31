import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import psycopg2 as pg
import sys

def connect():
	#Define our connection string
	conn_string = "host='localhost' dbname='movies' user='postgres' password='secret'"

	# print the connection string we will use to connect
	print "Connecting to database\n	-> {0}".format(conn_string)

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = pg.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	print "Connected!\n"
	return conn, cursor

def execute_find_movie(title, year):
	# execute our Query
	records1 = records2 = []
	conn.rollback()
	try:
		cursor.execute('SELECT * FROM title WHERE title = {0} AND production_year = {1} AND kind_id = 1 LIMIT 15'.format(title, year))
		records1 = cursor.fetchall()
	except:
		conn.rollback()
		print "error 1: " + title
	try:
		print type(title)
		print type(year)
		cursor.execute('SELECT * FROM aka_title WHERE title = {0} AND production_year = {1} AND kind_id = 1 LIMIT 15'.format(title, year))
		records2 = cursor.fetchall()
	except:
		conn.rollback()
		print "error 2: " + title

	records = records1 + records2

	if len(records) == 0:
		titles_to_redo.append([title, year])
	return records

def prepare_title(title):
	new_title = None
	return new_title

if __name__ == "__main__":
	conn, cursor = connect()
	df = pd.read_csv('search_titles.csv')
	df.drop('Unnamed: 0', axis=1, inplace=True)
	titles_to_redo = []

	columns = ['id', 'title', 'production_year', 'md5sum']
	df_records = pd.DataFrame(columns = columns)

	psql_cols = ['id', 'title', 'imdb_index', 'kind_id', 'production_year', 'imdb_id', 'phonetic_code', 'episode_of_id', 'season_nr', 'episode_nr', 'series_years', 'md5sum']
	i = 0
	for title, year in df.get_values().tolist():
		records = execute_find_movie(title, year)
		if len(records) != 0:
			df_titles = pd.DataFrame(records, columns=psql_cols)
			df2 = df_titles[columns]
			df_records = df_records.append(df2, ignore_index=True)
		else:
			i += 1
			print i
			pass

	int_columns = ['id','production_year']
	df_records[int_columns] = df_records[int_columns].astype(int)
	df_records.to_csv('cluster_data.csv', mode = 'w', index=False)

# where movetitle like '%10,000%'
#
# cursor.execute("SELECT * FROM aka_title WHERE title = 'Legally Blonde 2: Red, White and Blonde' AND production_year = 2014 AND kind_id = 1 LIMIT 15")

# cursor.execute("SELECT * FROM title WHERE title = 'After Earth' LIMIT 15")
# records1 = cursor.fetchall()
# cursor.execute("SELECT * FROM title WHERE title like 'Hunger Games%' LIMIT 15")
# records2 = cursor.fetchall()
