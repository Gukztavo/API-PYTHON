from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:utJnahZlnDwJkDlyhWLkNnNLBsBUPBtx@junction.proxy.rlwy.net:19380/railway'
app.app_context().push()

db = SQLAlchemy(app)


class Ingrediente(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "nome": self.nome}

class Receita(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100))
    
    def to_json(self):
        return{"id":self.id, "nome":self.nome}
    
# class ReceitaIngrediente(db.Model):
#     __tablename__ = 'receita_ingrediente' 
#     id = db.Column(db.Integer, primary_key=True)
#     receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), nullable=False)
#     ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)

#     receita = db.relationship('Receita', backref=db.backref('receita_ingrediente', lazy=True))
#     ingrediente = db.relationship('Ingrediente', backref=db.backref('receita_ingrediente', lazy=True))
    
   




@app.route("/receita", methods=['GET'])
def selecionaTodas():
    receita_objetos = Receita.query.all()
    receita_json = [receita.to_json() for receita in receita_objetos]
    
    return gera_response(200, "receitas", receita_json)

    

@app.route("/ingrediente", methods=['GET'])
def selecionaTodos():
    ingredientes_objetos = Ingrediente.query.all()
    # Chama o metodo to_json()
    ingredientes_json = [ingrediente.to_json() for ingrediente in ingredientes_objetos]
    
    return gera_response(200, "ingredientes", ingredientes_json)




@app.route("/receita/")

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
    
#Cadastros
@app.route("/receita", methods=["POST"])
def cria_receita():
    body = request.get_json()

    try: 
        receita = Receita(nome=body["nome"])
        db.session.add(receita)
        db.session.commit()
        ingredientes_ids = body.get("ingredientes",[])
        for ingrediente_id in ingredientes_ids:
            receita_ingrediente = ReceitaIngrediente(
                receita_id=receita.id, ingrediente_id = ingrediente_id
            )
            db.session.add(receita_ingrediente)        

        db.session.commit()
        return gera_response(201,"receita", receita.to_json())
    except Exception as e:
        print(e)
        return gera_response(400,"receita", receita.to_json())

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

#Editar
@app.route("/receita/<id>", methods=['PUT'])
def atualiza_receita(id):
    receita_objeto = Receita.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        if 'nome' in body:
            receita_objeto.nome = body['nome']
        
        # Limpa as relacoes antigas
        ReceitaIngrediente.query.filter_by(receita_id=id).delete()

        # Associav novos ingredientes
        ingredientes_ids = body.get("ingredientes", [])
        for ingrediente_id in ingredientes_ids:
            receita_ingrediente = ReceitaIngrediente(
                receita_id=receita_objeto.id, ingrediente_id=ingrediente_id
            )
            db.session.add(receita_ingrediente)

        db.session.commit()
        return gera_response(200,"receita",{},"receita atualizada")
    except Exception as e:
        print('Erro',e)
        return gera_response(400,"receita",{},"erro ao atualizar")

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
    

 #Delete
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
    

#Filtro de receita 
@app.route("/receita/filtrar", methods=["GET"])
def filtra_receitas():
    ingredientes_ids = request.args.getlist("ingredientes")

    if not ingredientes_ids:
        return gera_response(400, "receitas", {}, "Nenhum Ingrediente informado")

    ingredientes_ids = list(map(int, ingredientes_ids))

    receitas = Receita.query.join(ReceitaIngrediente).filter(
        ReceitaIngrediente.ingrediente_id.in_(ingredientes_ids)
    ).all()

    receitas_json = [receita.to_json() for receita in receitas]

    return gera_response(200, "receitas", receitas_json, "receita compativel com os ingredientes")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

# app.run()