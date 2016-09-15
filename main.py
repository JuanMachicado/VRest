import webapp2
import logging
import urllib2
import re
from JsonHelper import json_helper
from BaseHandler import BaseHandler
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.api import files
from google.appengine.api import memcache
from dbUser import USER
from dbTipoUsuario import TIPO_USUARIO
from dbChefEncargado import CHEF_ENCARGADO
from dbProducto import PRODUCTO
from dbPedido import PEDIDO
from dbCompraRealizada import COMPRA_REALIZADA
from dbStock import STOCK
jhelp = json_helper()

class MainHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    def get(self):
        self.callback = self.request.get('callback')
        result = {}
        result['success'] = 'true'
        result['message'] = 'Datos obtenidos correctamente'
        a = dict()
        a['app'] = 'valencia'
        a['version'] = 'v1.0'
        result['appData'] = []
        result['appData'].append(a);
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class LogInHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    # Params:
    # Usuario, CI, Contrasena, TipoUsuario, Nombre, Apellido1, Apellido2, Celular, Direccion
    def post(self):
        result = {}
        result['success'] = 'true'
        result['message'] = 'Usuario y Contrasena correctos'
        Usuario = self.request.get('Usuario')
        Contrasena = self.request.get('Contrasena')
        user = USER.login(Usuario, Contrasena)
        if not user:
            result['success'] = 'false'
            result['message'] = 'Sus datos son incorrectos'
        if self.callback:
            if user:
                result['data'] = {}
                result['data']['Nombre'] = user.Nombre
                result['data']['Apellido1'] = user.Apellido1
                tipo = TIPO_USUARIO.by_id_tipoUsuario(user.TipoUsuario)
                if tipo:
                    result['data']['TipoUsuario'] = tipo.t_usuario
                else:
                    result['success'] = 'false'
                    result['message'] = 'Ocurrio un error con el tipo de usuario, debe contactar al administrador'
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            if user:
                result['data'] = {}
                result['data']['Nombre'] = user.Nombre
                result['data']['Apellido1'] = user.Apellido1
                result['data']['TipoUsuario'] = user.TipoUsuario
                tipo = TIPO_USUARIO.by_id_tipoUsuario(user.TipoUsuario)
                if tipo:
                    result['data']['TipoUsuario'] = tipo.t_usuario
                else:
                    result['success'] = 'false'
                    result['message'] = 'Ocurrio un error con el tipo de usuario, debe contactar al administrador'
            self.response.write(jhelp.getAsJSONObject(result))

class TipoUsuarioHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    # Params:
    # Usuario, CI, Contrasena, TipoUsuario, Nombre, Apellido1, Apellido2, Celular, Direccion
    def post(self):
        result = {}
        result['success'] = 'true'
        result['message'] = 'Tipo de usuario registrado'
        id_tipoUsuario = int(self.request.get('id_tipoUsuario'))
        t_usuario = self.request.get('t_usuario')
        tipo = TIPO_USUARIO.register(id_tipoUsuario, t_usuario)
        tipo.put()
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class UserHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    # Params:
    # Usuario, CI, Contrasena, TipoUsuario, Nombre, Apellido1, Apellido2, Celular, Direccion
    def post(self):
        haveError = False
        result = {}
        result['success'] = 'false'
        Usuario = self.request.get('Usuario')
        CI = self.request.get('CI')
        TipoUsuario = None
        try:
            TipoUsuario = int(self.request.get('TipoUsuario'))
        except:
            haveError = True
            result['message'] = 'Tipo de usuario no se pudo convertir a int'
        Celular = None
        try:
            Celular = int(self.request.get('Celular'))
        except:
            Celular = 0
        Contrasena = self.request.get('Contrasena')
        Nombre = self.request.get('Nombre')
        Apellido1 = self.request.get('Apellido1')
        Apellido2 = self.request.get('Apellido2')
        Direccion = self.request.get('Direccion')
        if not Usuario or not CI or not Contrasena or not TipoUsuario:
            haveError =  True
            result['message'] = 'Algun campo falta, datos incompletos'
            result['data'] = {};
            result['data']['Usuario'] = Usuario;
            result['data']['CI'] = CI;
            result['data']['Contrasena'] = Contrasena;
            result['data']['TipoUsuario'] = TipoUsuario;
        if not haveError:
            user = USER.by_username(Usuario)
            if user is None:
                user = USER.register(Usuario, CI, Contrasena, TipoUsuario, Nombre, Apellido1, Apellido2, Celular, Direccion)
                user.put()
                result['success'] = 'true'
                result['app'] = 'valencia'
                result['message'] = 'Usuario registrado correctamente'
                result['data'] = []
                result['data'].append(user.to_dict());
            else:
                haveError =  True
                result['message'] = 'Ese nombre de usuario ya existe'
        else:
            result['success'] = 'false'
            a = dict()
            a['app'] = 'valencia'
            a['version'] = 'v1.0'
            result['appData'] = []
            result['appData'].append(a);
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))


class GetEncargadosHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        encargados = USER.get_allEncargados()
        result['data'] = encargados
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result)) 

class GetChefsHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        encargados = USER.get_allChefs()
        relaciones = CHEF_ENCARGADO.get_all()
        result['data'] = encargados
        result['relaciones'] = relaciones
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result)) 

class ProductoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        productos = PRODUCTO.get_all()
        result['data'] = productos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result)) 

    def post(self):
        result = {}
        result['success'] = 'false'
        nombre = self.request.get('nombre')
        ingredientes = self.request.get('ingredientes')
        precio = int(self.request.get('precio'))
        tipo = self.request.get('tipo')
        if nombre:
            producto = PRODUCTO.by_id_nombre(nombre)
            if not producto:
                producto = PRODUCTO.register(nombre, ingredientes, precio, tipo)
            else:
                producto.ingredientes = ingredientes
                producto.precio = precio
                producto.tipo = tipo
            producto.put()
            result['success'] = 'true'
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result)) 

class ChefEncargadoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        encargados = CHEF_ENCARGADO.get_all()
        result['data'] = encargados
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result)) 

    def post(self):
        result = {}
        result['success'] = 'false'
        chef_usuario = self.request.get('chef_usuario')
        encargado_usuario = self.request.get('encargado_usuario')
        empresa = self.request.get('empresa')
        if chef_usuario:
            Asignacion = CHEF_ENCARGADO.register(chef_usuario, encargado_usuario, empresa)
            Asignacion.put()
            result['success'] = 'true'
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result)) 

class EditarProductoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def post(self):
        result = {}
        result['success'] = 'false'
        nombre = self.request.get('nombre')
        ingredientes = self.request.get('ingredientes')
        precio = int(self.request.get('precio'))
        tipo = self.request.get('tipo')
        if nombre:
            producto = PRODUCTO.by_id_nombre(nombre)
            if producto:
                producto.ingredientes = ingredientes
                producto.precio = precio
                producto.tipo = tipo
                producto.put()
                result['success'] = 'true'
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class ProductoObtenerHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def post(self):
        result = {}
        nombre = self.request.get('nombre')
        result['success'] = 'false'
        if nombre:
            producto = PRODUCTO.by_id_nombre(nombre)
            if producto:
                result['data'] = producto.to_dict()
                result['success'] = 'true'
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class EliminarProductoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def post(self):
        result = {}
        nombre = self.request.get('nombre')
        result['success'] = 'false'
        if nombre:
            producto = PRODUCTO.by_id_nombre(nombre)
            if producto:
                producto.delete()
                result['success'] = 'true'
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class PedidoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        pedidos = PEDIDO.get_all()
        result['data'] = pedidos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

    def post(self):
        result = {}
        _id = self.request.get('id')
        fecha = self.request.get('fecha')
        nombre = self.request.get('nombre')
        usuario = self.request.get('usuario')
        estadoDeChef = self.request.get('estadoDeChef')
        cantidad = None
        try:
            cantidad = int(self.request.get('cantidad'))
        except ValueError:
            None
        estado = "pendiente"
        result['success'] = 'false'
        _idInt = 0
        try:
            _idInt = long(_id)
        except ValueError:
            _idInt = 0
        pedido = None
        if _idInt != 0:
            pedido = PEDIDO.by_id(_idInt)
        if pedido:
            if estadoDeChef:
                result['success'] = 'true'
                pedido.estadoDeChef = "Entregado"
            else:
                result['success'] = 'true'
                pedido.estado = "procesado"
            result['success'] = 'true'
        else:
            result['success'] = 'true'
            pedido = PEDIDO.register(fecha, nombre, cantidad, estado, usuario) 
        pedido.put()
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class ProductosDesayunoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        productos = PRODUCTO.all_by_tipo('desayuno')
        result['data'] = productos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class ProductosAlmuerzoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        productos = PRODUCTO.all_by_tipo('almuerzo')
        result['data'] = productos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class ProductosPlatoEspecialHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        productos = PRODUCTO.all_by_tipo('plato especial')
        result['data'] = productos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class ProductosRefrescoHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        productos = PRODUCTO.all_by_tipo('refresco')
        result['data'] = productos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class ProductosPostreHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        productos = PRODUCTO.all_by_tipo('postre')
        result['data'] = productos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class ComprasRealizadasHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        pedidos = COMPRA_REALIZADA.get_all()
        result['data'] = pedidos
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

    def post(self):
        result = {}
        fecha = self.request.get('fecha')
        nombre = self.request.get('nombre')
        cantidad = self.request.get('cantidad')
        unidad = self.request.get('unidad')
        user = self.request.get('user')
        comprado = self.request.get('comprado')
        result['success'] = 'true'
        compra = COMPRA_REALIZADA.register(fecha, nombre, cantidad, unidad, user, comprado) 
        compra.put()
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

class StockHandler(BaseHandler):
    def options(self):      
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    
    def get(self):
        result = {}
        result['success'] = 'true'
        stocks = STOCK.get_all()
        result['data'] = stocks
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))

    def post(self):
        result = {}
        nombre = self.request.get('nombre')
        cantidad = self.request.get('cantidad')
        result['success'] = 'true'
        u = STOCK.by_id_nombre(nombre)
        if not u:
            u = STOCK.register(nombre, cantidad)
        else:
            u.cantidad = cantidad
        u.put()
        if self.callback:
            self.response.write(self.callback + '(' + jhelp.getAsJSONObject(result) + ');');
        else:
            self.response.write(jhelp.getAsJSONObject(result))


application = webapp2.WSGIApplication([('/', MainHandler),
                                        ('/user', UserHandler),
                                        ('/login', LogInHandler),
                                        ('/getEncargados', GetEncargadosHandler),
                                        ('/getChefs', GetChefsHandler),
                                        ('/tipoUsuario', TipoUsuarioHandler),
                                        ('/chefEncargado', ChefEncargadoHandler),
                                        ('/producto', ProductoHandler),
                                        ('/producto/obtener', ProductoObtenerHandler),
                                        ('/producto/editar', EditarProductoHandler),
                                        ('/producto/eliminar', EliminarProductoHandler),
                                        ('/producto/tipo/desayunos', ProductosDesayunoHandler),
                                        ('/producto/tipo/almuerzos', ProductosAlmuerzoHandler),
                                        ('/producto/tipo/platosEspeciales', ProductosPlatoEspecialHandler),
                                        ('/producto/tipo/refrescos', ProductosRefrescoHandler),
                                        ('/producto/tipo/postres', ProductosPostreHandler),
                                        ('/pedido', PedidoHandler),
                                        ('/stock', StockHandler),
                                        ('/comprasRealizadas', ComprasRealizadasHandler),
                                       ], debug=True)
