information = 'Yealink SIP-T21P_E2 52.81.0.90 80:5e:c0:ae:9a:b6'
import re
from models import Directory, MacAddress


def get_info_from_user_agent(info):
    _, model, firmware, mac_raw = info.split()
    mac_address = re.sub(':', '', mac_raw)
    mac_address = mac_address.upper()
    return mac_address


def get_ip_from_db(mac):
    result = MacAddress.select().where(MacAddress.mac_address == mac).get()
    return result.telephone_ip


def get_number(ip):
    result = Directory.select().where(Directory.telephone_ip == ip).get()
    return result.line


def get_configuration_file_name(info):
    mac_address = get_info_from_user_agent(info)
    ip = get_ip_from_db(mac_address)
    line = get_number(ip)
    file_name = f'{mac_address}.cfg'
    with open(file_name, 'w', encoding='utf8') as mac_file:
        with open('base_model_config.cfg', 'r', encoding='utf8') as base_file:
            for row in base_file:
                if row.startswith('account.1.auth_name ='):
                    mac_file.write(f'account.1.auth_name = {line}\n')
                elif row.startswith('account.1.label ='):
                    mac_file.write(f'account.1.label = {line}\n')
                elif row.startswith('account.1.user_name ='):
                    mac_file.write(f'account.1.user_name = {line}\n')
                elif row.startswith('account.1.display_name ='):
                    mac_file.write(f'account.1.display_name = {line}\n')
                else:
                    mac_file.write(row)
    return file_name


if __name__ == '__main__':
    get_configuration_file_name(information)
