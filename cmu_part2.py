import csv
input_file_path = 'booksummaries_with_page_count.txt'
output_file_path = 'cmu_cleaned.txt'

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Write the header to the output file
    output_file.write(input_file.readline())

    # Iterate through each line in the input file
    for line in input_file:
        # Split the line into columns using tab as the separator
        columns = line.strip().split('\t')

        # Check if the "Page count" column is not None
        if columns[7] != 'None' and columns[4]:
            # Write the line to the output file
            output_file.write(line)


print("Rows with Page count=None removed. Output written to", output_file_path)


input_file_path = 'cmu_cleaned.txt'
csv_output_file_path = 'cmu_cleaned.csv'

# Define the CSV header
csv_header = ['book_title', 'author_name', 'release_date', 'page_count', 'language', 'description', 'book_link']

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(csv_output_file_path, 'w', encoding='utf-8', newline='') as csv_output_file:
    # Create a CSV writer
    csv_writer = csv.writer(csv_output_file)
    
    # Write the header to the CSV file
    csv_writer.writerow(csv_header)

    # Iterate through each line in the filtered input file
    for line in input_file:
        # Split the line into columns using tab as the separator
        columns = line.strip().split('\t')

        # Extract relevant columns based on the provided structure
        book_title = columns[2]
        author_name = columns[3]
        release_date = columns[4]
        page_count = columns[7]
        language = 'angielski'  # Add "angielski" to the language column
        description = columns[6]
        
        # Construct the book link using Wikipedia article ID
        wikipedia_article_id = columns[0]
        book_link = f'https://en.wikipedia.org/w/index.php?curid={wikipedia_article_id}'

        # Write the extracted data to the CSV file
        csv_writer.writerow([book_title, author_name, release_date, page_count, language, description, book_link])

print("CSV file created. Output written to", csv_output_file_path)

