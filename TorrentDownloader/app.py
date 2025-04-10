import os
import time
import requests
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # ✅ Correct import
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver(download_dir):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # More stable headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service()  # Assumes chromedriver is in PATH
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def resolve_js_link(url, driver):
    driver.get(url)
    try:
        print("Waiting for download button to appear...")
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Continue to download")]'))
        )
        download_url = download_button.get_attribute('href')
        print("Resolved link:", download_url)
        return download_url
    except Exception as e:
        print(f"[!] Error resolving JS-based link: {e}")
        return None

def download_file(url, output_folder):
    local_filename = os.path.join(output_folder, url.split('/')[-1])
    print(f"Starting download: {local_filename}")
    try:
        with requests.get(url, stream=True) as response:
            total_size = int(response.headers.get('content-length', 0))
            with open(local_filename, 'wb') as file, tqdm(
                desc=local_filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        bar.update(len(chunk))
        print(f"[+] Download complete: {local_filename}")
        return local_filename
    except Exception as e:
        print(f"[!] Download failed for {url}: {e}")
        return None

def is_direct_link(url):
    return url.endswith(('.rar', '.zip', '.7z', '.bin', '.iso'))

def main():
    input_file = 'files.txt'
    output_folder = 'downloads'
    os.makedirs(output_folder, exist_ok=True)

    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    driver = setup_driver(os.path.abspath(output_folder))
    print(f"[+] Resolving & downloading {len(urls)} links...\n")

    for url in urls:
        print(f"Processing: {url}")
        if is_direct_link(url):
            download_file(url, output_folder)
        else:
            resolved_url = resolve_js_link(url, driver)
            if resolved_url:
                download_file(resolved_url, output_folder)
            else:
                print(f"[!] Skipping {url} — Could not resolve final download link.")

    driver.quit()

if __name__ == "__main__":
    main()
