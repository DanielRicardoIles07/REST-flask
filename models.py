from peewee import *

DATABASE = MySQLDatabase('mu_domicilios', host = 'domiciliosurbanos.com', user = 'joseluis', passwd = '597b9050653f3')


class Empresa(Model):
    class Meta:
        database = DATABASE
        db_table = 'empresa'
    nombre = CharField(unique = True, max_length = 250)
    direccion = TextField()
    mu_ref = TextField()

    def to_json(self):
        return {'id': self.id, 'nombre': self.nombre, 'direccion': self.direccion, 'mu_ref': self.mu_ref} 