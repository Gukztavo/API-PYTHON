from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/iris'
db = SQLAlchemy(app)

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "nome": self.nome}

@app.route("/ingredientes", methods=['GET'])
def selecionaTodos():
    ingredientes_objetos = Ingrediente.query.all()
    # Chama o metodo to_json()
    ingredientes_json = [ingrediente.to_json() for ingrediente in ingredientes_objetos]
    
    return gera_response(200, "ingredientes", ingredientes_json)

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


#Listagem de 1 ingrediente
@app.route("/ingrediente/<id>", methods=["GET"])
def seleciona_ingrediente(id):
    ingrediente_objeto = Ingrediente.query.filter_by(id=id).first()
    ingrediente_json = ingrediente_objeto.to_json()

    if ingrediente_objeto:
        ingrediente_json = ingrediente_objeto.to_json()
        return gera_response(200, "ingrediente", ingrediente_json)
    else:
        return gera_response(404, "ingrediente", {}, "Ingrediente não encontrado")


#cAdastrar no banco
@app.route("/ingrediente",methods=["POST"])
def cria_ingrediente():
    body = request.get_json()


    try:
        ingrediente = Ingrediente(nome=body["nome"])
        db.session.add(ingrediente) # aqui eu abro sessão e dou add com o sqlalchamy
        db.session.commit()
        return gera_response(201,"ingrediente", ingrediente.to_json())
    except Exception as e:
        print(e)
        return gera_response(400,"ingrediente",{},"erro ao cadastrar")



#editar ingrediente

@app.route("/ingrediente/<id>",methods=["PUT"])
def atualiza_ingrediente(id):
    #pega o ingrediente
    ingrediente_objeto = Ingrediente.query.filter_by(id=id).first()
    #pega as modificacoes
    body = request.get_json()

    try:
        if('nome' in body):
            ingrediente_objeto.nome = body['nome']

        db.session.add(ingrediente_objeto)
        db.session.commit()
        return gera_response(200,"ingrediente",ingrediente_objeto.to_json())
    except Exception as e:
        print('Erro',e)
        return gera_response(400,"ingrediente",{},"Erro ao atualizar/editar")

@app.route("/ingrediente/<id>",methods=["DELETE"])
def deleta_ingrediente(id):
    Ingrediente_objeto = Ingrediente.query.filter_by(id=id).first()
    
    try:
        db.session.delete(Ingrediente_objeto)
        db.session.commit()
        return gera_response(200,"ingrediente",Ingrediente_objeto.to_json(),"Deletado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400,"ingrediente",{},"erro ao deletar")

app.run()
