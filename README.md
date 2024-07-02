# Eden-Internshio: Milestone 1
# Web Page Snapshot

## Introduction

Web Page Snapshot is a web tool designed to capture and download the HTML and CSS content of web pages. It provides a user-friendly interface for inputting a URL and selecting a browser, then generates a downloadable ZIP file containing the HTML and CSS files of the specified web page.

## Features

- Fetches HTML content of a web page using Selenium.
- Extracts and downloads all linked CSS files.
- Inserts CSS links into the HTML content.
- Packages the HTML and CSS files into a ZIP file for easy download.

## Requirements

- Python 3.6 or higher
- Flask
- Requests
- BeautifulSoup4
- Selenium
- WebDriver Manager

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Asmaa2222/web-page-snapshot.git
   cd web-page-snapshot
2. Create a virtual machine (optionall)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the required dependencies
   ```bash
   pip install -r requirements.txt

## Usage 
1. Run the Flask app:
   ```bash 
   python app.py
2. Open a web browser and navigate to http://localhost:5000/.
3. Enter the URL of the web page you want to snapshot and select a browser (Chrome, Firefox, or Edge).
4. Click "Generate Files" to fetch and process the HTML and CSS content.
5. Download the resulting ZIP file containing the HTML and CSS files.

   ## Project Structure

- `app.py`: The main Flask application file.
- `templates/`: Directory containing HTML templates.
  - `index.html`: The main interface for inputting URLs and selecting a browser.
  - `result.html`: The interface for downloading the generated ZIP file.
- `public/`: Directory where generated files (HTML, CSS, and ZIP) are stored.

## Functions

### `fetch_html_with_selenium(url, browser='chrome')`

Fetches the HTML content of a given URL using Selenium.

**Parameters**:
- `url`: The URL of the webpage to fetch.
- `browser`: The browser to use for fetching the webpage (default is Chrome).

**Returns**: The HTML content of the webpage.

### `extract_css_links(html, base_url)`

Extracts and returns CSS file links from the HTML content.

**Parameters**:
- `html`: The HTML content to parse.
- `base_url`: The base URL to resolve relative links.

**Returns**: A list of CSS links.

### `download_css_files(css_links)`

Downloads each CSS file and returns their content.

**Parameters**:
- `css_links`: A list of URLs to CSS files.

**Returns**: A dictionary with CSS file URLs as keys and their content as values.

### `save_to_file(content, filename)`

Saves content to a specified file.

**Parameters**:
- `content`: The content to save.
- `filename`: The name of the file to save the content to.

### `insert_css_links_into_html(html, css_filenames)`

Inserts `<link>` tags for CSS files into HTML content.

**Parameters**:
- `html`: The HTML content to modify.
- `css_filenames`: A list of CSS filenames to insert into the HTML.

**Returns**: The modified HTML content.

### `create_zip_file(files, zip_filename)`

Creates a ZIP file containing the specified files.

**Parameters**:
- `files`: A list of file paths to include in the ZIP file.
- `zip_filename`: The name of the resulting ZIP file.

## Flask Routes

### `@app.route('/', methods=['GET', 'POST'])`

Handles the index page and form submissions.

- **GET**: Renders the `index.html` template.
- **POST**: Processes the form submission to fetch and process HTML and CSS content from a URL.
  - Fetches HTML content using `fetch_html_with_selenium`.
  - Extracts CSS links using `extract_css_links`.
  - Downloads CSS files using `download_css_files`.
  - Saves CSS files to the `public/css` directory.
  - Inserts CSS links into the HTML content using `insert_css_links_into_html`.
  - Saves the modified HTML content to `public/output.html`.
  - Creates a ZIP file containing the HTML and CSS files.
  - Renders the `result.html` template with a link to download the ZIP file.

### `@app.route('/public/<path:filename>')`

Serves files from the public directory.

**Parameters**:
- `filename`: The name of the file to serve.

**Returns**: The requested file as a download.



