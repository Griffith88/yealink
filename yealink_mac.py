import re
import time

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from models import Directory, Autoprovision, data_base, autoprovision, MacAddress
from settings import error_list, auto_provision_server


class YealinkConfigure:

    def __init__(self, ip):
        self.ip = ip
        self.url = f'http://{self.ip}/servlet?m=mod_data&p=status&q=load'
        self.options = self.configure_driver()
        self.driver = webdriver.Chrome("D:\chromedriver\chromedriver.exe", options=self.configure_driver())
        self.driver.set_page_load_timeout(15)
        self.provision_url = f'http://{self.ip}/servlet?m=mod_data&p=settings-autop&q=load'

    @staticmethod
    def configure_driver():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        return options

    def set_auto_provision(self):
        self.open_page(self.provision_url)
        html_code = self.driver.page_source
        if auto_provision_server not in html_code:
            self.driver.find_element_by_name("AutoProvisionServerURL").send_keys(auto_provision_server)
            try:
                self.driver.find_element_by_id('btn_confirm1').click()
            except selenium.common.exceptions.NoSuchElementException:
                self.driver.find_element_by_name('btnSubmit').click()
        time.sleep(5)
        query = Autoprovision.select().where(Autoprovision.telephone_ip == self.ip)
        if not query.exists():
            Autoprovision.insert({
                'telephone_ip': self.ip,
                'provision_status': True
            }).execute()
        Autoprovision.update(telephone_ip=self.ip, provision_status=True)

    def get_mac_ip(self):
        self.open_page(self.url)
        html = self.driver.page_source
        mac = self.extract_info('#tdMACAddress', html)
        mac = re.sub(':', '', mac)
        query = MacAddress.select().where(MacAddress.telephone_ip == self.ip)
        if not query.exists():
            MacAddress.create(telephone_ip=self.ip, mac_address=mac)
        MacAddress.update(telephone_ip=self.ip, mac_address=mac)
        self.driver.quit()

    def open_page(self, page):
        self.driver.get(page)
        self.login_in_site('admin')
        time.sleep(2)
        if self.wrong_password():
            self.driver.refresh()
            self.login_in_site('admin1')
        time.sleep(5)

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


def get_mac(ip):
    yealink_telephone = YealinkConfigure(ip)
    print(f'начинаю проверку мака у телефона {ip}')
    try:
        yealink_telephone.get_mac_ip()
    except selenium.common.exceptions.WebDriverException:
        yealink_telephone.driver.quit()
        print(f'телефон {ip} не включен')


def get_all_mac_by_model(model='Yealink T21P E2'):
    '''
    Getting all mac by telephone model
    :param model: can be Yealink T21P E2
    :return:
    '''
    for ip in Directory.select().where(Directory.telephone_model == model):
        query = MacAddress.select().where(MacAddress.telephone_ip == ip.telephone_ip)
        if not query.exists():
            get_mac(ip.telephone_ip)


def get_one_mac(ip):
    get_mac(ip)


def auto_provision(ip):
    yealink = YealinkConfigure(ip)
    yealink.set_auto_provision()


if __name__ == '__main__':
    autoprovision.create_tables([Autoprovision])
    data_base.create_tables([Directory, MacAddress])
    get_all_mac_by_model()
