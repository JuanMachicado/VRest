from google.appengine.ext import db
from JsonHelper import json_helper
import logging
jhelp = json_helper()

def tipos_usuario_key(group = 'default'):
    return db.Key.from_path('tipos_usuario', group)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class TIPO_USUARIO(DictModel):
    id_tipoUsuario = db.IntegerProperty(required = True)
    t_usuario = db.StringProperty(required = True)
        
    @classmethod
    def register(cls, id_tipoUsuario, t_usuario):
        return TIPO_USUARIO(parent = tipos_usuario_key(),
                    id_tipoUsuario = id_tipoUsuario,
                    t_usuario = t_usuario)
    @classmethod
    def by_id_tipoUsuario(cls, id_tipoUsuario):
        u = TIPO_USUARIO.all().filter('id_tipoUsuario =', id_tipoUsuario).get()
        return u

