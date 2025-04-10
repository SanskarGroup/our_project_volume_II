import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm

def extract_external_links(url):
    print(f"[+] Scraping: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Only keep full or relative URLs that point outside the current domain
        full_url = urljoin(url, href)
        links.append(full_url)

    print(f"[+] Found {len(links)} links")
    return links

def resolve_final_download_url(url):
    try:
        # HEAD first to follow redirects quickly
        response = requests.head(url, allow_redirects=True, timeout=10)
        final_url = response.url

        # Fallback to GET if HEAD fails or no content-length
        if not response.ok or 'content-length' not in response.headers:
            response = requests.get(url, allow_redirects=True, stream=True, timeout=10)
            final_url = response.url

        if final_url.endswith(('.rar', '.bin')):
            return final_url
    except Exception as e:
        print(f"[!] Error resolving {url}: {e}")
    return None

def download_file(url, output_folder='downloads'):
    os.makedirs(output_folder, exist_ok=True)
    local_filename = os.path.join(output_folder, url.split('/')[-1])

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(local_filename, 'wb') as file, tqdm(
        desc=local_filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        dynamic_ncols=True,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))

    print(f"[+] Download complete: {local_filename}")

def main():
    page_url = input("Enter the FitGirl paste URL: ").strip()
    intermediate_links = extract_external_links(page_url)

    download_links = []
    for link in intermediate_links:
        final_url = resolve_final_download_url(link)
        if final_url:
            print(f"[✔] Found downloadable: {final_url}")
            download_links.append(final_url)

    print(f"\n[+] Total downloadable files: {len(download_links)}\n")
    for link in download_links:
        try:
            download_file(link)
        except Exception as e:
            print(f"[!] Failed to download {link}: {e}")

if __name__ == "__main__":
    main()
