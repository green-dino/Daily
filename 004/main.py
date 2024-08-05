import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils import extract_base_url, fix_url, delay, create_session


class ImageDownloader:
    def __init__(self, save_dir="./IMAGES/"):
        self.save_dir = save_dir

    def download_image(self, img_url):
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # Raise an error for bad responses
            img_name = os.path.basename(urlparse(img_url).path)
            img_output_path = os.path.join(self.save_dir, img_name)

            with open(img_output_path, 'wb') as out_file:
                out_file.write(response.content)
            return img_output_path
        except requests.RequestException as e:
            return f"Network error: {e}"
        except IOError as e:
            return f"File error: {e}"

class ContentExtractor:
    def __init__(self, save_dir="./IMAGES/"):
        self.image_downloader = ImageDownloader(save_dir)
    
    def extract_content(self, url):
        self.url = fix_url(url)  # Fix URL before making a request
        base = extract_base_url(url)
        if not os.path.exists(self.image_downloader.save_dir):
            os.makedirs(self.image_downloader.save_dir)

        try:
            page = requests.get(self.url)
            page.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            return f"Network error: {e}", [], []

        soup = BeautifulSoup(page.text, 'html.parser')

        page_title = soup.title.string if soup.title else "No Title Found"
        page_links = [link.get('href') for link in soup.find_all('a') if link.get('href')]

        images_found = []
        for img in soup.find_all('img'):
            img_url = img.get('src') or img.get('data-src')
            if img_url:
                img_url = fix_url(img_url)
                img_path = self.image_downloader.download_image(img_url)
                if img_path and "error" not in img_path:
                    images_found.append((img_url, img_path))

        return page_title, page_links, images_found

class ImageInfoDisplayer:
    @staticmethod
    def display_image_info(url):
        url = fix_url(url)
        try:
            page = requests.get(url)
            page.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return

        soup = BeautifulSoup(page.text, 'html.parser')
        images = soup.findAll('img')

        for each_image in images:
            img_url = each_image.get('src') or each_image.get('data-src')
            if img_url:
                alt_text = each_image.get('alt', 'No alternate text available')
                print("Image URL:", img_url)
                print("Alternate Text:", alt_text)
                print()

class PageLinkScanner:
    def __init__(self):
        self.page_links = set()

    def recurse_url(self, new_url, base, local):
        try:
            page = requests.get(new_url)
            page.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(page.text, 'html.parser')

            links = soup.findAll('a')
            for each_link in links:
                new_link = each_link.get('href')

                if new_link:
                    if 'http' not in new_link:
                        new_link = base + new_link

                    if local in new_link and new_link not in self.page_links:
                        self.page_links.add(new_link)
                        self.recurse_url(new_link, base, local)

        except requests.RequestException as err:
            print(f"Network error: {err}")

    def scan_page_links(self, base_url, must_include):
        base_domain = extract_base_url(base_url)
        self.page_links.add(base_url)
        print("\nScanning:", base_url, '\n')
        self.recurse_url(base_url, base_domain, must_include)
        print("\nScanning Complete\n")
        print("Unique URLs Discovered\n")
        for each_entry in self.page_links:
            print(each_entry)
        print('\n\nScript Complete')

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")

    content_extractor = ContentExtractor()
    title, links, images = content_extractor.extract_content(website_url)

    print("\nPage Title:", title)
    print("\nPage Links:")
    for link in links:
        print(link)

    print("\nImages Found:")
    for img_url, img_path in images:
        print(f"URL: {img_url}, Saved Path: {img_path}")

    print("\nImage Information:")
    ImageInfoDisplayer.display_image_info(website_url)

    base_url = input("Enter the base URL to scan (e.g., 'https://www.example.com/'): ")
    must_include = input("Enter the keyword that must be included in the URL (e.g., 'example'): ")

    if base_url and must_include:
        page_link_scanner = PageLinkScanner()
        page_link_scanner.scan_page_links(base_url, must_include)
    else:
        print("Base URL and must-include keyword cannot be empty.")