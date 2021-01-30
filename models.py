import peewee
from peewee import Model
from settings import data_base, autoprovision


class BaseModel1(Model):
    class Meta:
        database = data_base


class Directory(BaseModel1):
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


class MacAddress(BaseModel1):
    telephone_ip = peewee.CharField(max_length=16)
    mac_address = peewee.CharField(max_length=12)


class BaseModel2(Model):
    class Meta:
        database = autoprovision


class Autoprovision(BaseModel2):
    telephone_ip = peewee.CharField(max_length=16)
    provision_status = peewee.BooleanField()
