from flask import request, jsonify
from models.pacientes import Paciente
from db import db
from utils import validate_cpf
from werkzeug.exceptions import BadRequest, NotFound

def excluir_paciente(cpf):
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        paciente = Paciente.query.filter_by(cpf=cpf).first()
        if not paciente:
            raise NotFound("Paciente não encontrado")
        
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente excluído com sucesso!'}), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500