import csv,os 

with open('books.csv') as f:
	bookreader = csv.reader(f)
	for row in bookreader:
		isbn = row[0]
		img_file = isbn + '.jpg'
		size = os.path.getsize(img_file)
		if size < 1000:
			print(f"{isbn} has no cover image")