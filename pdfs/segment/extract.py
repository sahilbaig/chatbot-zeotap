import requests
import xml.etree.ElementTree as ET
import pdfkit
import os

# List of sitemaps from robots.txt
sitemaps = [
    "https://segment.com/docs/sitemap.xml",
]

# Headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Path to wkhtmltopdf executable
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Update this path
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Function to extract URLs from a sitemap
def extract_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url, headers=headers)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
            return urls
        else:
            print(f"Failed to fetch {sitemap_url}: Status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Error parsing {sitemap_url}: {e}")
        return []

# Function to download a URL as a PDF
def download_as_pdf(url):
    try:
        # Create a filename from the URL
        filename = url.split('/')[-2] + ".pdf"
        # Convert the URL to a PDF
        pdfkit.from_url(url, filename, configuration=config)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url} as PDF: {e}")

# Main script
for sitemap in sitemaps:
    print(f"Processing sitemap: {sitemap}")
    urls = extract_urls_from_sitemap(sitemap)
    for url in urls:
        download_as_pdf(url)