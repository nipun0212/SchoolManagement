from google.appengine.ext import ndb
from protorpc import message_types
from protorpc import messages

import models


class addSubjectsToGrade_InputForm(messages.Message):
    gradeWebSafeKey = messages.StringField(1)
    subjectWebSafeKey = messages.StringField(2, repeated=True)
        
class registerOrganization_InputForm(messages.Message):
    """OrganizationForm -- Organization outbound form message"""
    orgName = messages.StringField(1)
    phoneNumber = messages.StringField(2)

class registerGrade_InputForm(messages.Message):
    name = messages.EnumField('GradeList', 1)
    orgSpecificName = messages.StringField(2)
    gradeWebSafeKey = messages.StringField(3)

class registerSectionToGrade_InputForm(messages.Message):
    """ConferenceFormmm -- Conference outbound form message"""
    name = messages.StringField(1)
    gradeWebSafeKey = messages.StringField(2)
    sectionWebSafeKey = messages.StringField(3)

# class GradeForm(messages.Message):
#     """GradeForm outbound form message"""
#     gradeName = messages.StringField(1)
#     gradeWebSafeKey = messages.StringField(2)
#     orgSpecificName = messages.StringField(3)
#     sections = messages.MessageField("SectionForm", 4, repeated=True)
#     subjects = messages.MessageField("SubjectForm", 5, repeated=True)
    
    
class GradeOutputForm(messages.Message):
    """GradeOutputForm form message"""
    grades = messages.MessageField(registerSectionToGrade_InputForm, 1, repeated=True)
     
class SectionOutputForm(messages.Message):
    sections = messages.MessageField(registerSectionToGrade_InputForm, 1, repeated=True)
    
class registerSubject_InputForm(messages.Message):
    """SubjectForm -- Conference outbound form message"""
    name = messages.StringField(1, required=True)
    code = messages.StringField(2, required=True)
    subjectWebSafeKey = messages.StringField(3)
    
class registerStudent_InputForm(messages.Message):
    """Profile -- User profile object"""
    studentName = messages.StringField(1)
    studentAge = messages.StringField(2)
    gradeWebSafeKey = messages.StringField(3)
    sectionWebSafeKey = messages.StringField(5)
    subjectWebSafeKey = messages.StringField(6, repeated=True)
    studentWebSafeKey = messages.StringField(7)

class approveUser_InputForm(messages.Message):
    empId = messages.StringField(1)
    studentId = messages.StringField(2)
    tokenNumber = messages.IntegerField(3)

class giveRolesToUser_InputForm(messages.Message):
    registeredUserKey = messages.StringField(1, required=True)
    isAdmin = messages.BooleanField(2)
    isTeacher = messages.BooleanField(3)
    isStudent = messages.BooleanField(4)
    isPrincipal = messages.BooleanField(5)


class giveAttendenceToStudent_InputForm(messages.Message):
    studentWebSafeKey = messages.StringField(1, required=True)
    date = messages.StringField(2)
    isPresent = messages.BooleanField(3)



class SelfRegistration_InputForm(messages.Message):
    orgKey = messages.StringField(1)
    empKey = messages.StringField(2)
    studentKey = messages.StringField(3)
    
class GradeList(messages.Enum):
    """GradeList enumeration value"""
    PreNursery = 1
    Nursery = 2
    JuniorKG = 3
    SeniorKG = 4
    First = 5
    Second = 6
    Third = 7
    Fourth = 8
    Fifth = 9
    Sixth = 10
    Seventh = 11
    Eigth = 12
    Nine = 13
    Ten = 14
    Eleven = 15
    Twelth = 16
