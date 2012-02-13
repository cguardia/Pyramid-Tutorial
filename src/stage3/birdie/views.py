from datetime import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.security import forget
from pyramid.view import view_config
from pyramid.url import route_url

from birdie.models import DBSession
from birdie.models import Chirp
from birdie.models import User
from birdie.models import Follower
from birdie.models import check_login

from repoze.timeago import get_elapsed

@view_config(route_name='home',
                permission='view',
                renderer='templates/birdie.pt')
def birdie_view(request):
    dbsession = DBSession()
    userid = authenticated_userid(request)
    user = dbsession.query(User).filter_by(userid=userid).first()
    follows = dbsession.query(Follower).filter(Follower.follower==user.id)
    follows = follows.order_by(Follower.follows.asc()).limit(10)
    followers = dbsession.query(Follower).filter(Follower.follows==user.id)
    followers = followers.order_by(Follower.follower.asc()).limit(10)
    chirpers = [follow.follows for follow in follows]
    chirpers.append(user.id)
    chirps = dbsession.query(Chirp).filter(Chirp.author_id.in_(chirpers))
    chirps = chirps.order_by(Chirp.timestamp.desc()).limit(30)
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'userid': userid,
            'user': user,
            'elapsed': get_elapsed,
            'follows': follows,
            'followers': followers,
            'user_chirps': False,
            'chirps': chirps}

@view_config(route_name='home',
                request_method='POST',
                permission='view',
                renderer='templates/birdie.pt')
def birdie_post(request):
    dbsession = DBSession()
    userid = authenticated_userid(request)
    user = dbsession.query(User).filter_by(userid=userid).one()
    chirp = request.params.get('chirp')
    author = user
    timestamp = datetime.utcnow()
    new_chirp = Chirp(chirp, author, timestamp)
    dbsession.add(new_chirp)
    return HTTPFound(location = '/')

@view_config(context='pyramid.httpexceptions.HTTPForbidden',
                request_method='GET',
                renderer='templates/login.pt')
def login_page(request):
    login = ''
    message = ''
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': message,
            'login': login}

@view_config(context='pyramid.httpexceptions.HTTPForbidden',
                request_method='POST',
                renderer='templates/login.pt')
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

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = '/',
                     headers = headers)

@view_config(route_name='join',
                request_method='GET',
                renderer='templates/join.pt')
def join_page(request):
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'message': '',
            'userid': '',
            'fullname': '',
            'about': ''}

@view_config(route_name='join',
                request_method='POST',
                renderer='templates/join.pt')
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

@view_config(route_name='users',
             permission="view",
             renderer='birdie:templates/birdie.pt')
def user_chirps(request):
    dbsession = DBSession()
    userid = authenticated_userid(request)
    user = dbsession.query(User).filter_by(userid=userid).first()
    matchdict = request.matchdict
    other_userid = matchdict.get('userid')
    other_user = dbsession.query(User).filter_by(userid=other_userid).first()
    url = route_url('users', request, userid=other_userid)
    if other_user is None:
        return HTTPNotFound(location=url)
    chirps = dbsession.query(Chirp).filter(Chirp.author==other_user)
    chirps = chirps.order_by(Chirp.timestamp.desc()).limit(30)
    follows = dbsession.query(Follower).filter(Follower.follower==other_user.id)
    follows = follows.order_by(Follower.follows.asc()).limit(10)
    followers = dbsession.query(Follower).filter(Follower.follows==other_user.id)
    followers = followers.order_by(Follower.follower.asc()).limit(10)
    followed = dbsession.query(Follower).filter(Follower.follower==user.id)
    followed = followed.filter(Follower.follows==other_user.id).first()
    follow_url = route_url('follow', request, userid=other_userid)
    unfollow_url = route_url('unfollow', request, userid=other_userid)
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'userid': userid,
            'chirps': chirps,
            'user_chirps': True,
            'user': other_user,
            'original_user': user,
            'elapsed': get_elapsed,
            'follows': follows,
            'followers': followers,
            'followed': followed,
            'follow_url': follow_url,
            'unfollow_url': unfollow_url
        }

@view_config(route_name='follow',
             permission="view",
             renderer='birdie:templates/birdie.pt')
def follow(request):
    dbsession = DBSession()
    userid = authenticated_userid(request)
    user = dbsession.query(User).filter_by(userid=userid).first()
    matchdict = request.matchdict
    other_userid = matchdict.get('userid')
    other_user = dbsession.query(User).filter_by(userid=other_userid).first()
    follower = user.id
    follows = other_user.id
    new_follower = Follower(follower, follows)
    dbsession.add(new_follower)
    return HTTPFound(location = '/')

@view_config(route_name='unfollow',
             permission="view",
             renderer='birdie:templates/birdie.pt')
def unfollow(request):
    dbsession = DBSession()
    userid = authenticated_userid(request)
    user = dbsession.query(User).filter_by(userid=userid).first()
    matchdict = request.matchdict
    other_userid = matchdict.get('userid')
    other_user = dbsession.query(User).filter_by(userid=other_userid).first()
    follower = user.id
    follows = other_user.id
    dbsession.query(Follower).filter(Follower.follower==follower).filter(Follower.follows==follows).delete()
    return HTTPFound(location = '/')

