from revistas_app.config.mysqlconnection import connectToMySQL
from revistas_app import BASE_DATOS, EMAIL_REGEX, NOMBRE_REGEX
from flask import flash

class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo = data['correo']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def crear_usuario(cls,data):
        query = """
                INSERT INTO usuarios ( nombre, apellido, correo, password) 
                VALUES (%(nombre)s, %(apellido)s, %(correo)s, %(password)s);
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query,data)
        return resultado
    
    @classmethod
    def obtener_usuario(cls,data):
        query = """
                SELECT *
                FROM usuarios
                WHERE correo = %(correo)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query,data)
        if len(resultado) == 0:
            return None
        else:
            return Usuario(resultado[0])
        
    @classmethod
    def obtener_uno (cls,data):
        query = """
                SELECT *
                FROM usuarios
                WHERE id = %(id_usuario)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query,data)
        usuario = Usuario(resultado[0])
        return usuario 
    
    @classmethod
    def actualizar_uno (cls,data):
        query = """
                UPDATE usuarios
                SET nombre = %(nombre)s, apellido = %(apellido)s, correo = %(correo)s
                WHERE id = %(id_usuario)s;
                """
        return connectToMySQL(BASE_DATOS).query_db(query,data) 

    @staticmethod
    def val_registro(data, usuario_existe):
        valido = True
        if len(data['nombre']) < 3:
            valido = False
            flash('Nombre debe contener más de tres caracteres', "error_nombre")
        if not NOMBRE_REGEX.match(data['nombre']):
            valido = False
            flash('Favor proporcionar nombre valido (solo letras)', "error_nombre")
        if len(data['apellido']) < 3:
            valido = False
            flash('Apellido debe contener más de tres caracteres', "error_apellido")
        if not NOMBRE_REGEX.match(data['apellido']):
            valido = False
            flash('Favor proporcionar apellido valido (solo letras)', "error_apellido")
        if not EMAIL_REGEX.match(data['correo']):
            valido = False
            flash('Favor proporcionar correo valido', "error_correo")
        if 'password' in data and len(data['password']) < 8:
            valido = False
            flash('Contraseña debe contener más de ocho caracteres', "error_contraseña")
        if 'password' in data and data['password'] != data['confirmacion_contraseña']:
            flash('Las contraseñas no coinciden', "error_contraseña")
        if 'correo' in data and data['correo'] != data['correo']:
            if Usuario.usuario_existe(data['correo']):
                valido = False
                flash('Este usuario ya está en uso', "error_correo")
        return valido