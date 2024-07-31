from marshmallow import Schema, fields


class MachineHaltSchema(Schema):
    id = fields.Int(dump_only=True)
    machine_tag = fields.Str(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime()
    reason = fields.Str()
