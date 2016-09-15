from google.appengine.ext import db
from JsonHelper import json_helper
import logging
jhelp = json_helper()

def productos_key(group = 'default'):
    return db.Key.from_path('productos', group)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class PRODUCTO(DictModel):
    nombre = db.StringProperty(required = True)
    ingredientes = db.StringProperty(required = True)
    precio = db.IntegerProperty(required = True)
    tipo = db.StringProperty(required = True)
    FechaCreacion = db.DateTimeProperty(auto_now_add = True)
        
    @classmethod
    def register(cls, nombre, ingredientes, precio, tipo):
        return PRODUCTO(parent = productos_key(),
                    nombre = nombre,
                    ingredientes = ingredientes,
                    precio = precio,
                    tipo = tipo)
    @classmethod
    def by_id_nombre(cls, nombre):
        u = PRODUCTO.all().filter('nombre =', nombre).get()
        return u

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM PRODUCTO")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def all_by_tipo(cls, parameter):
        res = PRODUCTO.all().filter('tipo =', parameter)
        response = []
        for r in res:
            response.append(r.to_dict())
        return response
