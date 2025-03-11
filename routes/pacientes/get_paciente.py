from flask import request, jsonify
from models.pacientes import Paciente
from utils import get_local_time, get_user_timezone
from werkzeug.exceptions import BadRequest, NotFound

def buscar_paciente():
    try:
        campo = request.args.get('campo')
        valor = request.args.get('valor')

        if not campo or not valor:
            raise BadRequest("Campo e valor de busca são obrigatórios")

        if campo not in ['id', 'nome_completo', 'cpf']:
            raise BadRequest("Campo de busca inválido")

        if campo == 'id':
            paciente = Paciente.query.filter_by(id=valor).first()
        elif campo == 'nome_completo':
            paciente = Paciente.query.filter(Paciente.nome_completo.ilike(f'%{valor}%')).all()
        elif campo == 'cpf':
            paciente = Paciente.query.filter_by(cpf=valor).first()

        if not paciente:
            raise NotFound("Paciente não encontrado")

        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)

        if isinstance(paciente, list):
            pacientes = [p.to_dict() for p in paciente]
        else:
            pacientes = [paciente.to_dict()]

        return jsonify({
            'pacientes': pacientes
        }), 200

    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500