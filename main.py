import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import sys

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'

if (__name__ == '__main__'):
	if (len(sys.argv) < 2):
		print('Usage: main.py <url> (No trailing slash)')
		sys.exit(1)

	url = sys.argv[1]

	response = requests.get(url, headers={'User-Agent': user_agent})

	soup = BeautifulSoup(response.text, 'lxml')

	# Details
	title = soup.find('title') != None and soup.find('title').text or 'No title'
	description = soup.find('meta', { 'name': 'description' }) != None and soup.find('meta', { 'name': 'description' })['content'] or None
	manifest_href = soup.find('link', { 'rel': 'manifest' }) != None and soup.find('link', { 'rel': 'manifest' })['href'] or None
	manifest_url = url + "/" + manifest_href.split('/')[-1] if manifest_href != None else None
	
	print('Title: ' + title if title != None else 'No title')
	print('Description: ' + description if description != None else 'No description')
	print('Manifest: ' + manifest_url if manifest_url != None else 'No manifest')

	# Manifest
	manifest = None
	icon_url = None
	if (manifest_url != None):
		manifest = requests.get(manifest_url).json()
		icons = manifest['icons']

		# Icons
		for icon in icons:
			if (icon['sizes'] == '512x512'):
				if str(icon['src']).startswith('http'):
					icon_url = icon['src']
				elif str(icon['src']).startswith('./'):
					icon_url = url + "/" + str(icon['src']).removeprefix('./')
				elif str(icon['src']).startswith('/'):
					icon_url = url + "/" + str(icon['src']).removeprefix('/')
				else:
					icon_url = url + "/" + str(icon['src']).removeprefix('./')
				break

		if (icon_url == None):
			for icon in icons:
				if (icon['sizes'] == '192x192'):
					if str(icon['src']).startswith('http'):
						icon_url = icon['src']
					elif str(icon['src']).startswith('./'):
						icon_url = url + "/" + str(icon['src']).removeprefix('./')
					else:
						icon_url = url + "/" + str(icon['src']).removeprefix('./')
					break

	# Icon conversion
	if (icon_url):
		response = requests.get(icon_url, headers={'User-Agent': user_agent}, stream=True)

		print("Icon URL: " + icon_url)

		# Convert to webp
		if (response.ok):
			icon = Image.open(BytesIO(response.content))

			icon.save('icon-large.webp', format='webp', optimize=True, quality=95)
			
			icon.resize((128, 128)).save('icon-small.webp', format='webp', optimize=True, quality=95)

			print("Icons generated")