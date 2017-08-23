import logging

from google.appengine.api import search
from google.appengine.ext import deferred
from google.appengine.ext import ndb
from protorpc import messages


class Employee(ndb.Model):
    """Profile -- User prjhklhjlkofile object"""
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    enrollementNumber = ndb.IntegerProperty()
    createdBy = ndb.KeyProperty()

class Student(ndb.Model):
    """Profile -- User profile object"""
    serialNumber = ndb.IntegerProperty()
    studentName = ndb.StringProperty()
    studentAge = ndb.StringProperty()
    studentFees = ndb.StringProperty()
    createdBy = ndb.KeyProperty()
    createdOn = ndb.DateTimeProperty()
    gradeKey = ndb.KeyProperty(kind="Grade")
    sectionKey = ndb.KeyProperty(kind="Section")
    subjectKey = ndb.KeyProperty(kind="Subject", repeated=True)
    isApproved = ndb.BooleanProperty(default=False)
    attendencePercentage = ndb.FloatProperty(default=0.0)
    def _post_put_hook(self, future):
        document = search.Document(
                doc_id=self.studentName,
                fields=[
                   search.TextField(name='username', value=self.studentName),
                   search.TextField(name='studentAge', value=self.studentAge),
                   ])
        try:
            index = search.Index(name="StudentIndex")
            index.put(document)
        except search.Error:
                logging.exception('Put failed')

class GlobalOrganization(ndb.Model):
    orgKey = ndb.KeyProperty(kind="Organization")
    organizationNamespace = ndb.IntegerProperty()

    
class Organization(ndb.Model):
    """Organization"""
    orgName = ndb.StringProperty()
    phoneNumber = ndb.StringProperty()
    emailID = ndb.StringProperty()
    userID = ndb.StringProperty()
    studentCount = ndb.IntegerProperty(default=0) 
    employeeCount = ndb.IntegerProperty(default=0)
    uniqueOrganizationName = ndb.IntegerProperty()
       
   

class RegisteredUsers(ndb.Model):
    """RegisteredUsers -- User profile object"""
    userName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    orgKey = ndb.KeyProperty(kind=Organization)
    studentKey = ndb.KeyProperty(kind=Student)
    employeeKey = ndb.KeyProperty(kind=Employee)
    isOwner = ndb.BooleanProperty(default=False)
    isPrincipal = ndb.BooleanProperty(default=False)
    isAdmin = ndb.BooleanProperty(default=False)
    isTeacher = ndb.BooleanProperty(default=False)
    isStudent = ndb.BooleanProperty(default=False)
    isActive = ndb.BooleanProperty(default=False)

class Token(ndb.Model):
    studentKey = ndb.KeyProperty(kind=Student)
    employeeKey = ndb.KeyProperty(kind=Employee)
    tokenNumber = ndb.IntegerProperty()    

class StudentForm(messages.Message):
    """Profile -- User profile object"""
    studentName = messages.StringField(1)
    studentAge = messages.StringField(2)
    studentFees = messages.StringField(3)
    gradeWebSafeKey = messages.StringField(4)
    sectionWebSafeKey = messages.StringField(5)
    subjectWebSafeKey = messages.StringField(6, repeated=True)
    studentWebSafeKey = messages.StringField(7)

class StudentOutputForm(messages.Message):
    """StudentOutputForm -- User profile object"""
    studentName = messages.StringField(1)
    studentAge = messages.StringField(2)
    studentFees = messages.StringField(3)
    gradeWebSafeKey = messages.StringField(4)
    sectionWebSafeKey = messages.StringField(5)
    subjectWebSafeKey = messages.StringField(6, repeated=True)
    studentWebSafeKey = messages.StringField(7)
    studentRollNumber = messages.IntegerField(8)
    isApproved = messages.BooleanField(9)

class StudentOutputForm1(messages.Message):
    """StudentOutputForm -- User profile object"""
    studentName = messages.StringField(1)
    studentAge = messages.StringField(2)
    studentFees = messages.StringField(3)
#     grade = messages.MessageField("GradeForm", 4)
#     section = messages.MessageField("GradeForm", 5)
#     subjects = messages.MessageField("SubjectForm", 6, repeated=True)
    studentWebSafeKey = messages.StringField(7)
    studentRollNumber = messages.IntegerField(8)
    isApproved = messages.BooleanField(9)

class StudentsOutputForm(messages.Message):
    students = messages.MessageField(StudentOutputForm, 1, repeated=True)

class StudentsOutputForm1(messages.Message):
    students = messages.MessageField(StudentOutputForm1, 1, repeated=True)


    
class OrganizationForm(messages.Message):
    """OrganizationForm -- Organization outbound form message"""
    orgName = messages.StringField(1)
    phoneNumber = messages.StringField(2)

class EmployeeInputForm(messages.Message):
    name = messages.StringField(1)
    address = messages.StringField(2)
    employeeWebSafeKey = messages.StringField(3)



class RegisteredUsersOutputForm(messages.Message):
    userName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    isTeacher = messages.BooleanField(3, default=False)
    isPrincipal = messages.BooleanField(4, default=False)
    isAdmin = messages.BooleanField(5, default=False)
    isStudent = messages.BooleanField(6, default=False)
    isActive = messages.BooleanField(7, default=True)

class RegisteredUsersInputForm(messages.Message):
    userName = messages.StringField(1)
    orgKey = messages.StringField(2)
    employeeKey = messages.StringField(3)
    studentKey = messages.StringField(4)
    isEmployee = messages.BooleanField(5, default=False)
    isStudent = messages.BooleanField(6, default=False)
    
class Grade(ndb.Model):
    """Class -- Conference object"""
    name = ndb.StringProperty(required=True)
    number = ndb.IntegerProperty(required=False)
    orgSpecificName = ndb.StringProperty()
    subjectKey = ndb.KeyProperty(kind="Subject", repeated=True)
    orgKey = ndb.KeyProperty(kind=Organization)



# class GradeForm(messages.Message):
#     """GradeForm outbound form message"""
#     gradeName = messages.StringField(1)
#     gradeWebSafeKey = messages.StringField(2)
#     orgSpecificName = messages.StringField(3)
#     sections = messages.MessageField("SubjectForm", 4, repeated=True)
#     subjects = messages.MessageField("SubjectForm", 5, repeated=True)
#     
#     
# class GradeOutputForm(messages.Message):
#     """GradeOutputForm form message"""
#     grades = messages.MessageField(GradeForm, 1, repeated=True)

class Subject(ndb.Model):
    """Subject -- Conference object"""
    name = ndb.StringProperty(required=True)
    code = ndb.StringProperty()
    book = ndb.StringProperty()
    mandatory = ndb.BooleanProperty(default=True)
     
class Section(ndb.Model):
    """Section -- Conference object"""
    name = ndb.StringProperty(required=True)
    nameUpper = ndb.StringProperty(required=True)

class StudentAttendence(ndb.Model):
    studentKey = ndb.KeyProperty()
    date = ndb.DateProperty()
    isPresent = ndb.BooleanProperty(default=True)
    employeeKey = ndb.KeyProperty()
    when = ndb.DateTimeProperty(auto_now=True)
    
