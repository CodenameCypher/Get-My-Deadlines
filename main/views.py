from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
import re
import datetime


def get_my_deadlines(email, password, semester):
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
            pattern2 = r'\+'+semester+'/course/'
            item = re.sub(r'/courses/course-v1:buX\+', '', item)
            item = re.sub(pattern2, '', item)
            if dates["data-datetime"] != '':
                string = dates["data-datetime"]
                nameText = dates.parent.parent.parent.find(
                    'h4').text.split('\n')[1].strip()
                hours = datetime.timedelta(hours=6)
                my_time = datetime.datetime.strptime(
                    string, '%Y-%m-%d  %H:%M:00+00:00') + hours
                date = str((my_time-hours).date()).replace('-', '')
                time = str((my_time-hours).time()).replace(':', '')
                text = (nameText+' - '+item).replace(' ', '+')
                gCalLink = 'https://calendar.google.com/calendar/render?action=TEMPLATE&text='+text+'&dates=' + \
                    date + 'T'+time + 'Z%2F'+date + 'T'+time+'Z'
                # new_time = (my_time+hours).strftime("%A %d %B, %I:%M%p")
                datesList.append((nameText, my_time, gCalLink))

        if len(datesList) != 0:
            theUltimateList[item] = datesList

    # for x in theUltimateList:
    #     if len(theUltimateList[x]) != 0:
    #         print(x+':')
    #         for y in theUltimateList[x]:
    #             print(y)
    #         print()
    return theUltimateList


def homepage(request):
    if request.method == 'POST':
        buX_email = request.POST.get('email')
        buX_password = request.POST.get('password')
        semester = request.POST.get('semester')
        dateDictionary = get_my_deadlines(buX_email, buX_password, semester)
        return render(request, 'results.html', context={'list': dateDictionary, 'currentTime': datetime.datetime.now()})
    return render(request, 'index.html')


def get_deadlines(request):
    if request.method == 'POST':
        print(request.POST.get('email'))
        return render(request, 'results.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'faq.html')
