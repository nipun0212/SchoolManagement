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
    
    def _create_document(self,):
        document = search.Document(
        # Setting the doc_id is optional. If omitted, the search service will
        # create an identifier.
        doc_id='Students',
        fields=[
            search.TextField(name='studentName'),
            search.TextField(name='studentAge')
        ])
        return document
    
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
    def _saveOrganization(self, organization, registeredUser, globalOrganization, user_id):
        organizationKey = organization.put()
        
        registeredUser.isOwner = True
        registeredUser.orgKey = organizationKey
        registeredUser.isActive = True
        registeredUser.key = ndb.Key(RegisteredUsers, user_id)
        registeredUser.put()
        
        globalOrganization.orgKey = organizationKey
        globalOrganization.put()
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
        globalOrganization = GlobalOrganization()
        orgCount = GlobalOrganization.query().count()
                
        globalOrganization.organizationNamespace = orgCount + 888
        organization = Organization()
        if request:
            for field in ('orgName', 'phoneNumber'):
                if hasattr(request, field):
                    val = getattr(request, field)
                    if val:
                        setattr(organization, field, str(val))
        
        organization.uniqueOrganizationName = globalOrganization.organizationNamespace
        organization.userID = user_id
        organization.emailID = user.email() 
        organization.key = ndb.Key(Organization, globalOrganization.organizationNamespace)
        registeredUser.mainEmail = user.email() 
        registeredUser.userName = user.nickname()
        self._saveOrganization(organization, registeredUser, globalOrganization, user_id)
        
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
        employee.key = ndb.Key(Employee, organization.employeeCount)
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
            setattr(student, 'key', ndb.Key(Student, organization.studentCount)) 
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
        d = self._create_document()
        d.studentAge = student.studentAge
        d.studentName = student.studentAge
        index = search.Index('student')
        index.put(d)
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
            registeredUsersOutputForm.isActive = True if registeredUser.isActive else False
        return registeredUsersOutputForm
    @endpoints.method(SelfRegistration_InputForm, message_types.VoidMessage,
            path='selfRegistration', http_method='POST', name='selfRegistration')      
    def selfRegistration(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        token = Token()
        if not registeredUser:
            registeredUser = RegisteredUsers()
            if request.orgKey:
                registeredUser.orgKey = ndb.Key(Organization, request.orgKey)
            else:
                raise endpoints.NotFoundException(
                'Please give Organization key')
        else:
            raise endpoints.InternalServerErrorException("User Already Registered")
        if request.studentKey:
            registeredUser.studentKey = ndb.Key(Student, request.studentKey)
            token.tokenNumber = random.randint(10000, 99999)
            token.studentKey = registeredUser.studentKey
        elif request.empKey:
            registeredUser.employeeKey = ndb.Key(Employee, request.empKey)
            token.tokenNumber = random.randint(10000, 99999)
            token.employeeKey = registeredUser.employeeKey
        registeredUser.key = ndb.Key(RegisteredUsers, user_id)
        print registeredUser
        registeredUser.put()
        token.put()
        return message_types.VoidMessage()
        
  
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
        tokenFromDatabaseQuery = Token.query()
        print tokenFromDatabaseQuery
        if request.empId:
            regiteredUserToApprove = RegisteredUsers.query(RegisteredUsers.orgKey == registeredUser.orgKey and RegisteredUsers.employeeKey == ndb.Key(Employee, request.empId)).fetch()
            tokenFromDatabase = tokenFromDatabaseQuery.filter(Token.employeeKey == ndb.Key(Employee, request.empId)).fetch(projection=["tokenNumber"])
            if not tokenFromDatabase:
                raise endpoints.BadRequestException("Not a valid tEnployee ID")
        elif request.studentId:
            regiteredUserToApprove = RegisteredUsers.query(RegisteredUsers.orgKey == registeredUser.orgKey and RegisteredUsers.studentKey == ndb.Key(Student, request.studentId)).fetch()
            tokenFromDatabase = tokenFromDatabaseQuery.filter(Token.studentKey == ndb.Key(Student, request.studentId)).fetch(projection=["tokenNumber"])
            if not tokenFromDatabase:
                raise endpoints.BadRequestException("Not a valid tEnployee ID")
        regiteredUserToApprove = regiteredUserToApprove[0]
        tokenFromDatabase = tokenFromDatabase[0]
        if tokenFromDatabase.tokenNumber == request.tokenNumber:
            print 
            regiteredUserToApprove.isActive = True
            regiteredUserToApprove.put()
            tokenFromDatabaseQuery.fetch()[0].key.delete()
        else:
            raise endpoints.BadRequestException("Not a valid token Number")
            
    
        return message_types.VoidMessage()
        
    @endpoints.method(giveRolesToUser_InputForm, message_types.VoidMessage,
            path='giveRolesToUser', http_method='POST', name='giveRolesToUser')
    def giveRolesToUser(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.ForbiddenException("Not Allowed to update user")
        if not (registeredUser.isAdmin == True or registeredUser.isOwner == True):
            raise endpoints.ForbiddenException("Not Allowed to update user")
        userToUpdate = RegisteredUsers.query(RegisteredUsers.key == ndb.Key(urlsafe=request.registeredUserKey)).fetch()
        if not userToUpdate:
            raise endpoints.ForbiddenException("Enter Correct Key")
        userToUpdate = userToUpdate[0]
        userToUpdate.isAdmin = True if request.isAdmin == True else False
        userToUpdate.isTeacher = True if request.isTeacher == True else False
        userToUpdate.isStudent = True if request.isStudent == True else False
        userToUpdate.isPrincipal = True if request.isPrincipal == True else False
        userToUpdate.put()
        
    @endpoints.method(giveAttendenceToStudent_InputForm, message_types.VoidMessage,
            path='giveAttendenceToStudent', http_method='POST', name='giveAttendenceToStudent')
    def giveAttendenceToStudent(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.ForbiddenException("Not Allowed to update user")
        if not (registeredUser.isAdmin == True or registeredUser.isOwner == True or registeredUser.isTeacher == True):
            raise endpoints.ForbiddenException("Not Allowed to update user")
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        print request.studentWebSafeKey
        studentAttendenceKey = ndb.Key(StudentAttendence, request.date, parent=ndb.Key(urlsafe=request.studentWebSafeKey))
        print studentAttendenceKey
        studentAttendence = studentAttendenceKey.get()
        print studentAttendence
        if not studentAttendence:
            studentAttendence = StudentAttendence()
        print studentAttendence
        studentAttendence.isPresent = True if request.isPresent == True else False
        studentAttendence.date = datetime.datetime.strptime(request.date, '%d-%m-%Y').date()
        studentAttendence.employeeKey = registeredUser.key
        studentAttendence.key = studentAttendenceKey
        studentAttendence.studentKey = ndb.Key(urlsafe=request.studentWebSafeKey)
#         student = ndb.Key(urlsafe=request.studentWebSafeKey).get()
#         attendencePercentage = StudentAttendence.all()
#         attendencePercentage = attendencePercentage.ancestor(ndb.Key(urlsafe=request.studentWebSafeKey))
        studentAttendence1 = StudentAttendence.query(ancestor=ndb.Key(urlsafe=request.studentWebSafeKey))
        totalAttendence = 0.0
        totalPresent = 0.0
        for s in studentAttendence1:
            totalAttendence = totalAttendence + 1
            print s.isPresent 
            if s.isPresent == True:
                totalPresent = totalPresent + 1
        print totalAttendence
        print totalPresent
        attendencePercentage = (totalPresent / totalAttendence) * 100
        student = ndb.Key(urlsafe=request.studentWebSafeKey).get()
        student.attendencePercentage = attendencePercentage
        kind = []
        kind.append(student)
        kind.append(studentAttendence)
        self._saveKinds(kind)
        print datetime.date.today()
        print studentAttendence
        return message_types.VoidMessage()
        


        
api = endpoints.api_server([SchoolManagementAPI]) 
