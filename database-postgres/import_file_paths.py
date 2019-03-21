import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

os.environ["DATABASE_URL"] = 'postgres://rstrmsgknaerel:b27002260a792f02d00ba9d23da8e41d1d7a375ea03aa44210fcf8fe4b082a86@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dfofnj4eu4rg1q'
engine = create_engine('postgres://rstrmsgknaerel:b27002260a792f02d00ba9d23da8e41d1d7a375ea03aa44210fcf8fe4b082a86@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dfofnj4eu4rg1q')
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
