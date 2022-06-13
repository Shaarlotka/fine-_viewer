from car_model import Car
from data_model import Conf
import os
from selenium import webdriver
import requests
import json

class Result:
    def __init__(self, data):
        self.data = data
        self.text = self.list_analysis()

    def list_analysis(self):
        text = ''
        for car in self.data.car_list:
            fine = Fines(car)
            text = text + fine.fines + '\n'
        if text == '':
            text = 'Штрафов не найдено'
        return text


class Fines:
    def __init__(self, car):
        self.car = car
        self.reCaptchaToken = ''
        self.fines = self.parse_req()
        

    def get_reCaptchaToken(self):
        os.environ['MOZ_HEADLESS'] = '1'
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.disable_open_during_load", True)
        browser = webdriver.Firefox(firefox_profile=profile)
        browser.implicitly_wait(40)
        browser.set_page_load_timeout(30)

        url = str('https://xn--90adear.xn--p1ai/check/fines#') + str(self.car.regnum) \
              + str("+") + str(self.car.regreg) + str("+") + str(self.car.stsnum)
        try:
            browser.get (url)
        except:
            return -1

        while True:
            tocken = browser.execute_script("return appCheckFines.reCaptchaToken;")
            if tocken is not None:
                browser.quit()
                break
        return tocken

    def get_response(self):
        url = 'https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/fines'
        payload={'regnum':self.car.regnum,'regreg':self.car.regreg,
                 'stsnum':self.car.stsnum,'reCaptchaToken':self.reCaptchaToken}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Origin': 'https://xn--90adear.xn--p1ai',
                   'Connection': 'keep-alive',
                   'Referer': 'https://xn--90adear.xn--p1ai/',
                   'Sec-Fetch-Dest': 'empty',
                   'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Site': 'same-site'}
        try:
            req = requests.post(url, data=payload, headers=headers)
        except:
            return -1
        return req

    def parse_req(self):
        req = ''
        while True:
            self.reCaptchaToken = self.get_reCaptchaToken()
            req = self.get_response()
            if req.status_code == 200:
                break

        result = json.loads(req.text)
        text = ''
        if len(result['data']) > 0:
            Total_Fine = 0
            for inf in result['data']:
                Total_Fine = Total_Fine + int(inf['Summa'])
            text = "Авто " + self.car.regnum + self.car.regreg + ' ' +\
                str(len(result['data'])) + ' штрафа на на сумму ' + Total_Fine + 'руб.'
        return text