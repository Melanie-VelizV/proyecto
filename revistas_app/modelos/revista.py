from revistas_app.config.mysqlconnection import connectToMySQL
from revistas_app import BASE_DATOS
from revistas_app.modelos.usuario import Usuario
from flask import flash

class Revista:
    def __init__(self,data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.descripcion = data['descripcion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.id_usuario = None

    @classmethod
    def crear_revista(cls, data):
        query = """
                INSERT INTO revistas (titulo, descripcion, id_usuario)
                VALUES ( %(titulo)s, %(descripcion)s, %(id_usuario)s);
                """
        id_revista = connectToMySQL(BASE_DATOS).query_db(query,data)
        return id_revista

    @classmethod
    def get_all(cls):
        query = """
                SELECT * 
                FROM revistas re JOIN usuarios us 
                    ON re.id_usuario = us.id;
                """
        resultados = connectToMySQL(BASE_DATOS).query_db(query)
        lista_revistas = []
        for renglon in resultados:
            revista = Revista(renglon)
            data_usuario = {
                "id": renglon['us.id'],
                "nombre": renglon['nombre'],
                "apellido": renglon['apellido'],
                "correo": renglon['correo'],
                "password": renglon['password'],
                "created_at": renglon['us.created_at'],
                "updated_at": renglon['us.updated_at']
            }
            usuario = Usuario (data_usuario)
            revista.usuario = usuario
            lista_revistas.append(revista)
        return lista_revistas
    
    @classmethod
    def get_revista(cls, data):
        query = """
                SELECT * 
                FROM revistas re JOIN usuarios us 
                    ON re.id_usuario = us.id
                WHERE us.id =%(id_usuario)s;
                """
        results = connectToMySQL(BASE_DATOS).query_db(query, data)
        revistas = []
        for row in results:
            revistas.append(cls(row))
        return revistas
    
    @classmethod
    def obtener_una(cls,data):
        query = """
                SELECT * 
                FROM revistas re JOIN usuarios us 
                    ON re.id_usuario = us.id
                WHERE re.id =%(id_usuario)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        renglon = resultado[0]
        revista = Revista(renglon)
        data_usuario = {
            "id": renglon['us.id'],
            "nombre": renglon['nombre'],
            "apellido": renglon['apellido'],
            "correo": renglon['correo'],
            "password": renglon['password'],
            "created_at": renglon['us.created_at'],
            "updated_at": renglon['us.updated_at']
        }
        revista.usuario = Usuario(data_usuario)
        return revista
    
    @classmethod
    def eliminar_uno(cls,data):
        query = """
                DELETE FROM revistas 
                WHERE id = %(id)s;
                """
        print(query)
        return connectToMySQL(BASE_DATOS).query_db(query, data)

    @staticmethod
    def val_registro_revista(data):
        valido = True
        if len(data['titulo']) < 2:
            valido = False
            flash('Titulo debe contener más de dos caracteres', "error_titulo")
        if len(data['descripcion']) < 10:
            valido = False
            flash('descripcion debe contener más de diez caracteres', "error_descripcion")
        return valido