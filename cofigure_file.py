import os
from models import Directory


class Phone:
    models = {
        'T21PE2_CONFIG': os.path.normpath('configs\\base_t21pe2_config.cfg'),
        'T58_CONFIG': os.path.normpath('configs\\base_t58_config.cfg'),
        'T49G_CONFIG': os.path.normpath('configs\\base_t49g_config.cfg'),
        'T46G_CONFIG': os.path.normpath('configs\\base_t46g_config.cfg'),
        'T31G_CONFIG': os.path.normpath('configs\\base_t31g_config.cfg')
    }

    def __init__(self, mac, user_agent):
        self.mac = mac.upper()
        self.user_agent = user_agent.split()
        self.line = None
        self.model = None
        self.get_model()

    def get_number(self):
        query = Directory.select().where(Directory.telephone_mac == self.mac)
        if query.exists():
            result = query.get()
            print(result.line)
            return result.line
        else:
            raise ValueError(f'{self.mac} --- такого мак адреса нету в системе')

    def get_model(self):
        print(self.user_agent)
        if 'SIP-T58' in self.user_agent:
            self.model = self.models['T58_CONFIG']
        elif 'SIP-T21P_E2' in self.user_agent:
            self.model = self.models['T21PE2_CONFIG']
        elif 'VP-T49G' in self.user_agent:
            self.model = self.models['T49G_CONFIG']
        elif 'SIP-T46G' in self.user_agent:
            self.model = self.models['T46G_CONFIG']
        elif 'SIP-T31G' in self.user_agent:
            self.model = self.models['T31G_CONFIG']
        else:
            raise ValueError(f'для {self.user_agent} нету конфигурации')

    def get_configuration_file_name(self):
        self.line = self.get_number()
        file_name = os.path.normpath('configs\\' + f'{self.mac}.cfg')
        with open(file_name, 'w', encoding='utf8') as mac_file:
            with open(self.model, 'r', encoding='utf8') as base_file:
                for row in base_file:
                    if row.startswith('account.1.auth_name ='):
                        mac_file.write(f'account.1.auth_name = {self.line}\n')
                    elif row.startswith('account.1.label ='):
                        mac_file.write(f'account.1.label = {self.line}\n')
                    elif row.startswith('account.1.user_name ='):
                        mac_file.write(f'account.1.user_name = {self.line}\n')
                    elif row.startswith('account.1.display_name ='):
                        mac_file.write(f'account.1.display_name = {self.line}\n')
                    else:
                        mac_file.write(row)
        return file_name


if __name__ == '__main__':
    exit()
