import re
import time

import peewee
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from peewee import Model
from settings import data_base, error_list


class YealinkConfigure:

    def __init__(self, ip):
        self.ip = ip
        self.url = f'http://{self.ip}/servlet?m=mod_data&p=status&q=load'
        self.options = self.configure_driver()
        self.driver = webdriver.Chrome("D:\chromedriver\chromedriver.exe", options=self.configure_driver())
        self.driver.set_page_load_timeout(15)

    @staticmethod
    def configure_driver():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        return options

    def get_mac_ip(self):
        self.driver.get(self.url)
        self.login_in_site('admin')
        time.sleep(2)
        if self.wrong_password():
            self.driver.refresh()
            self.login_in_site('admin1')
        time.sleep(5)
        html = self.driver.page_source
        mac = self.extract_info('#tdMACAddress', html)
        ip_address = self.extract_info('#tdWANIP', html)
        mac = re.sub(':', '', mac)
        print(f'Мак телефон {mac}\tIP телефона {ip_address}')
        self.driver.quit()

    def login_in_site(self, password):
        try:
            self.driver.find_element_by_id('idUsername').send_keys('admin')
        except selenium.common.exceptions.NoSuchElementException:
            self.driver.find_element_by_name('username').send_keys('admin')
        try:
            self.driver.find_element_by_id('idPassword').send_keys(password)
        except selenium.common.exceptions.NoSuchElementException:
            self.driver.find_element_by_name('pwd').send_keys(password)

        self.driver.find_element_by_id('idConfirm').click()

    def wrong_password(self):
        html_doc = self.driver.page_source
        for error in error_list:
            if error in html_doc:
                return True
        return False

    @staticmethod
    def extract_info(info_type, html):
        soup = BeautifulSoup(html, 'html.parser')
        raw_info = soup.select(info_type)
        try:
            raw_info = str(raw_info[0])
        except IndexError:
            print('ЧТО ТО НЕ ТАК С ТЕЛЕФОНОМ!!!')
            raw_info = '>ERROR</'
        info = re.search(r'>(.+?)</', raw_info)
        return info.group(1)


def run(telephone_ip):
    telephone = YealinkConfigure(telephone_ip)
    try:
        telephone.get_mac_ip()
    except selenium.common.exceptions.WebDriverException:
        telephone.driver.close()
        print('Timeout Error')


class BaseModel(Model):
    class Meta:
        database = data_base


class Directory(BaseModel):
    domain_id = peewee.IntegerField()
    cache = peewee.IntegerField()
    username = peewee.CharField(max_length=255)
    line = peewee.CharField(max_length=255)
    telephone_model = peewee.CharField(max_length=255)
    telephone_ip = peewee.CharField(max_length=50)
    computer_ip = peewee.CharField(max_length=50)
    computer_mac = peewee.CharField(max_length=255)
    other_telephone_number = peewee.TextField()
    vlan = peewee.TextField()
    desc = peewee.TextField()
    ad_display_name = peewee.CharField(max_length=255)
    ad_extension_attribute = peewee.CharField(max_length=255)
    ad_department = peewee.CharField(max_length=255)
    ad_ip_phone = peewee.CharField(max_length=255)
    ad_title = peewee.CharField(max_length=255)
    samaccountname = peewee.CharField(max_length=255)
    network_device = peewee.CharField(max_length=255)


def get_mac(ip):
    yealink_telephone = YealinkConfigure(ip)
    print(f'начинаю проверку мака у телефона {ip}')
    try:
        yealink_telephone.get_mac_ip()
    except selenium.common.exceptions.WebDriverException:
        yealink_telephone.driver.quit()
        print(f'телефон {ip} не включен')


def get_all_mac_by_model(model):
    for ip in Directory.select().where(Directory.telephone_model == model):
        get_mac(ip)


def get_one_mac(ip):
    get_mac(ip)


if __name__ == '__main__':
    get_one_mac('172.29.0.81')
