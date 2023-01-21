# importing the modules
import requests
from bs4 import BeautifulSoup
import csv

# Website want to scrape ==> https://www.yallakora.com/?nav-logo

# Inserting a specific date form the user
date = input("Please enter a date in the following format MM/DD/YYYY: ")
page = requests.get(f"https://www.yallakora.com/Match-Center/?date={date}")


def main(page):
    """
    Getting the website page that contains all matches and make it readable
    """
    src = page.content
    soup = BeautifulSoup(src, "lxml")

    # Saving the all data i get in a variable
    matches_details = []

    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(championships):
        """
        Obtain the available matches information on the insert date with all the required details.
        """
        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all("li")
        number_of_matches = len(all_matches)

        # Get match info
        for match in range(number_of_matches):
            # Get Teams Names
            team_a = all_matches[match].find("div", {"class": "teamA"}).text.strip()
            team_b = all_matches[match].find("div", {"class", "teamB"}).text.strip()

            # Get The Score
            match_result = all_matches[match].find("div", {"class", "MResult"}).find_all("span", {"class": "score"})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # Get Match Time
            match_time = all_matches[match].find("div", {"class", "MResult"}).find("span",
                                                                                   {"class", "time"}).text.strip()

            # Add matches info in matches_details
            matches_details.append({"نوع البطولة": championship_title, "الفريق الأول": team_a, "الفريق الثانى": team_b,
                                    "وقت المباراة": match_time, "النتيجة": score})

    # looping on the number of championships to get every match in every champion.
    for i in range(len(championships)):
        get_match_info(championships[i])

    # Write results in a csv file
    keys = matches_details[0].keys()

    with open(r"FilePath\Matches Details.csv", "w", encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("File Created.")


main(page)

# Coded By Mahmoud Dwidar
# GitHub ==> https://github.com/mahmouddwidar