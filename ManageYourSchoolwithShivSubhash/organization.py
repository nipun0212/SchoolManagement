import datetime
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


GET_REQUEST_With_Key = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeKey=messages.StringField(1)
)


EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
@endpoints.api(name='schoolmanagement',
                version='v1',
                allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID],
                scopes=[EMAIL_SCOPE])
class SchoolManagementAPI(remote.Service):
    
    def _getNamespace(self, registeredUser):
        uniqueOrganizationName = Organization.query(registeredUser.orgKey == Organization.key).fetch(projection=[Organization.uniqueOrganizationName])
        
        return str(uniqueOrganizationName[0].uniqueOrganizationName)
    
    def _getSubjectFormFromSubjetcKeyList(self, subjectKeyList):
        subjectFormList = []
        for subKey in subjectKeyList:
            subject = subKey.get()
            subjectForm = registerStudent_InputForm()
            subjectForm.subjectWebSafeKey = subject.key.urlsafe()
            subjectForm.name = subject.name
            subjectForm.code = subject.code
            subjectFormList.append(subjectForm)
        return subjectFormList
     
    def _getSectionFormFromSectioncKeyList(self, sectionKeyList):
        sectionFormList = []
        print sectionKeyList
        for secKey in sectionKeyList:
            print 'secKey'
            print secKey
            section = secKey.get()
            sectionForm = registerSectionToGrade_InputForm()
            sectionForm.sectionWebSafeKey = section.key.urlsafe()
            sectionForm.name = section.name
            sectionFormList.append(sectionForm)
        return sectionFormList

    @ndb.transactional(xg=True)
    def _saveOrganization(self, organization, registeredUser, user_id):
        organizationKey = organization.put()
        
        registeredUser.isOwner = True
        registeredUser.orgKey = organizationKey
        registeredUser.key = ndb.Key(RegisteredUsers, user_id)
           
        registeredUser.put()
        return 
    
    """SchoolManagementAPI v0.1"""
    @endpoints.method(registerOrganization_InputForm, message_types.VoidMessage,
            path='registerOrganization', http_method='POST', name='registerOrganization')
    def registerOrganization(self, request):
        """Regiter the Organization with Details"""
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if registeredUser:
            raise endpoints.NotFoundException(
                'User already registered')
        else :
            registeredUser = RegisteredUsers()
        organization = Organization()
        if request:
            for field in ('orgName', 'phoneNumber'):
                if hasattr(request, field):
                    val = getattr(request, field)
                    if val:
                        setattr(organization, field, str(val))
        
        uniqueOrganizationName = str(request.orgName).upper()
        for i in range(1000):
            if Organization.query(Organization.uniqueOrganizationName == uniqueOrganizationName).fetch():
                uniqueOrganizationName = uniqueOrganizationName + str(i)
            else:
                break
        organization.uniqueOrganizationName = uniqueOrganizationName   
        organization.userID = user_id
        organization.emailID = user.email() 
        registeredUser.mainEmail = user.email() 
        registeredUser.userName = user.nickname()
        self._saveOrganization(organization, registeredUser, user_id)
        
        return message_types.VoidMessage()
    
    @endpoints.method(registerGrade_InputForm, message_types.VoidMessage,
            path='registerGrade', http_method='POST', name='registerGrade')
    def registerGrade(self, request):
        """Configure the school classes"""
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        print request.name
        print request.name.number
        grade = Grade()
        _key = ndb.Key(Grade, str(request.name))
        print _key
        if _key.get():
            grade = _key.get()
        else:
            grade = Grade()
        if request.gradeWebSafeKey:
            grade_key = ndb.Key(urlsafe=request.gradeWebSafeKey)
            grade = grade_key.get() 
        if request:
            if request.name:
                setattr(grade, 'name', str(request.name))
                setattr(grade, 'number', request.name.number)
                
            else:
                raise endpoints.BadRequestException("Class Name Required")
            if request.orgSpecificName:
                setattr(grade, 'orgSpecificName', request.orgSpecificName)
            else:
                grade.orgSpecificName = grade.name
        grade.orgKey = registeredUser.orgKey 
        grade.key = ndb.Key(Grade, grade.name)
        grade.number = request.name.number
        print grade.key
        print grade.key.id()
        print grade.key.get()
        grade.put()
        return message_types.VoidMessage()
    
    @endpoints.method(addSubjectsToGrade_InputForm, message_types.VoidMessage,
            path='addSubjectsToGrade', http_method='POST', name='addSubjectsToGrade')
    def addSubjectsToGrade(self, request):
        """Configure the school classes"""
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        if request.gradeWebSafeKey:
            grade_key = ndb.Key(urlsafe=request.gradeWebSafeKey)
            grade = grade_key.get() 
        else :raise endpoints.PreconditionFailedException("Not a valid Grade")
        
        if request.subjectWebSafeKey:
            for subjectWebSafeKey in request.subjectWebSafeKey:
                if ndb.Key(urlsafe=subjectWebSafeKey) not in grade.subjectKey:
                    grade.subjectKey.append(ndb.Key(urlsafe=subjectWebSafeKey))     
       
        grade.put()
        return message_types.VoidMessage()
    
   
    @endpoints.method(message_types.VoidMessage, GradeOutputForm,
            path='getGrades', http_method='POST', name='getGrades')
    def getGrades(self, request):
        """Configure the school classes"""
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        grades = Grade.query().order(Grade.number).fetch()
        return GradeOutputForm(grades=[self._copyGradestoForm(grade) for grade in grades])
    
    
    @endpoints.method(registerSectionToGrade_InputForm, message_types.VoidMessage,
            path='registerSection', http_method='POST', name='registerSection')
    def registerSectionToGrade(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        if request.sectionWebSafeKey:
            section = ndb.Key(urlsafe=request.sectionWebSafeKey).get()
        else:
            if request.gradeWebSafeKey:
                section = Section()
                section_id = Section.allocate_ids(size=1, parent=ndb.Key(urlsafe=getattr(request, 'gradeWebSafeKey')))[0]
                section_key = ndb.Key(Section, section_id, parent=ndb.Key(urlsafe=getattr(request, 'gradeWebSafeKey')))
                section.key = section_key
            else:raise endpoints.NotFoundException('Not a valid Grade')    
        if request:
            if request.name:
                setattr(section, 'name', str(request.name))    
                setattr(section, 'nameUpper' , str(request.name).upper())       
            else:
                raise endpoints.BadRequestException("Section Name Required")     
        section.put()
        return message_types.VoidMessage()
    
    @endpoints.method(registerSubject_InputForm, message_types.VoidMessage,
            path='registerSubject', http_method='POST', name='registerSubject')
    def registerSubject(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        print "registeredUser.orgKey.urlsafe()"
        print registeredUser.orgKey
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        if request.subjectWebSafeKey:
            subject_key = ndb.Key(urlsafe=request.subjectWebSafeKey)
            subject = subject_key.get()
            
        if request.code:
            subject = Subject()
            subject_key = ndb.Key(Subject, str(request.code))
            subject.key = subject_key
        else:raise endpoints.NotFoundException('Not a valid code')
                    
        if request:
            if request.name:
                setattr(subject, 'name', str(request.name))        
            else:
                raise endpoints.BadRequestException("Section Name Required")    
            if request.code:
                setattr(subject, 'code', str(request.code))  
            else:
                raise endpoints.BadRequestException("Subject Code Required")
    
        subject.put()
        return message_types.VoidMessage()
    
    
    @ndb.transactional(xg=True)
    def _saveKinds(self, kind=[]):
        for x in kind:
            x.put()
 
    @endpoints.method(EmployeeInputForm, message_types.VoidMessage,
            path='registerEmployee', http_method='POST', name='registerEmployee')
    def registerEmployee(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        organization = registeredUser.orgKey.get()
        if request.employeeWebSafeKey:
            employee = ndb.Key(urlsafe=request.employeeWebSafeKey).get()
        else:
            employee = Employee()
            organization.employeeCount = organization.employeeCount + 1
            employee.enrollementNumber = organization.employeeCount
        if request:
            for field in ('name', 'address'):
                if hasattr(request, field):
                    val = getattr(request, field)
                    if val:
                        setattr(employee, field, str(val)) 
        employee.orgKey = registeredUser.orgKey
        employee.createdBy = registeredUser.key
        kind = []
        kind.append(employee)
        kind.append(organization)
        self._saveKinds(kind)
        return message_types.VoidMessage()

        
    @endpoints.method(registerStudent_InputForm, message_types.VoidMessage,
            path='registerStudent', http_method='POST', name='registerStudent')
    def registerStudent(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        organization = registeredUser.orgKey.get()
        if request.studentWebSafeKey:
            student = ndb.Key(urlsafe=request.studentWebSafeKey).get()
        else:
            student = Student()
            organization.studentCount = organization.studentCount + 1
            setattr(student, 'serialNumber', organization.studentCount)  
        if request:
            if request.studentName:
                setattr(student, 'studentName', str(request.studentName))        
            else:
                raise endpoints.BadRequestException("studentName Name Required")    
            if request.studentAge:
                setattr(student, 'studentAge', str(request.studentAge))
            else:
                raise endpoints.BadRequestException("studentAge Name Required")   
            if request.gradeWebSafeKey:
                setattr(student, 'gradeKey', ndb.Key(urlsafe=request.gradeWebSafeKey))
            if request.sectionWebSafeKey:
                setattr(student, 'sectionKey', ndb.Key(urlsafe=request.sectionWebSafeKey))
            if request.subjectWebSafeKey:
                for subjectWebSafeKey in request.subjectWebSafeKey:
                    if ndb.Key(urlsafe=subjectWebSafeKey) not in student.subjectKey:
                        student.subjectKey.append(ndb.Key(urlsafe=subjectWebSafeKey))                    
        setattr(student, 'createdBy', registeredUser.key)
        setattr(student, 'createdOn', datetime.datetime.now())
        kind = []
        kind.append(student)
        kind.append(organization)
        self._saveKinds(kind)
        return message_types.VoidMessage()

    def _copyStudentsToForm(self, student):
        studentOutputForm = StudentOutputForm()
        setattr(studentOutputForm, 'studentName', getattr(student, 'studentName'))
        setattr(studentOutputForm, 'studentAge', getattr(student, 'studentAge'))
        setattr(studentOutputForm, 'studentFees', getattr(student, 'studentFees'))
        setattr(studentOutputForm, 'isApproved', getattr(student, 'isApproved'))
        setattr(studentOutputForm, 'studentRollNumber', getattr(student, 'rollNumber'))
        setattr(studentOutputForm, 'sectionWebSafeKey', getattr(student, 'sectionKey').urlsafe() if getattr(student, 'sectionKey') else getattr(student, 'sectionKey'))
#         setattr(studentOutputForm, 'subjectWebSafeKey', getattr(student, 'subjectKey').urlsafe())
        setattr(studentOutputForm, 'gradeWebSafeKey', getattr(student, 'gradeKey').urlsafe() if getattr(student, 'gradeKey') else getattr(student, 'gradeKey'))
        setattr(studentOutputForm, 'studentWebSafeKey', getattr(student, 'key').urlsafe() if getattr(student, 'key') else getattr(student, 'key'))
        return studentOutputForm
        
    @endpoints.method(message_types.VoidMessage, StudentsOutputForm,
            path='getStudents', http_method='POST', name='getStudents')
    def getStudents(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        students = Student.query().fetch()
        return StudentsOutputForm(students=[self._copyStudentsToForm(student) for student in students])
    
    @endpoints.method(GET_REQUEST_With_Key, StudentOutputForm1,
            path='getStudent', http_method='POST', name='getStudent')
    def getStudent(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        sectionKeyList = []
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        if not request.websafeKey:
            raise endpoints.NotFoundException(
                'Not Valid Key')
        studentOutputForm1 = StudentOutputForm1()
        student = ndb.Key(urlsafe=request.websafeKey).get()
        studentOutputForm1.studentName = student.studentName
        studentOutputForm1.studentAge = student.studentAge
        studentOutputForm1.studentFees = student.studentFees
        studentOutputForm1.grade = self._copyGradestoForm(student.gradeKey.get())
        studentOutputForm1.subjects = self._getSubjectFormFromSubjetcKeyList(student.subjectKey)
        print 'student.sectionKey'
        print student.sectionKey
        sectionKeyList.append(student.sectionKey)
        print "sectionKeyList" 
        print sectionKeyList 
        studentOutputForm1.section = self._getSectionFormFromSectioncKeyList(sectionKeyList)[0]
        
        return studentOutputForm1
    
    @endpoints.method(message_types.VoidMessage, RegisteredUsersOutputForm,
            path='getUser', http_method='POST', name='getUser')      
    def getUser(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        registeredUsersOutputForm = RegisteredUsersOutputForm()
        if not registeredUser:
            registeredUsersOutputForm.isUser = False
        else:
            registeredUsersOutputForm.userName = registeredUser.userName
            registeredUsersOutputForm.mainEmail = registeredUser.mainEmail
            # registeredUsersOutputForm.userAddress = registeredUser.userAddress
            # registeredUsersOutputForm.isOwner = True if registeredUser.isOwner else False
            registeredUsersOutputForm.isPrincipal = True if registeredUser.isPrincipal else False
            registeredUsersOutputForm.isAdmin = True if registeredUser.isAdmin else False
            registeredUsersOutputForm.isStudent = True if registeredUser.isStudent else False
            registeredUsersOutputForm.isUser = True
        return registeredUsersOutputForm
    @endpoints.method(RegisteredUsersInputForm, RegisteredUsersOutputForm,
            path='configureUser', http_method='POST', name='configureUser')      
    def configureUser(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        registeredUsersOutputForm = RegisteredUsersOutputForm()
        token = Token()
#         namespace_manager.set_namespace(self._getNamespace(registeredUser))
        
        if not registeredUser:
            registeredUser = RegisteredUsers()
            if request.orgKey:
                registeredUser.orgKey = ndb.Key(urlsafe=request.orgKey)
            else:
                raise endpoints.NotFoundException(
                'Please give Organization key')
        else:
            raise endpoints.InternalServerErrorException("User Already Registered")
        if request.isStudent == True:
            if request.studentKey:
                registeredUser.studentKey = ndb.Key(urlsafe=request.studentKey)
                token.tokenNumber = random.randint(10000, 99999)
                token.studentKey = registeredUser.studentKey
            else:
                raise endpoints.NotFoundException(
               'Please give student key')
        else:
            if request.isEmployee == True:
                if request.employeeKey:
                    registeredUser.employeeKey = ndb.Key(urlsafe=request.employeeKey)
                    token.tokenNumber = random.randint(10000, 99999)
                    token.employeeKey = registeredUser.employeeKey
                else:
                    raise endpoints.NotFoundException(
                    'Please give employee key')
        registeredUser.key = ndb.Key(RegisteredUsers, user_id)
        print registeredUser
        registeredUser.put()
        token.put()
        return registeredUsersOutputForm
        
    
    @endpoints.method(approveUser_InputForm, message_types.VoidMessage,
            path='approveUser', http_method='POST', name='approveUser')
    def approveUser(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.ForbiddenException("Not Allowed to update user")
        if not (registeredUser.isAdmin == True or registeredUser.isOwner == True):
            raise endpoints.ForbiddenException("Not Allowed to update user")
#         tokenFromDatabase = Token.query(ndb.GenericProperty(str(Token.employeeKey)) == str(request.registeredUserKey)).fetch(projection=["tokenNumber"])
        tokenFromDatabase = Token.query(Token.employeeKey == ndb.Key(urlsafe=request.registeredUserKey)).fetch(projection=["tokenNumber"])
        print tokenFromDatabase[0].tokenNumber
        if tokenFromDatabase[0].tokenNumber == request.tokenNumber:
            regiteredUserToApprove = RegisteredUsers.query(RegisteredUsers.orgKey == registeredUser.orgKey and RegisteredUsers.employeeKey == ndb.Key(urlsafe=request.registeredUserKey)).fetch()
            print regiteredUserToApprove[0]
            regiteredUserToApprove[0].isActive = True
            regiteredUserToApprove[0].put()
        else:
            raise endpoints.BadRequestException("Not a valid token Number")
            
    
        return message_types.VoidMessage()
        
        
        
api = endpoints.api_server([SchoolManagementAPI]) 
