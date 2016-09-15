from google.appengine.ext import db
from JsonHelper import json_helper
import logging
jhelp = json_helper()

def chef_encargado_key(group = 'default'):
    return db.Key.from_path('chef_encargado', group)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class CHEF_ENCARGADO(DictModel):
    chef_usuario = db.StringProperty(required = True)
    encargado_usuario = db.StringProperty()
    empresa = db.StringProperty()
        
    @classmethod
    def register(cls, chef_usuario, encargado_usuario, empresa):
        u = CHEF_ENCARGADO.all().filter('chef_usuario =', chef_usuario).get()
        if u:
            u.encargado_usuario = encargado_usuario
            u.empresa = empresa
            return u
        return CHEF_ENCARGADO(parent = chef_encargado_key(),
                    chef_usuario = chef_usuario,
                    encargado_usuario = encargado_usuario,
                    empresa = empresa)

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM CHEF_ENCARGADO")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

