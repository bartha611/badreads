import psycopg2

def main():
	conn = psycopg2.connect(dbname = "dfofnj4eu4rg1q", host = "ec2-23-23-80-20.compute-1.amazonaws.com", user = "rstrmsgknaerel", 
		password = "b27002260a792f02d00ba9d23da8e41d1d7a375ea03aa44210fcf8fe4b082a86", port = "5432")
	cursor = conn.cursor()
	