import requests
from bs4 import BeautifulSoup
import sys

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'

if (__name__ == '__main__'):
	if (len(sys.argv) < 2):
		print('Usage: main.py <url>')
		sys.exit(1)

	url = sys.argv[1]

	response = requests.get(url, headers={'User-Agent': user_agent})

	soup = BeautifulSoup(response.text, 'lxml')

	# Details
	title = soup.find('title') and soup.find('title').text or 'No title'
	description = soup.find("meta", { 'name': 'description' }) and soup.find('meta', { 'name': 'description' })['content'] or "No description"

	print(title)
	print(description)