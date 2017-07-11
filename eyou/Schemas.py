from marshmallow import Schema, fields



class TypeSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    popularity = fields.Int()
    category_id = fields.Int()

class PlaceSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    type_id = fields.Int()
    area_id = fields.Int()
    area = fields.Nested('AreaSchema',only='localName')
    type = fields.Nested('TypeSchema', only='name')
    lat = fields.Float()
    lon = fields.Float()


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    popularity = fields.Int()
    types = fields.Nested('TypeSchema', many=True,only=('id', 'name'))

class AreaSchema(Schema):
    id = fields.Int()
    lon = fields.Float()
    lat = fields.Float()
    country = fields.Str()
    city = fields.Str()
    localName = fields.Str()
    displayName = fields.Str()
    description = fields.Str()


