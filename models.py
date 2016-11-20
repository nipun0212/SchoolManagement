from google.appengine.ext import ndb
from protorpc import messages



class Organization(ndb.Model):
    """Organization"""
    orgName = ndb.StringProperty()
    phoneNumber = ndb.StringProperty()
    emailID = ndb.StringProperty()
    userID = ndb.StringProperty()
    studentCount = ndb.IntegerProperty(default=0) 
    teacherCount = ndb.IntegerProperty(default=0)
    uniqueOrganizationName = ndb.StringProperty()
    
    
class OrganizationForm(messages.Message):
    """OrganizationForm -- Organization outbound form message"""
    orgName = messages.StringField(1)
    phoneNumber = messages.StringField(2)
    

class RegisteredUsers(ndb.Model):
    """RegisteredUsers -- User profile object"""
    userName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    userAddress = ndb.StringProperty()
    orgKey = ndb.KeyProperty(kind=Organization)
    isOwner = ndb.KeyProperty()
    isPrincipal = ndb.KeyProperty()
    isAdmin = ndb.KeyProperty()
    isStudent = ndb.KeyProperty(kind="Student")
    
class Grade(ndb.Model):
    """Class -- Conference object"""
    name = ndb.StringProperty(required=True)
    orgSpecificName = ndb.StringProperty()
    subjectKey = ndb.KeyProperty(kind="Subject", repeated=True)
    orgKey = ndb.KeyProperty(kind=Organization)

class GradeForm(messages.Message):
    """GradeForm outbound form message"""
    gradeName = messages.StringField(1)
    gradeWebSafeKey = messages.StringField(2)
    orgSpecificName = messages.StringField(3)
    sections = messages.MessageField("SectionForm", 4, repeated=True)
    subjects = messages.MessageField("SubjectForm", 5, repeated=True)

class GradeInputForm(messages.Message):
    name = messages.EnumField('GradeList', 1)
    orgSpecificName = messages.StringField(2)
    subjectWebSafeKey = messages.StringField(3, repeated=True)
    gradeWebSafeKey = messages.StringField(4)
    delete = messages.BooleanField(5, default=False)
    
    
class GradeOutputForm(messages.Message):
    """GradeOutputForm form message"""
    grades = messages.MessageField(GradeForm, 1, repeated=True)

class Subject(ndb.Model):
    """Subject -- Conference object"""
    name = ndb.StringProperty(required=True)
    code = ndb.StringProperty()
    nameUpper = ndb.StringProperty(required=True)
    book = ndb.StringProperty()
    mandatory = ndb.BooleanProperty(default=True)
    organizerUserId = ndb.KeyProperty(kind=Organization)
     
class SubjectForm(messages.Message):
    """SubjectForm -- Conference outbound form message"""
    name = messages.StringField(1, required=True)
    code = messages.StringField(2, required=True)
    subjectWebSafeKey = messages.StringField(3)
    delete = messages.BooleanField(4, default=True)
    mandatory = messages.BooleanField(5, default=True)
    gradeWebSafeKey = messages.StringField(6)
    book = messages.StringField(7)
    
    
class Student(ndb.Model):
    """Profile -- User profile object"""
    rollNumber = ndb.IntegerProperty()
    orgKey = ndb.KeyProperty(kind="Organization")
    studentName = ndb.StringProperty()
    studentAge = ndb.StringProperty()
    studentFees = ndb.StringProperty()
    createdBy = ndb.KeyProperty(kind=RegisteredUsers)
    gradeKey = ndb.KeyProperty(kind="Grade")
    sectionKey = ndb.KeyProperty(kind="Section")
    subjectKey = ndb.KeyProperty(kind="Subject", repeated=True)
    isApproved = ndb.BooleanProperty(default=False)
    attendencePercentage = ndb.StringProperty()

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
    grade = messages.MessageField("GradeForm", 4)
    section = messages.MessageField("SectionForm", 5)
    subjects = messages.MessageField("SubjectForm", 6, repeated=True)
    studentWebSafeKey = messages.StringField(7)
    studentRollNumber = messages.IntegerField(8)
    isApproved = messages.BooleanField(9)

class StudentsOutputForm(messages.Message):
    students = messages.MessageField(StudentOutputForm, 1, repeated=True)

class StudentsOutputForm1(messages.Message):
    students = messages.MessageField(StudentOutputForm1, 1, repeated=True)

class Section(ndb.Model):
    """Section -- Conference object"""
    name = ndb.StringProperty(required=True)
    nameUpper = ndb.StringProperty(required=True)
    organizerUserId = ndb.KeyProperty(kind="Organization")


class SectionForm(messages.Message):
    """ConferenceFormmm -- Conference outbound form message"""
    name = messages.StringField(1)
    gradeWebSafeKey = messages.StringField(2)
    sectionWebSafeKey = messages.StringField(3)
    delete = messages.BooleanField(4, default=False)

class SectionOutputForm(messages.Message):
    sections = messages.MessageField(SectionForm, 1, repeated=True)
    

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
