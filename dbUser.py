from google.appengine.ext import db
from JsonHelper import json_helper
import logging
jhelp = json_helper()

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class USER(DictModel):
    Nombre = db.StringProperty()
    Apellido1 = db.StringProperty()
    Apellido2 = db.StringProperty()
    CI = db.StringProperty(required = True)
    Celular = db.IntegerProperty()
    Direccion = db.StringProperty()
    Usuario = db.StringProperty(required = True)
    Contrasena = db.StringProperty(required = True)
    TipoUsuario = db.IntegerProperty(required = True)
    FechaCreacion = db.DateTimeProperty(auto_now_add = True)
    
    @classmethod
    def by_id_check(cls, CI):
        res = USER.all().filter('CI =', CI).get()
        return res
        
    @classmethod
    def register(cls, Usuario, CI, Contrasena, TipoUsuario, Nombre=None, Apellido1=None, Apellido2=None, Celular=None, Direccion=None):
        return USER(parent = users_key(),
                    Usuario = Usuario,
                    CI = CI,
                    Contrasena = Contrasena,
                    TipoUsuario = TipoUsuario,
                    Nombre = Nombre,
                    Apellido1 = Apellido1,
                    Apellido2 = Apellido2,
                    Celular = Celular,
                    Direccion = Direccion)
    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM USER ORDER BY fecha_creacion DESC")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def get_allEncargados(cls):
        res = db.GqlQuery("SELECT * FROM USER WHERE TipoUsuario=3 ORDER BY Apellido1")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def get_allChefs(cls):
        res = db.GqlQuery("SELECT * FROM USER WHERE TipoUsuario=2 ORDER BY Apellido1")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def by_username(cls, Usuario):
        u = USER.all().filter('Usuario =', Usuario).get()
        return u

    @classmethod
    def login(cls, Usuario, contrasenha):
        u = cls.by_username(Usuario)
        if u:
            # if enc.valid_pw(nombre_uva, pw, u.pw_hash):
                # return u
            if contrasenha == u.Contrasena:
                return u

