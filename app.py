from flask import Flask, request, jsonify
from marshmallow import ValidationError

from config import Config
from machine_halt.models import db
from machine_halt.schemas import MachineHaltSchema
from machine_halt.services import (
    create_machine_halt, get_machine_halt_by_id, list_machine_halts,
    update_machine_halt_end_time, update_machine_halt_reason, delete_all_halts, parse_iso_datetime
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    machine_halt_schema = MachineHaltSchema()
    machine_halts_schema = MachineHaltSchema(many=True)

    @app.route('/machine-halt', methods=['POST'])
    def create_halt():
        try:
            data = request.get_json()
            data['start_time'] = parse_iso_datetime(data['start_time'])
            halt = create_machine_halt(data)
            return jsonify(machine_halt_schema.dump(halt)), 201
        except ValidationError as err:
            return jsonify(err.messages), 400
        except (ValueError, TypeError) as err:
            return jsonify({'message': str(err)}), 400

    @app.route('/machine-halt/<int:halt_id>', methods=['GET'])
    def get_halt(halt_id):
        halt = get_machine_halt_by_id(halt_id)
        if halt is None:
            return jsonify({'message': 'Halt not found'}), 404
        return jsonify(machine_halt_schema.dump(halt))

    @app.route('/machine-halt/list', methods=['GET'])
    def list_halts():
        machine_tag = request.args.get('machine_tag')
        interval_start = request.args.get('interval_start')
        interval_end = request.args.get('interval_end')

        if not machine_tag or not interval_start or not interval_end:
            return jsonify({"error": "machine_tag, interval_start, and interval_end are required"}), 400

        try:
            interval_start = parse_iso_datetime(interval_start)
            interval_end = parse_iso_datetime(interval_end)
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid date format'}), 400

        halts = list_machine_halts(machine_tag, interval_start, interval_end)
        return jsonify(machine_halts_schema.dump(halts))

    @app.route('/machine-halt', methods=['PUT'])
    def update_halt():
        data = request.get_json()
        halt_id = data.get('id')
        end_time = data.get('end_time')
        reason = data.get('reason')

        if end_time and reason is None:
            try:
                end_time = parse_iso_datetime(end_time)
            except (ValueError, TypeError):
                return jsonify({'message': 'Invalid date format'}), 400
            halt = update_machine_halt_end_time(halt_id, end_time)
        elif reason and end_time is None:
            halt = update_machine_halt_reason(halt_id, reason)
        else:
            return jsonify({'message': 'or end_time or reason required'}), 400

        if halt is None:
            return jsonify({'message': 'Halt not found'}), 404
        return jsonify(machine_halt_schema.dump(halt))

    @app.route('/machine-halt/all', methods=['DELETE'])
    def delete_halts():
        delete_all_halts()
        return '', 204

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
