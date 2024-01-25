from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def scrape_website():
    # URL pattern to scrape multiple pages
    base_url = "https://lubimyczytac.pl/katalog?page={}&listId=booksFilteredList&category[]=41&rating[]=0&rating[]=10&publishedYear[]=1200&publishedYear[]=2024&catalogSortBy=published-desc&paginatorType=Standard"

    # Initialize an empty list to store scraped data
    scraped_data = []

    # Iterate over 334 pages
    for page_number in range(1, 335):
        # Construct the URL for each page
        url = base_url.format(page_number)

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract information from the page as needed
            # Example: Get the title of the page
            page_title = soup.title.text

            # Append the scraped information to the list
            scraped_data.append({
                'page_number': page_number,
                'page_title': page_title
                # Add more data extraction as needed
            })
        else:
            # Print an error message if the request was not successful
            print(f"Error: Unable to fetch page {page_number}. Status code: {response.status_code}")

    # Return the scraped data as a response
    return render_template('index.html', scraped_data=scraped_data)

if __name__ == '__main__':
    app.run(debug=True)
