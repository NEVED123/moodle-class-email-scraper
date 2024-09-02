import json
import urllib.parse
import requests as req
from bs4 import BeautifulSoup as bs
import urllib
from tqdm import tqdm

def get_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    return config["courseId"], parse_cookie_string(config['cookie'])

def parse_cookie_string(cookie_string):
    cookies = cookie_string.split('; ')
    cookie_dict = {}

    for cookie in cookies:
        key, value = cookie.split('=', 1)
        cookie_dict[key] = urllib.parse.unquote(value)
    
    return cookie_dict

def get_student_page_urls(courseId, cookies):
    student_list_url = f"https://moodle.oakland.edu/user/index.php?page=0&perpage=5000&contextid=0&id={courseId}" # params avoids pagination issues
    response = req.get(student_list_url, cookies=cookies)
    soup = bs(response.text, 'html.parser')
    user_hrefs = soup.find_all('a', href=match_user_href)
    return [anchor['href'] for anchor in user_hrefs]

def match_user_href(href):
    return href and href.startswith('https://moodle.oakland.edu/user/view')

def get_student_email(student_url, cookies):
    response = req.get(student_url, cookies=cookies)
    soup = bs(response.text, 'html.parser')

    if soup.find('a', string='Teacher') is not None:
        return None
    
    mailto_href = soup.find('a', href=match_email_href)['href']
    return urllib.parse.unquote(mailto_href).split(':')[1]

def match_email_href(href):
    return href and urllib.parse.unquote(href).startswith('mailto:')

def main():
    print("Processing config information...")
    courseId, cookies = get_config()
    print("Getting list of student ids...")
    student_urls = get_student_page_urls(courseId, cookies)
    emails = []
    for student_url in tqdm(student_urls, desc='Getting student emails...'):
        email = get_student_email(student_url, cookies)
        if email is not None:
            emails.append(get_student_email(student_url, cookies))
    with open('emails.txt', 'w') as f:
        f.write('\n'.join(emails))

if __name__ == '__main__':
    main()
