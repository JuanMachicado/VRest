from google.appengine.ext import db
from JsonHelper import json_helper
import logging
jhelp = json_helper()

def compras_realizadas_key(group = 'default'):
    return db.Key.from_path('compras', group)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class COMPRA_REALIZADA(DictModel):
    fecha = db.StringProperty(required = True)
    nombre = db.StringProperty(required = True)
    cantidad = db.StringProperty(required = True)
    comprado = db.StringProperty(required = True)
    unidad = db.StringProperty(required = True)
    user = db.StringProperty(required = True)
    FechaCreacion = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def register(cls, fecha, nombre, cantidad, unidad, user, comprado):
        return COMPRA_REALIZADA(parent = compras_realizadas_key(),
                    fecha = fecha,
                    nombre = nombre,
                    cantidad = cantidad,
                    unidad = unidad,
                    user = user,
                    comprado = comprado)

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM COMPRA_REALIZADA ORDER BY FechaCreacion DESC LIMIT 100")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response
