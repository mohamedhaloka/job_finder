import csv
import os

import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import inquirer


def get_url_depend_on_name(name):
    if name == 'Wuzzuf':
        return 'https://wuzzuf.net'
    else:
        return 'https://forasna.com'


def get_search_url_depend_on_name(name):
    if name == 'Wuzzuf':
        return 'https://wuzzuf.net/search/jobs/?q=' + searchKy.replace(' ', '+') + '&a=hpb' + '&start=' + str(
            current_page)
    else:
        return 'https://forasna.com/وظائف-خالية?query=' + searchKy.replace(' ', '%20')


def get_tag(name):
    if name == 'Wuzzuf':
        return ['h2', 'a', 'span', 'span']
    else:
        return ['h2', 'span', 'span', 'div']


def get_identifier(name):
    if name == 'Wuzzuf':
        return [{'class': 'css-m604qf'}, {'class': 'css-17s97q8'}, {'class': 'css-5wys0k'}, {'class': 'css-1ve4b75'}]
    else:
        return [{'class': 'job-title'}, {'class': 'company-name'}, {'class': 'location location-desktop'},
                {'clas': 'job-details'}]


questions = [
    inquirer.List('engine',
                  message="What Website you want to search in?",
                  choices=['Wuzzuf', 'Forsna'],
                  ),
]
answers = inquirer.prompt(questions)

website_name = answers.get('engine')
print(website_name)
website_url = get_url_depend_on_name(website_name)
# website_search_url = get_search_url_depend_on_name(website_name)

current_page = 0

while True:

    # show input field in first of app to allow user to type what is search in
    if current_page == 0:
        searchKy = input("What is job do you search in? ")

    # send request to get the web page content
    request = requests.get(get_search_url_depend_on_name(website_name))

    # save page content in variable to use it later
    src = request.content

    # use beautiful soup package to convert web page content to 'lxml' format to use it easily
    soup = BeautifulSoup(src, "lxml")

    # depend on html we get the all details about all jobs depend on tags in html page and with unique identifier
    job_titles = soup.find_all(get_tag(website_name)[0], get_identifier(website_name)[0])
    companies_name = soup.find_all(get_tag(website_name)[1], get_identifier(website_name)[1])
    location_companies = soup.find_all(get_tag(website_name)[2], get_identifier(website_name)[2])
    job_type = soup.find_all(get_tag(website_name)[3], get_identifier(website_name)[3])

    # extract all needed information from details
    titles = []
    com_names = []
    com_locations = []
    types = []
    links = []

    for i in range(len(job_titles)):
        titles.append(job_titles[i].text)
        if website_name == 'Wuzzuf':
            links.append(website_url + job_titles[i].find_next('a').attrs['href'])
        else:
            links.append(job_titles[i].find_next('a').attrs['href'])
        com_names.append(companies_name[i].text)
        com_locations.append(location_companies[i].text)
        if website_name == 'Wuzzuf':
            types.append(job_type[i].text)

    # create csv file and put all jobs requirements into it
    file_list = [titles, com_names, com_locations, types, links]
    extracted = zip_longest(*file_list)

    file_is_found = os.path.isfile('/Users/mohamednasr/Downloads/jobs.csv')

    if file_is_found:
        with open("/Users/mohamednasr/Downloads/jobs.csv", 'a+') as file:
            csv.writer(file).writerows(extracted)
    else:
        with open("/Users/mohamednasr/Downloads/jobs.csv", 'w') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['Job Titles', 'Company Names', 'Locations Company', 'Job Type', 'Job Links'])
            csv_file.writerows(extracted)

    print('get data from page number ' + str(current_page + 1))

    if website_name == 'Wuzzuf':
        print('you need more data from next page?')
        nextPage = input("Do You need more?[Y/N]: ")

        if nextPage.lower() == 'n':
            break
        else:
            current_page += 1
    else:
        break
