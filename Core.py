import requests
from bs4 import BeautifulSoup as bs
import re


def get_my_deadlines(email, password):
    url = 'https://bux.bracu.ac.bd/login/'

    s = requests.session()
    csrf = s.get(url).cookies['csrftoken']

    cookies = {
        '_ga': 'GA1.3.1720954072.1625223504',
        'openedx-language-preference': 'en',
        'hide_captions': 'true',
        'video_player_volume_level': '0',
        '_gid': 'GA1.3.56544039.1632555132',
        'experiments_is_enterprise': 'false',
        'csrftoken': csrf,
        '_gat_edunext': '1',
        '_gat': '1',
        'sessionid': s.cookies['sessionid'],
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^94^\\^, ^\\^Microsoft',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': s.cookies['csrftoken'],
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'Origin': 'https://bux.bracu.ac.bd',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://bux.bracu.ac.bd/login?next=^%^2F',
        'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
    }

    data = {
        'email': email,
        'password': password
    }

    s.post('https://bux.bracu.ac.bd/user_api/v1/account/login_session/',
           headers=headers, cookies=cookies, data=data)
    dashboard = s.get("https://bux.bracu.ac.bd/dashboard")
    soup = bs(dashboard.text, 'html.parser')

    semester = '2021_Summer'

    listofLinks = []
    for item in soup.find_all('a', class_='course-target-link'):
        if semester in item['href'] and item['href'] not in listofLinks:
            listofLinks.append(item['href'])

    r = re.compile(".*/course/")
    listofCourseLinks = list(filter(r.match, listofLinks))

    theUltimateList = {}

    for item in listofCourseLinks:
        course_page = bs(
            s.get("https://bux.bracu.ac.bd"+item).text, 'html.parser')
        datesList = []
        for dates in course_page.find_all('span', class_='localized-datetime subtitle-name'):
            if dates["data-datetime"] != '':
                datesList.append(dates.parent.parent.parent.find(
                    'h4').text.split('\n')[1].strip()+' due on '+dates["data-datetime"])

        item = re.sub(r'/courses/course-v1:buX\+', '', item)
        item = re.sub(r'\+2021_Summer/course/', '', item)
        theUltimateList[item] = datesList

    for x in theUltimateList:
        if len(theUltimateList[x]) != 0:
            print(x+':')
            for y in theUltimateList[x]:
                print(y)
            print()


if __name__ == "__main__":
    get_my_deadlines('aditya.roy@g.bracu.ac.bd', 'aditya19101414')
