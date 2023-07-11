from revistas_app import app
from flask import session, render_template, redirect, request, flash
from revistas_app.modelos.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/', methods = ['GET'])
def desplegar_login_registro():
    return render_template ('login_registro.html')

@app.route('/crear/usuario', methods = ['POST'])
def crear_usuario():
    data = {
        **request.form
    }
    usuario_existe = Usuario.obtener_usuario(data)
    if Usuario.val_registro(data, usuario_existe) == False:
        return redirect('/')
    else:
        contraseña_encriptada = bcrypt.generate_password_hash(data['password'])
        data['password'] = contraseña_encriptada
        id_usuario = Usuario.crear_usuario(data)
        session['nombre'] = data['nombre']
        session['apellido'] = data['apellido']
        session['id_usuario'] = id_usuario
    return redirect('/validar')
    
@app.route('/validar', methods=['GET'])
def desplegar_validar():
    return redirect('/revistas')
    
@app.route('/login', methods=['POST'])
def procesa_login():
    data = {
        "correo": request.form['correo_login']
    }
    usuario_existe = Usuario.obtener_usuario(data)

    if usuario_existe == None:
        flash("Correo Inválido", "error_login_correo")
        return redirect('/')
    else:
        if not bcrypt.check_password_hash(usuario_existe.password, request.form['contraseña_login']):
            flash("Credenciales Inválido", "error_login_contraseña")
            return redirect('/')
        else:
            session['nombre'] = usuario_existe.nombre
            session['apellido'] = usuario_existe.apellido
            session['id_usuario'] = usuario_existe.id
            return redirect('/validar')

@app.route('/logout', methods=['POST'])
def procesa_logout():
    session.clear()
    return redirect('/')

@app.route('/actualizar/usuario/<int:id>', methods=['POST'])
def editar_usuario(id):
    if "id_usuario" not in session:
        return redirect('/')
    else:
        usuario_existe = Usuario.obtener_uno({"id_usuario": id})
        if Usuario.val_registro(request.form, usuario_existe) == False:
            return redirect(f'/datos/usuario/{id}')
        else:
            data = {
                **request.form,
                "id_usuario": id,
                "correo": usuario_existe.correo
            }
            Usuario.actualizar_uno(data)
            return redirect(f'/datos/usuario/{id}')
