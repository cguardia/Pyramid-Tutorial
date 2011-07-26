from datetime import datetime

from birdie.models import DBSession
from birdie.models import Chirp

from repoze.timeago import get_elapsed

def birdie_view(request):
    dbsession = DBSession()
    chirps = dbsession.query(Chirp).filter(Chirp.author==u'anonymous')
    chirps = chirps.order_by(Chirp.timestamp.desc()).limit(30)
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'elapsed': get_elapsed,
            'chirps': chirps}

def birdie_post(request):
    dbsession = DBSession()
    chirp = request.params.get('chirp')
    author = u'anonymous'
    timestamp = datetime.utcnow()
    new_chirp = Chirp(chirp, author, timestamp)
    dbsession.add(new_chirp)
    chirps = dbsession.query(Chirp).filter(Chirp.author==u'anonymous')
    chirps = chirps.order_by(Chirp.timestamp.desc()).limit(30)
    return {'app_url': request.application_url,
            'static_url': request.static_url,
            'elapsed': get_elapsed,
            'chirps': chirps}
