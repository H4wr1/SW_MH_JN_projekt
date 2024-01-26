import requests
from bs4 import BeautifulSoup
import re

def get_page_count(wikipedia_article_id):
    try:

        url = f'https://en.wikipedia.org/w/index.php?curid={wikipedia_article_id}'

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        infobox_table = soup.find('table', class_='infobox vcard')

        pages_row = infobox_table.find('th', text='Pages')

        page_count_cell = pages_row.find_next('td', class_='infobox-data')

        page_count = int(re.search(r'\d+', page_count_cell.text).group())
        print("page")
        return page_count
    except Exception as e:
        print(f"Error processing Wikipedia article {wikipedia_article_id}: {str(e)}")
        return None

def add_page_count_to_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(lines[0].strip() + '\tPage Count\n')  

        for line in lines[1:]:
            columns = line.strip().split('\t')
            wikipedia_article_id = columns[0]
            page_count = get_page_count(wikipedia_article_id)

            file.write(line.strip() + f'\t{page_count}\n')

if __name__ == "__main__":
    input_file_path = 'booksummaries.txt'
    output_file_path = 'booksummaries_with_page_count.txt'
    add_page_count_to_file(input_file_path, output_file_path)
