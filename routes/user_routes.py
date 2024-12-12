from flask import Blueprint, app, request, jsonify
from models.user import User
from db import db  
from flasgger import swag_from

user_routes = Blueprint('user_routes', __name__)

usuarios = []

#Criar novo usuário
@user_routes.route('/api/criar_usuario', methods=['POST'])
@swag_from('create_user.yml')
def create_user():

    data = request.json
    new_user = User(
        nome=data['nome'],
        cpf=data['cpf'],
        endereco=data.get('endereco'),
        setor=data.get('setor'),
        funcao=data.get('funcao'),
        especialidade=data.get('especialidade'),
        registro_categoria=data.get('registro_categoria')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

#Lista todos os usuários
@user_routes.route('/api/exibe_usuarios', methods=['GET'])
@swag_from('get_all_users.yml') 
def get_all_users():

    usuarios = User.query.all()  
    resultado = []
    
    for usuario in usuarios:
        resultado.append({
            "matricula": usuario.id,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "setor": usuario.setor,
            "funcao": usuario.funcao,
            "especialidade": usuario.especialidade,
            "registro_categoria": usuario.registro_categoria
        })

    return jsonify(resultado), 200  


#Atualizar um usuário

@user_routes.route('/api/atualizar_usuario/<cpf>', methods=['PUT'])
#@swag_from('update_user.yml')
def atualizar_usuario(cpf):
    data = request.json
    usuario = User.query.filter_by(cpf=cpf).first()
    if usuario:
        usuario.nome = data['nome']
        usuario.setor = data['setor']
        usuario.funcao = data['funcao']
        usuario.especialidade = data['especialidade']
        usuario.registro_categoria = data['registro_categoria']
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!'})
    else:
        return jsonify({'message': 'Usuário não encontrado.'}), 404


#Excluir um usuário

@user_routes.route('/api/excluir_usuario/<cpf>', methods=['DELETE'])
@swag_from('delete_user.yml')
def excluir_usuario(cpf):
    usuario = User.query.filter_by(cpf=cpf).first()
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
