import csv

your_string = "Poznajcie poczńÖtki historii Durzo Blinta, ..."

# Specify the file name
file_name = "your_file.csv"

# Open the file in write mode with UTF-8-SIG encoding
with open(file_name, mode='w', encoding='utf-8', newline='') as file:
    # Create a CSV writer
    writer = csv.writer(file)

    # Write the string to the CSV file
    writer.writerow([your_string])