# Date: 4/3/2023 -- DD/MM/YYYY
# WebSite -- > https://doris.ffessm.fr/find/species/
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import csv


def scrape_data(url):
    """
    Scrape data from a given URL.

    Args:
        url (str): The URL to scrape data from.

    Returns:
        original_name (list): A list of original names.
        latin_name (list): A list of Latin names.
        des_link (list): A list of description links.
        img_link (list): A list of image links.
    """
    original_name = []
    latin_name = []
    des_link = []
    img_link = []

    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, 'lxml')

    names = soup.find_all("div", {"class": "padder"})

    for name in names:
        full_name = name.find("a").text.strip()
        stop = full_name.find('\n')
        original_name.append(full_name[0:stop])
        latin_name.append(full_name[stop + 1:])
        des_link.append(name.find("a").attrs['href'])

    img_span = soup.find_all("span", {"class": "pull-right"})
    for img in img_span:
        img_link.append("https://doris.ffessm.fr" + img.find("img").attrs['src'])

    return original_name, latin_name, des_link, img_link


def export_data(data_columns, file_path):
    """
    Export data to a CSV file.

    Args:
        data_columns (list): A list of columns containing the data to export.
        file_path (str): The path to the CSV file to create.

    Returns:
        None
    """
    zipped_data = zip_longest(*data_columns)

    with open(file_path, "w", encoding='utf-8-sig', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["Name", "Latin Name", "Description Link", "Image Link"])
        writer.writerows(zipped_data)

    print(f"File created: {file_path}.")


def main():
    """
    The main entry point for the program.

    Args:
        None

    Returns:
        None
    """
    page_num = 0
    page_limit = 5124
    data_columns = [[], [], [], []]

    while True:
        url = f"https://doris.ffessm.fr/find/species/(offset)/{page_num}"
        original_name, latin_name, des_link, img_link = scrape_data(url)

        if page_num > page_limit:
            print("Pages ended, wait for file creation...")
            break

        data_columns[0].extend(original_name)
        data_columns[1].extend(latin_name)
        data_columns[2].extend(des_link)
        data_columns[3].extend(img_link)

        page_num += 21
        print(f"Page Switched [{page_num}].")

    file_path = r"AllData.csv"
    export_data(data_columns, file_path)


if __name__ == "__main__":
    main()

# Coded By Mahmoud Dwidar
# GitHub -- > https://github.com/mahmouddwidar