from revistas_app import app
from flask import render_template,request,session, redirect
from revistas_app.modelos.revista import Revista
from revistas_app.modelos.usuario import Usuario

@app.route('/revistas')
def desplegar_revistas():
    listas_revistas = Revista.get_all()
    print(listas_revistas)
    return render_template("dashboard.html", listas_revistas=listas_revistas)

@app.route('/mostrarrevista/<int:id_usuario>')
def desplegar_revista(id_usuario):
    data ={ 
        "id_usuario":id_usuario
    }
    if "id_usuario" not in session:
        return redirect('/')
    else:
        revista = Revista.obtener_una(data)
        return render_template("leer_revista.html",revista=revista)

@app.route('/agregar/revista', methods = ['GET'])
def desplegar_formulario_revista():
    if "id_usuario" not in session:
        return redirect('/')
    else:
        return render_template("formulario_revista.html")

@app.route('/crear/revista',  methods = ['POST'])
def nueva_revista():
    data = {
        **request.form,
        "id_usuario": session['id_usuario']
    }
    if Revista.val_registro_revista(data) == False:
        return redirect('/agregar/revista')
    else:
        id_revista = Revista.crear_revista(data)
        return redirect('/revistas')

@app.route('/datos/usuario/<int:id_usuario>', methods=['GET'])
def desplegar_revistas_usuario(id_usuario):
    print (id_usuario)
    data ={ 
        "id_usuario":id_usuario
    }
    if "id_usuario" not in session:
        return redirect('/')
    else:
        print (data)
        usuario = Usuario.obtener_uno(data)
        return render_template("editar_cuenta.html", revistas = Revista.get_revista(data), usuario=usuario)

@app.route('/borrar/<int:id>/<int:id_usuario>', methods=['GET'])
def eliminar_revista(id, id_usuario):
    data = {
        "id" : id
    }
    if "id_usuario" not in session:
        return redirect('/')
    else:
        Revista.eliminar_uno(data)
        return redirect('/datos/usuario/'+ str(id_usuario))