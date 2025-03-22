from flask import request, jsonify
from models.pacientes import Paciente
from db import db
from werkzeug.exceptions import BadRequest, NotFound

def excluir_paciente(paciente_id):
    try:
        # Validar se o ID é um número inteiro válido
        try:
            paciente_id = int(paciente_id)
        except ValueError:
            raise BadRequest("ID de paciente inválido")
            
        # Buscar paciente pelo ID
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            raise NotFound("Paciente não encontrado")
        
        # Excluir o paciente
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