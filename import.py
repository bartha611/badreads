import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

os.environ["DATABASE_URL"] = "dababase_url"
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

