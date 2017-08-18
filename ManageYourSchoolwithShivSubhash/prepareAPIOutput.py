import random

import endpoints
from google.appengine.api import namespace_manager
from google.appengine.api import search
from google.appengine.api import users
from protorpc import message_types
from protorpc import remote
from apiForms import *
import helper
from models import *
from settings import WEB_CLIENT_ID

def _copyGradestoForm(self, grade):
    sectionKeyList = []
    sections = Section.query(ancestor=grade.key).fetch()
    for section in sections:
        sectionKeyList.append(section.key)
    sectionFormList = self._getSectionFormFromSectioncKeyList(sectionKeyList)
    subjectFormList = self._getSubjectFormFromSubjetcKeyList(grade.subjectKey)  
    gf = GradeForm()
    gf.sections = sectionFormList
    gf.subjects = subjectFormList
    setattr(gf, 'gradeWebSafeKey', getattr(grade, 'key').urlsafe())
    setattr(gf, 'gradeName', getattr(grade, 'name'))
    setattr(gf, 'orgSpecificName', getattr(grade, 'orgSpecificName'))
    return gf
        