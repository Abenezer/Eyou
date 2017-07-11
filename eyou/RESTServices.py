from cornice import Service

from eyou.Schemas import AreaSchema
from services import IAuthenticationService
from models import User, Role

import pyramid.httpexceptions as exc
from pyramid.security import Allow, Deny, NO_PERMISSION_REQUIRED, Everyone, DENY_ALL

auth = Service('auth', '/auth', 'authentication service', cors_origins=('*',))


@auth.post()
def create_token(request):
    login = request.json['login']
    password = request.json['password']
    auth_svc = request.find_service(IAuthenticationService)
    user = auth_svc.authenticate(login, password)  # type: User
    if user:

        return {
            'result': 'ok',
            'token': request.create_jwt_token(user.id, name=user.username, roles=[r.name for r in user.roles])
        }
    else:
        return {
            'result': 'error'
        }



reg = Service('reg', '/register', 'registration service')
@reg.post()
def register_user(request):
    login = request.POST['login']
    password = request.POST['password']
    num_existing = request.dbsession.query(User).filter(User.username == login).count()
    if num_existing > 0:
        raise Exception('That Type already exists!')
    user = User(username=login)
    user.set_password(password)
    role = request.dbsession.query(Role).filter(Role.name == 'Admin').first()
    if role:
        user.roles.append(role)
    request.dbsession.add(user)



locate = Service('locate_area', '/locate', 'geocode an area', cors_origins=('*',))
@locate.get()
def locate_area(request):
    from geopy.geocoders import Nominatim
    q = request.params['q']
    print (q)
    geolocator = Nominatim(format_string='%s, addis ababa',timeout=10,country_bias='Ethiopia')
    location = geolocator.geocode(q)
    if location==None:
        raise exc.HTTPNotFound()
    return {'address':location.address,'lat':location.latitude,'lon':location.longitude}
reverse = Service('reverse_area', '/reverse', 'reverse geocode an area', cors_origins=('*',))
@reverse.get()
def reverse_area(request):
    lat = request.params['lat']
    lon = request.params['lon']
    from eyou.Helpers import toArea
    area = toArea(lon,lat)
    return AreaSchema().dump(area)
