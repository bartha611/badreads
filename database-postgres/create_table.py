import psycopg2


def main():
	conn = psycopg2.connect(dbname = "database", host = "localhost", user = "user", 
		password = "password", port = "port")
	cursor = conn.cursor()
	sql_file = open('schema.sql', 'r').read()
	cursor.execute(sql_file)
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
	main()
