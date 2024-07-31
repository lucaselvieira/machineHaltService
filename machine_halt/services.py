from datetime import datetime

from .models import MachineHalt, db


def parse_iso_datetime(iso_str):
    return datetime.fromisoformat(iso_str).replace(tzinfo=None)


def create_machine_halt(data):
    new_halt = MachineHalt(**data)
    db.session.add(new_halt)
    db.session.commit()
    return new_halt


def get_machine_halt_by_id(halt_id):
    return MachineHalt.query.get(halt_id)


def list_machine_halts(machine_tag, interval_start, interval_end):
    halts = MachineHalt.query.filter(
        MachineHalt.machine_tag == machine_tag
    ).all()

    # Step 2: Filter the fetched halts to include only those that match the interval criteria
    filtered_halts = [
        h for h in halts if (
                interval_start <= h.start_time <= interval_end or
                (h.end_time and interval_start <= h.end_time <= interval_end)
        )
    ]
    return filtered_halts


def update_machine_halt_end_time(halt_id, end_time):
    halt = MachineHalt.query.get(halt_id)
    if halt:
        halt.end_time = end_time
        db.session.commit()
    return halt


def update_machine_halt_reason(halt_id, reason):
    halt = MachineHalt.query.get(halt_id)
    if halt:
        halt.reason = reason
        db.session.commit()
    return halt


def delete_all_halts():
    num_rows_deleted = db.session.query(MachineHalt).delete()
    db.session.commit()
    return num_rows_deleted
