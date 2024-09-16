from flask import Flask, render_template, request, send_from_directory, abort
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import zipfile
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'public'), static_url_path='')

def fetch_html_with_selenium(url, browser='chrome'):
    if browser == 'chrome':
        options = ChromeOptions()
        options.headless = True
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == 'firefox':
        options = FirefoxOptions()
        options.headless = True
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == 'edge':
        options = EdgeOptions()
        options.headless = True
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    else:
        raise ValueError("Unsupported browser. Choose 'chrome', 'firefox', or 'edge'.")
    driver.get(url)
    time.sleep(10)
    html_content = driver.page_source
    driver.quit()
    return html_content

def extract_css_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = [urljoin(base_url, link['href']) for link in soup.find_all('link', rel='stylesheet')]
    return links

def download_css_files(css_links):
    css_contents = {}
    for link in css_links:
        try:
            response = requests.get(link)
            response.raise_for_status()
            css_contents[link] = response.text
        except requests.RequestException as e:
            print(f"Failed to download CSS from {link}: {e}")
    return css_contents

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def insert_css_links_into_html(html, css_filenames):
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.head if soup.head else soup.new_tag('head')
    if not soup.head:
        soup.insert(0, head)
    for css_filename in css_filenames:
        link_tag = soup.new_tag('link', rel='stylesheet', href=css_filename)
        head.append(link_tag)
    return str(soup)

def create_zip_file(files, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))

def clean_up_old_files(folder):
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        browser = request.form['browser']
        clean_up_old_files(os.path.join(BASE_DIR, 'public/css'))
        clean_up_old_files(os.path.join(BASE_DIR, 'public'))
        html = fetch_html_with_selenium(url, browser)
        css_links = extract_css_links(html, url)
        css_files = download_css_files(css_links)
        css_folder = os.path.join(BASE_DIR, 'public/css')
        os.makedirs(css_folder, exist_ok=True)
        css_filenames = []
        timestamp = int(time.time())
        for i, (link, content) in enumerate(css_files.items(), start=1):
            css_filename = os.path.join(css_folder, f'style_{timestamp}_{i}.css')
            save_to_file(content, css_filename)
            css_filenames.append(css_filename)
        updated_html = insert_css_links_into_html(html, css_filenames)
        html_filename = os.path.join(BASE_DIR, f'public/output_{timestamp}.html')
        save_to_file(updated_html, html_filename)
        zip_filename = os.path.join(BASE_DIR, f'public/snapshot_{timestamp}.zip')
        files_to_zip = [html_filename] + css_filenames
        create_zip_file(files_to_zip, zip_filename)
        return render_template('result.html', zip_file=f'/public/snapshot_{timestamp}.zip')
    return render_template('index.html')

@app.route('/public/<path:filename>')
def download_file(filename):
    file_path = os.path.join(BASE_DIR, 'public', filename)
    if os.path.exists(file_path):
        return send_from_directory(os.path.join(BASE_DIR, 'public'), filename, as_attachment=True)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
