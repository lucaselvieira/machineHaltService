from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

machine_halts = []
current_id = 1


def get_machine_halt_by_id(halt_id):
    return next((h for h in machine_halts if h['id'] == halt_id), None)


def parse_iso_datetime(date_str):
    return datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)


@app.route('/machine-halt', methods=['POST'])
def create_halt():
    global current_id
    data = request.get_json()

    # Validate input
    if 'machine_tag' not in data or 'start_time' not in data:
        return jsonify({"error": "machine_tag and start_time are required"}), 400

    new_halt = {
        "id": current_id,
        "machine_tag": data['machine_tag'],
        "start_time": data['start_time'],
        "end_time": None,
        "reason": ""
    }
    machine_halts.append(new_halt)
    current_id += 1
    return jsonify(new_halt), 201


@app.route('/machine-halt/<int:id>', methods=['GET'])
def get_halt(id):
    halt = get_machine_halt_by_id(id)
    if halt is None:
        return jsonify({"error": "Machine halt not found"}), 404
    return jsonify(halt), 200


@app.route('/machine-halt/list', methods=['GET'])
def list_halts():
    machine_tag = request.args.get('machine_tag')
    interval_start = request.args.get('interval_start')
    interval_end = request.args.get('interval_end')

    if not machine_tag or not interval_start or not interval_end:
        return jsonify({"error": "machine_tag, interval_start, and interval_end are required"}), 400

    interval_start = parse_iso_datetime(interval_start)
    interval_end = parse_iso_datetime(interval_end)

    filtered_halts = [
        h for h in machine_halts if h['machine_tag'] == machine_tag and
                                    (interval_start <= parse_iso_datetime(h['start_time']) <= interval_end or
                                     (h['end_time'] and interval_start <= parse_iso_datetime(
                                         h['end_time']) <= interval_end))
    ]
    return jsonify(filtered_halts), 200


@app.route('/machine-halt', methods=['PUT'])
def update_halt():
    data = request.get_json()
    halt = get_machine_halt_by_id(data['id'])
    if halt is None:
        return jsonify({"error": "Machine halt not found"}), 404

    if 'end_time' in data:
        halt['end_time'] = data['end_time']
    if 'reason' in data:
        halt['reason'] = data['reason']
    return jsonify(halt), 200


@app.route('/machine-halt/all', methods=['DELETE'])
def delete_all_halts():
    global machine_halts, current_id
    machine_halts.clear()
    current_id = 1
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
