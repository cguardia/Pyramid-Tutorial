from datetime import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.security import forget

from birdie.models import DBSession
from birdie.models import Chirp
from birdie.models import User
from birdie.models import check_login

from repoze.timeago import get_elapsed

def birdie_view(request):
    dbsession = DBSession()
    userid = authenticated_userid(request)
    user = dbsession.query(User).filter_by(userid=userid).first()
    chirps = dbsession.query(Chirp).filter(Chirp.author==user)
    chirps = chirps.order_by(Chirp.timestamp.desc()).limit(30)
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'userid': userid,
            'user': user,
            'elapsed': get_elapsed,
            'chirps': chirps}

def birdie_post(request):
    dbsession = DBSession()
    userid = authenticated_userid(request)
    user = dbsession.query(User).filter_by(userid=userid).one()
    chirp = request.params.get('chirp')
    author = user
    timestamp = datetime.utcnow()
    new_chirp = Chirp(chirp, author, timestamp)
    dbsession.add(new_chirp)
    chirps = dbsession.query(Chirp).filter(Chirp.author==user)
    chirps = chirps.order_by(Chirp.timestamp.desc()).limit(30)
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'elapsed': get_elapsed,
            'userid': userid,
            'user': user,
            'chirps': chirps}

def login_page(request):
    login = ''
    message = ''
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': message,
            'login': login}

def login(request):
    login = request.params['login']
    password = request.params['password']
    if check_login(login, password):
        headers = remember(request, login)
        return HTTPFound(location = '/',
                         headers = headers)
    message = 'Failed login'
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': message,
            'login': login}

def logout(request):
    headers = forget(request)
    return HTTPFound(location = '/',
                     headers = headers)

def join_page(request):
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': '',
            'userid': '',
            'fullname': '',
            'about': ''}

def join(request):
    dbsession = DBSession()
    userid = request.params.get('userid')
    user = dbsession.query(User).filter_by(userid=userid).first()
    password = request.params.get('password')
    confirm = request.params.get('confirm')
    fullname = request.params.get('fullname')
    about = request.params.get('about')
    if user:
        return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': "The userid %s already exists." % userid,
            'userid': userid,
            'fullname': fullname,
            'about': about}
    if confirm != password:
        return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': "The passwords don't match.",
            'userid': userid,
            'fullname': fullname,
            'about': about}
    if len(password) < 6:
        return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': "The password is too short. Minimum is 6 characters.",
            'userid': userid,
            'fullname': fullname,
            'about': about}
    user = User(userid, password, fullname, about)
    dbsession.add(user)
    headers = remember(request, userid)
    return HTTPFound(location = '/',
                     headers = headers)
