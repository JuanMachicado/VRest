from google.appengine.ext import db
from JsonHelper import json_helper
import logging
jhelp = json_helper()

def stocks_key(group = 'default'):
    return db.Key.from_path('stocks', group)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class STOCK(DictModel):
    nombre = db.StringProperty(required = True)
    cantidad = db.StringProperty(required = True)
    FechaCreacion = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def register(cls, nombre, cantidad):
        return STOCK(parent = stocks_key(),
                    nombre = nombre,
                    cantidad = cantidad)

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM STOCK ORDER BY FechaCreacion")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def by_id_nombre(cls, nombre):
        u = STOCK.all().filter('nombre =', nombre).get()
        return u