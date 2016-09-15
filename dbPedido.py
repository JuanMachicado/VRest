from google.appengine.ext import db
from JsonHelper import json_helper
import logging
jhelp = json_helper()

def pedidos_key(group = 'default'):
    return db.Key.from_path('pedidos', group)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class PEDIDO(DictModel):
    fecha = db.StringProperty(required = True)
    nombre = db.StringProperty(required = True)
    cantidad = db.IntegerProperty(required = True)
    usuario = db.StringProperty(required = True)
    estado = db.StringProperty(required = True)
    estadoDeChef = db.StringProperty(required = True)
    FechaCreacion = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def register(cls, fecha, nombre, cantidad, estado, usuario):
        return PEDIDO(parent = pedidos_key(),
                    fecha = fecha,
                    nombre = nombre,
                    cantidad = cantidad,
                    estadoDeChef = "No entregado",
                    estado = estado,
                    usuario = usuario)

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM PEDIDO")
        response = []
        for r in res:
            dic = r.to_dict()
            dic["id"] = r.key().id()
            response.append(dic)
        return response

    @classmethod
    def by_id(cls, id):
        u = PEDIDO.get_by_id(id, pedidos_key())
        return u

