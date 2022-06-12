from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import requests
import json
import time
import base64
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект
import smtplib   
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
 
Builder.load_string("""
<InitScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        canvas:
            Color:
                rgb: [193/255, 219/255, 179/255, 1]
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            source: 'car-wireless.png'
            size: [200, 200]
""")


class MainApp(App):
    def build(self):
        self.regnum = 0
        self.regreg = 0
        self.stsnum = 0
        self.reCaptchaToken = ""
        
        gsheetkey = "1gqWc2QKkUDG6i88axFP2NC_Xi3rPubsAas9KbY8Jb50"
        sheet_name = 'Лист1'
        url=f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'
        self.df = pd.read_excel(url,sheet_name=sheet_name)
        
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
 
        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_button_press)
        main_layout.add_widget(equals_button)
 
        return main_layout

 
    def on_button_press(self, instance):
        for index,row in self.df.iterrows():
            TC=row.T.T.ТС
            TC = [TC[index : index + 6] for index in range(0, len(TC), 6)]
            CTC=row.T.T.СТС
            CTC=str(CTC).replace(".0","")

            self.regnum=TC[0]
            self.regreg=TC[1]
            self.stsnum=CTC

            os.environ['MOZ_HEADLESS'] = '1'
            profile = webdriver.FirefoxProfile()

            profile.set_preference("dom.disable_open_during_load", True)
            browser = webdriver.Firefox(firefox_profile=profile)

            browser.implicitly_wait(40)
            browser.set_page_load_timeout(30)
            url = str('https://xn--90adear.xn--p1ai/check/fines#') + str(self.regnum) + str("+") + str(self.regreg) + str("+") + str(self.stsnum)
            try:
                browser.get (url)
            except:
                return -1

            while True:
                x = browser.execute_script("return appCheckFines.reCaptchaToken;")
                if x is not None:
                    browser.quit()
                    break
            self.reCaptchaToken = x
            break
        url = 'https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/fines'
        payload={'regnum':self.regnum,'regreg':self.regreg,'stsnum':self.stsnum,'reCaptchaToken':self.reCaptchaToken}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',    'Accept': 'application/json, text/javascript, */*; q=0.01',    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Origin': 'https://xn--90adear.xn--p1ai','Connection': 'keep-alive','Referer': 'https://xn--90adear.xn--p1ai/','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-site'}
        r = requests.post(url, data=payload, headers=headers)
        self.solution.text = str(r.status_code)
 
    def on_solution(self, instance):
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution
 
 
if __name__ == "__main__":
    app = MainApp()
    app.run()