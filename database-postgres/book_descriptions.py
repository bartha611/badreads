import csv,os,requests,json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

os.environ["DATABASE_URL"] = os.getenv('DATABASE_URL')
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	with open('books.csv') as f:
		bookreader = csv.reader(f)
		count = 0
		for row in bookreader:
			isbn = row[0]
			title = row[1]
			author = row[2]
			title.rstrip()
			title = title.replace(" ", "+")
			author = author.replace(" ","+")
			api = "https://www.googleapis.com/books/v1/volumes?q=" + title + "q=inauthor:" + author + "&key=AIzaSyAb4Ee1FfZWCHCgW08UFESFw_jfzZK27x0"
			if count > 2217:
				try:
					response = requests.get(api)
					if response.status_code != 200:
						print(response)
						print(count)
						break
					objects = response.json()
					description = objects['items'][0]['volumeInfo']['description']
					db.execute("""
						UPDATE books
							SET book_description = :description
						WHERE isbn = :isbn""",{"isbn":isbn,"description":description})
					db.commit()
					print(f"added {title} book description to database")
					count += 1
				except:
					with open("nodescription.csv","a") as csvFile:
						writer = csv.writer(csvFile)
						writer.writerow(row)
					csvFile.close()
					print(f"Could not add {title} book description to database")
			else:
				count += 1
		db.close()
if __name__ == '__main__':
	main()
