import re
import time

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class YealinkConfigure:

    def __init__(self, ip):
        self.ip = ip
        self.url = f'http://{self.ip}/servlet?m=mod_data&p=status&q=load'
        self.options = self.configure_driver()
        self.driver = webdriver.Chrome("D:\chromedriver\chromedriver.exe")

    @staticmethod
    def configure_driver():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        return options

    def get_mac_ip(self):
        self.driver.get(self.url)
        self.login_in_site('admin')
        time.sleep(1)
        if self.wrong_password():
            self.driver.refresh()
            self.login_in_site('admin1')
        time.sleep(2)
        html = self.driver.page_source
        mac = self.extract_info('#tdMACAddress', html)
        ip_address = self.extract_info('#tdWANIP', html)
        mac = re.sub(':', '', mac)
        print(f'Мак телефон {mac}\tIP телефона {ip_address}')
        self.driver.close()

    def login_in_site(self, password):
        self.driver.find_element_by_id('idUsername').send_keys('admin')
        self.driver.find_element_by_id('idPassword').send_keys(password)
        self.driver.find_element_by_id('idConfirm').click()

    def wrong_password(self):
        error_text = 'Неверное имя пользователя или пароль!'
        en_error_text = 'Incorrect username or password!'
        html_doc = self.driver.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        error = soup.select('#notice')
        error = str(error[0])
        if error_text in error or en_error_text in error:
            return True
        return False

    @staticmethod
    def extract_info(info_type, html):
        soup = BeautifulSoup(html, 'html.parser')
        raw_info = soup.select(info_type)
        raw_info = str(raw_info[0])
        info = re.search(r'>(.+?)</label>', raw_info)
        return info.group(1)


def run(telephone_ip):
    telephone = YealinkConfigure(telephone_ip)
    try:
        telephone.get_mac_ip()
    except selenium.common.exceptions.WebDriverException:
        telephone.driver.close()
        print('Timeout Error')


if __name__ == '__main__':
    list_ip = ['172.29.0.81', '172.29.16.15']
    for ip in list_ip:
        run(ip)