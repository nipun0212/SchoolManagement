import os

import endpoints

from google.appengine.ext import ndb
from models import RegisteredUsers
import utils


def getUserId():
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        if str((os.environ.copy()['HTTP_HOST'])) == "localhost:8080":
            user_id = utils.getUserId(user, "oauth")
            print "Running on LocalHost"
        else:
            user_id = user.user_id()
            print "Running on Non Local Host"
        return user_id

def getRegisteredUser():
        user_id = getUserId()
        registeredUserKey = ndb.Key(RegisteredUsers, user_id)
        registeredUser = registeredUserKey.get()
        return registeredUser
    
# def getKey(kind,parent=None,id=None):
#     
#      p_key = ndb.Key(Profile, user_id)
#         # allocate new Conference ID with Profile key as parent
#         c_id = Conference.allocate_ids(size=1, parent=p_key)[0]
#         # make Conference key from ID
#         c_key = ndb.Key(Conference, c_id, parent=p_key)