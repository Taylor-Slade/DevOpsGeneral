from marshmallow import Schema, fields, validate, pre_load
import bleach
from werkzeug.security import generate_password_hash


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True, validate=validate.Length(min=1, max=100))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
    phone_number = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=255))
    age = fields.Int(validate=validate.Range(min=0))

    @pre_load
    def sanitize_input(self, in_data, **kwargs):
        for field in in_data:
            if isinstance(in_data[field], str):
                in_data[field] = bleach.clean(in_data[field], strip=True)
        return in_data

    @pre_load
    def hash_password(self, in_data, **kwargs):
        data = dict(in_data)
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])
        return data
