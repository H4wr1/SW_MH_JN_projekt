import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def scrape_and_save_to_csv():
    base_url = "https://lubimyczytac.pl/katalog?page={}&listId=booksFilteredList&category[]=53&rating[]=0&rating[]=10&publishedYear[]=1200&publishedYear[]=2024&catalogSortBy=published-desc&paginatorType=Standard"

    scraped_data = []

    for page_number in range(1, 335):
        url = base_url.format(page_number)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            book_elements = soup.find_all('a', class_='authorAllBooks__singleTextTitle float-left')

            for book_element in book_elements:
                book_link = urljoin(base_url, book_element['href'])
                book_response = requests.get(book_link)

                if book_response.status_code == 200:
                    book_soup = BeautifulSoup(book_response.content, 'html.parser')

                    book_title_elem = book_soup.find('h1', class_='book__title')
                    book_title = None
                    try:
                        book_title = book_title_elem.text.strip() if book_title_elem else None
                    except AttributeError:
                        pass

                    author_name_elem = book_soup.find('a', class_='link-name d-inline-block')
                    author_name = None
                    try:
                        author_name = author_name_elem.text.strip() if author_name_elem else None
                    except AttributeError:
                        pass

                    description_elem = book_soup.find('div', id='book-description')
                    description = None
                    try:
                        description = description_elem.find('p').text.strip() if description_elem else None
                    except AttributeError:
                        pass

                    print(f"Book Title: {book_title}")
                    print(f"Author Name: {author_name}")
                    print(f"Description: {description}")

                    collapse_element = book_soup.find('div', class_='collapse', id='book-details')
                    if collapse_element:
 
                        details_dl = collapse_element.find('dl')
                        if details_dl:
                            details_dict = dict(zip(
                                (dt.text.strip() for dt in details_dl.find_all('dt')),
                                (dd.text.strip() for dd in details_dl.find_all('dd'))
                            ))

                            release_date = details_dict.get('Data wydania:')
                            page_count = details_dict.get('Liczba stron:')
                            language = details_dict.get('Język:')

                            print(f"Release Date: {release_date}")
                            print(f"Page Count: {page_count}")
                            print(f"Language: {language}")

                        scraped_data.append({
                            'book_title': book_title,
                            'author_name': author_name,
                            'release_date': release_date,
                            'page_count': page_count,
                            'language': language,
                            'description': description,
                            'book_link': book_link
                        })

                    else:
                        print(f"Error: Book details section not found on page {book_link}")
                else:
                    print(f"Error: Unable to fetch book page {book_link}. Status code: {book_response.status_code}")
        else:
            print(f"Error: Unable to fetch page {page_number}. Status code: {response.status_code}")

    csv_filename = "scraped_datav2.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['book_title', 'author_name', 'release_date', 'page_count', 'language', 'description', 'book_link']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for data_entry in scraped_data:
            writer.writerow(data_entry)

    print(f"Scraped data saved to {csv_filename}")

if __name__ == "__main__":
    scrape_and_save_to_csv()
