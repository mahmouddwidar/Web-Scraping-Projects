# Importing the modules
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import csv

# Saving The Data
company_name: list = []
links: list = []
contact_email: list = []
long_introduction: list = []
all_tags: list = []

# Get the page and make it BeautifulSoup
page_num = 1

while True:
    page = requests.get(f"https://www.horecava.nl/leveranciers/page/{page_num}/")
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    # page limit is 339 pages
    page_limit = 339

    if page_num > page_limit:
        print("Pages ended, wait for file creation...")
        break

    # Get the Whole tags for company names and their page links
    company_names = soup.find_all("div", {"class": "articleblock__content__text__title header-medium"})

    for i in range(len(company_names)):
        # Get Company name
        company_name.append(company_names[i].text.strip())

        # Get Company page
        links.append(company_names[i].find("a").attrs['href'])
    page_num += 1
    print(f"Page Switched [{page_num}].")

# GEt the info from the inner page
for link in links:
    page = requests.get(link)
    src = page.content
    soup = BeautifulSoup(src, "lxml")

    # Get Contact info.
    contact_emails = soup.find("p", {"class": "contact-container"})
    contact_email.append(contact_emails.text.strip())

    # Get Long introduction
    long_introductions = soup.find("div", {"class": "content-container"})
    long_introduction.append(long_introductions.text.strip())

    # Get Tags
    tags = soup.find_all("a", {"class": "button button--darkgray"})
    tag = ""
    for i in tags:
        tag += i.text.strip() + "| "
    tag = tag[:-2]
    all_tags.append(tag)

file_list = [company_name, links, contact_email, long_introduction, all_tags]
exported: zip_longest = zip_longest(*file_list)

with open(r"FilePath\Data.csv", "w") as output_file:
    wr = csv.writer(output_file)
    wr.writerow(["Company Name", "Links", "Contact Info.", "Long Introduction", "Tags"])
    wr.writerows(exported)
    print("File Created.")

# Coded By Mahmoud Dwidar
# Github ==> https://github.com/mahmouddwidar