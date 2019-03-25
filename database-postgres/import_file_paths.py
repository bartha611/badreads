import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

os.environ["DATABASE_URL"] = os.getenv('DATABASE_URL')
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

def main():
	url = 'https://s3.us-east-2.amazonaws.com/bartha611bucket1/Covers/'

	with open('books.csv', 'r') as f:
		reader = csv.reader(f)
		for data in reader:
			isbn = data[0]
			full_url = url + str(isbn) + '.jpg'
			db.execute("""
				UPDATE books
					SET image_path = :full_url
				WHERE isbn = :isbn""",{"full_url":full_url, "isbn":isbn})
			db.commit()
			print(f"added {isbn} file path to database")


if __name__ == '__main__':
	main()
