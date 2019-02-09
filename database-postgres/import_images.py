import csv
import urllib.request

def main():
	with open('books.csv','r') as csvfile:
		bookreader = csv.reader(csvfile)
		for row in bookreader:
			isbn = row[0]
			cover_image_url = 'http://covers.openlibrary.org/b/isbn/' + row[0] + '-M.jpg'
			img_src = isbn + '.jpg'
			urllib.request.urlretrieve(cover_image_url,img_src)
			print(f"added {isbn} to cover image folder")
			
if __name__ == '__main__':
	main()