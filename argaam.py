# Date: 4/2/2023 -- DD/MM/YYYY
# WebSite -- > https://www.argaam.com/ar/monitors/market-ownership/3
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import csv


def main(page_url):
    """
        Fetches the whole page and extracts data of gainers and losers tables

        Args:
            page_url: URL of the page to be scraped
    """
    page = requests.get(page_url)

    # Check if the request was successful
    try:
        page.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return f"An HTTP error occurred: {e}"

    src = page.content
    soup = BeautifulSoup(src, "lxml")

    def gainers():
        """
        Getting the all info. of gainers table

        Args:
            None

        Returns:
            None
        """
        print("Getting The Gainers Data...")
        # Saving The Data
        nums_of_gainers: list = []  # Write in the CSV file like that ==> nums_of_gainers[::2]
        company_name: list = []  # It will be written like that ==> company_name[::2]
        start: list = []  # It will be written like that ==> start[::2]
        end: list = []  # It will be written like that ==> end[::2]
        change: list = []  # It will be written like that ==> change[::2]

        # Getting First and last Date
        first_date = soup.find("div", {"id": "gainersList"}).find("th", {"class": "firstDate"}).text.strip()
        last_date = soup.find("div", {"id": "gainersList"}).find("th", {"class": "lastDate"}).text.strip()

        # finding the gainers list in the table
        gainers_list = soup.find("div", {"id": "gainersList"})
        # Getting all rows
        tr_list = gainers_list.find_all("tr", {"class": "argaam-font dataRow"})
        # Looping on all rows to get all info.
        for i in tr_list:
            nums_of_gainers.append(i.contents[1].text.strip())
            company_name.append(i.contents[3].find("a").text.strip())
            start.append(i.contents[5].text.strip())
            end.append(i.contents[7].text.strip())
            change.append(i.contents[9].text.strip())

        # unpacking all data to give every row its specific data
        file_list: list = [nums_of_gainers[::2], company_name[::2], start[::2], end[::2], change[::2]]
        exported: zip_longest = zip_longest(*file_list)

        with open(r"D:\Python\web Scrapping\upWork\Argaam\Gainers.csv", "w", encoding='utf-8-sig') as output_file:
            wr = csv.writer(output_file)
            wr.writerow(["الترتيب", "الشركة", f"{first_date}", f"{last_date}", "التغير"])
            wr.writerows(exported)
            print("Gainers File Created.")

    gainers()

    def losers():
        """
        Getting the all info. of losers table

        Args:
            None

        Returns:
            None
        """
        print("Getting The Losers Data...")
        # Saving The Data
        nums_of_losers: list = []  # Write in the CSV file like that ==> nums_of_losers[::2]
        company_name: list = []  # It will be written like that ==> company_name[::2]
        start: list = []  # It will be written like that ==> start[::2]
        end: list = []  # It will be written like that ==> end[::2]
        change: list = []  # It will be written like that ==> change[::2]

        # Getting First and last Date
        first_date = soup.find("div", {"id": "loosersList"}).find("th", {"class": "firstDate"}).text.strip()
        last_date = soup.find("div", {"id": "loosersList"}).find("th", {"class": "lastDate"}).text.strip()

        # finding the losers list in the table
        losers_list = soup.find("div", {"id": "loosersList"})
        # Getting all rows
        tr_list = losers_list.find_all("tr", {"class": "argaam-font dataRow"})
        # Looping on all rows to get all info.
        for i in tr_list:
            nums_of_losers.append(i.contents[1].text.strip())
            company_name.append(i.contents[3].find("a").text.strip())
            start.append(i.contents[5].text.strip())
            end.append(i.contents[7].text.strip())
            change.append(i.contents[9].text.strip())

        # unpacking all data to give every row its specific data
        file_list: list = [nums_of_losers[::2], company_name[::2], start[::2], end[::2], change[::2]]
        exported: zip_longest = zip_longest(*file_list)

        with open(r"D:\Python\web Scrapping\upWork\Argaam\Losers.csv", "w", encoding='utf-8-sig') as output_file:
            wr = csv.writer(output_file)
            wr.writerow(["الترتيب", "الشركة", f"{first_date}", f"{last_date}", "التغير"])
            wr.writerows(exported)
            print("Losers File Created.")

    losers()


if __name__ == '__main__':
    main("https://www.argaam.com/ar/monitors/market-ownership/3")

# Coded By Mahmoud Dwidar