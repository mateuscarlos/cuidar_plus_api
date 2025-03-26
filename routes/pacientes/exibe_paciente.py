from flask import jsonify
from models.pacientes import Paciente
from werkzeug.exceptions import NotFound

def exibir_paciente(id):
    try:
        paciente = Paciente.query.get(id)
        
        if not paciente:
            raise NotFound(f"Paciente com ID {id} não encontrado")
            
        return jsonify({
            'paciente': paciente.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500

def exibir_pacientes():
    try:
        pacientes = Paciente.query.all()
        return jsonify({
            'pacientes': [p.to_dict() for p in pacientes]
        }), 200
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500