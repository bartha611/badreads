import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

os.environ["DATABASE_URL"] = "postgres://rstrmsgknaerel:b27002260a792f02d00ba9d23da8e41d1d7a375ea03aa44210fcf8fe4b082a86@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dfofnj4eu4rg1q"

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
	f = open("books.csv")
	reader = csv.reader(f)
	for isbn, title, author, year in reader:
		db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:i, :t, :a, :y)", 
					{"i": isbn, "t": title, "a": author, "y": year})
		print(f"Added {isbn}, {title}, {author}, and {year} to database")
		db.commit()



if __name__ == '__main__':
	main()

