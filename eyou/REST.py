from cornice.resource import resource, view
from pyramid.response import Response
from models import *
from Schemas import *
from pyramid.security import Allow, Deny, NO_PERMISSION_REQUIRED, Everyone, Authenticated


def my_acl(request):
    return [
        (Allow, Authenticated, ['read']),
        (Allow, 'role:Admin', ['create', 'update']),
    ]


policy = dict(

    origins=('*',),

)


# @resource(collection_path='/users', path='/users/{id}')
# class User(object):
#
#     def __init__(self, request):
#         self.request = request
#
#     def collection_get(self):
#
#         return {'users': _USERS.keys()}
#
#

@resource(collection_path='/places', path='/places/{id}', acl=my_acl, cors_policy=policy)
class Places(object):
    def __init__(self, context, request):
        self.request = request
        self.DB = request.dbsession
        self.schema = PlaceSchema()
        self.schema_c = PlaceSchema(many=True)

    @view(permission='read')
    def collection_get(self):
        type_id = self.request.params.get('type_id')
        area_id = self.request.params.get('area_id')
        cat_id = self.request.params.get('cat_id')
        q = self.DB.query(Place)
        if type_id:
            q = q.filter(Place.type_id == type_id)
        if area_id:
            q = q.filter(Place.area_id == area_id)
        if cat_id:
            q = q.filter(Place.type.has(category_id=cat_id))
        return self.schema_c.dump(q.all())

    @view(permission='read')
    def get(self):
        id = int(self.request.matchdict['id'])
        return self.schema.dump(self.DB.query(Place).filter(Place.id == id).first())

    @view(permission='update')
    def collection_post(self):
        place = self.schema.load(self.request.json).data

        # print(self.request.json_body)
        num_existing = self.DB.query(Place).filter(Place.name == place['name']).count()
        if num_existing > 0:
            raise Exception('That place already exists!')

        p = Place(name=place['name'], description=place['description'], type_id=place['type_id'], lon=place['lon'],
                  lat=place['lat']);
        from eyou.Helpers import toArea
        area = toArea(place['lon'], place['lat'])
        if area is not None:
            area_existing = self.DB.query(Area).filter(Area.OSM_id == area.OSM_id).first()
            if area_existing is not None:
                p.area_id = area_existing.area_id
            else:
                p.area = area

        self.DB.add(p)
        return self.schema.dump(place)


@resource(collection_path='/types', path='/types/{id}', acl=my_acl, cors_policy=policy)
class Types(object):
    def __init__(self, context, request):
        self.request = request
        self.DB = request.dbsession
        self.schema = TypeSchema()
        self.schema_c = TypeSchema(many=True)

    @view(permission='read')
    def collection_get(self):
        return self.schema_c.dump(self.DB.query(Type))

    @view(permission='read')
    def get(self):
        id = int(self.request.matchdict['id'])
        return self.schema.dump(self.DB.query(Type).filter(Type.id == id).first())

    @view(permission='update')
    def collection_post(self):
        type = self.schema.load(self.request.json).data

        # print(self.request.json_body)
        num_existing = self.DB.query(Type).filter(Type.name == type['name']).count()
        if num_existing > 0:
            raise Exception('That Type already exists!')
        self.DB.add(Type(name=type['name'], description=type['description'], category_id=type['category_id']))
        return self.schema.dump(type)


@resource(collection_path='/categories', path='/categories/{id}', acl=my_acl, cors_policy=policy)
class Categories(object):
    def __init__(self, context, request):
        self.request = request
        self.DB = request.dbsession
        self.schema = CategorySchema()
        self.schema_c = CategorySchema(many=True)

    @view(permission='read')
    def collection_get(self):
        return self.schema_c.dump(self.DB.query(Category))

    @view(permission='read')
    def get(self):
        id = int(self.request.matchdict['id'])
        cat = self.DB.query(Category).filter(Category.id == id).first()
        return self.schema.dump(cat)

    def delete(self):
        id = int(self.request.matchdict['id'])
        cat = self.DB.query(Category).filter(Category.id == id).first();
        self.DB.delete(cat)

    @view(permission='update')
    def collection_post(self):
        cat = self.schema.load(self.request.json).data

        # print(self.request.json_body)
        num_existing = self.DB.query(Category).filter(Category.name == cat['name']).count()
        if num_existing > 0:
            raise Exception('That Type already exists!')
        self.DB.add(Category(name=cat['name'], description=cat['description']))
        return self.schema.dump(cat)


@resource(collection_path='/areas', path='/areas/{id}', acl=my_acl, cors_policy=policy)
class Areas(object):
    def __init__(self, context, request):
        self.request = request
        self.DB = request.dbsession
        self.schema = AreaSchema()
        self.schema_c = AreaSchema(many=True)

    @view(permission='read')
    def collection_get(self):
        return self.schema_c.dump(self.DB.query(Area))

    @view(permission='read')
    def get(self):
        id = int(self.request.matchdict['id'])
        area = self.DB.query(Area).filter(Area.id == id).first()
        return self.schema.dump(area)

    def delete(self):
        id = int(self.request.matchdict['id'])
        area = self.DB.query(Area).filter(Area.id == id).first();
        self.DB.delete(area)

    @view(permission='update')
    def collection_post(self):
        area = self.schema.load(self.request.json).data

        # print(self.request.json_body)
        num_existing = self.DB.query(Area).filter(Area.displayName == area['display_name']).count()
        if num_existing > 0:
            raise Exception('That Area already exists!')
        self.DB.add(Area(displayName=area['displayName'], lon=area['lon'], lat=area['lat']))
        return self.schema.dump(area)
