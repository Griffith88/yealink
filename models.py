import peewee
from peewee import Model
from settings import data_base


class BaseModel1(Model):
    class Meta:
        database = data_base


class Directory(BaseModel1):
    line = peewee.CharField(max_length=255)
    telephone_model = peewee.CharField(max_length=255)
    telephone_ip = peewee.CharField(max_length=50)
    vlan = peewee.TextField()
    telephone_mac = peewee.CharField(max_length=255)

