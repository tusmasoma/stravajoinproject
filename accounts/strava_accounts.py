
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin
from time import sleep

def login_strava_by_requests(email,password):
    """
    stravaにログインする
    """

    login_url="https://www.strava.com/login"

    session=requests.Session()
    response=session.get(login_url)

    soup=BeautifulSoup(response.text,'html.parser')

    utf8=soup.select('input[name="utf8"]')[0].get('value')
    authenticity=soup.select('input[name="authenticity_token"]')[0].get('value')

    json_data={
        "email":email,
        "password":password,
        "utf8":utf8,
        "authenticity_token":authenticity,
        "plan":"",
        }

    action_url=urljoin("https://www.strava.com/login","/session")

    session.post(action_url,data=json_data)

    response=session.get('https://www.strava.com/dashboard')

    if response.url == 'https://www.strava.com/dashboard':
        return (session,True)
    else:
        return (session,None)
