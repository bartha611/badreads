import csv,os
import urllib.request,json 

def main():
	with open('books.csv') as f:
		bookreader = csv.reader(f)
		for row in bookreader:
			isbn = row[0]
			image_file = isbn + '.jpg'
			size = os.path.getsize(image_file)
			index = 1
			if size < 1000:
				print(f"{isbn} has size {size} bytes")
				google_book_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + '&key=AIzaSyA7LSBWRzf5_ee1zvcJAYbAtQT0lBpZLSY'
				response = urllib.request.urlopen(google_book_url)
				data = json.loads(response.read())
				try:
					cover_image_url = data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
					urllib.request.urlretrieve(cover_image_url, image_file)
				except:
					print(f"{isbn} not present in google api")

if __name__ == '__main__':
	main()
