import endpoints
from google.appengine.api import namespace_manager
from google.appengine.api import search
from google.appengine.api import users
from protorpc import message_types
from protorpc import remote

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
            subjectForm = SubjectForm()
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
            sectionForm = SectionForm()
            sectionForm.sectionWebSafeKey = section.key.urlsafe()
            sectionForm.name = section.name
            sectionFormList.append(sectionForm)
        return sectionFormList

    @ndb.transactional(xg=True)
    def _saveOrganization(self, organization, registeredUser, user_id):
        organizationKey = organization.put()
        
        registeredUser.isOwner = organizationKey
        registeredUser.orgKey = organizationKey
        registeredUser.key = ndb.Key(RegisteredUsers, user_id)
           
        registeredUser.put()
        return 
    
    """SchoolManagementAPI v0.1"""
    @endpoints.method(OrganizationForm, message_types.VoidMessage,
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
        
        self._saveOrganization(organization, registeredUser, user_id)
        
        return message_types.VoidMessage()
    
    @endpoints.method(GradeInputForm, message_types.VoidMessage,
            path='registerGrade', http_method='POST', name='registerGrade')
    def registerGrade(self, request):
        """Configure the school classes"""
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        grade = Grade()
        if request.delete:
            if request.gradeWebsafeKey:
                grade_key = ndb.Key(urlsafe=request.gradeWebsafeKey)
                grade_key.delete()
                return message_types.VoidMessage()
            else: raise endpoints.NotFoundException('Not a valid grade')
        subject_keys = []
        if request.subjectWebSafeKey:
            for key in request.subjectWebSafeKey:
                print key
                if ndb.Key(urlsafe=key) not in subject_keys:
                    subject_keys.append(ndb.Key(urlsafe=key))
            grade.subjectKey = subject_keys      
        if request:
            for field in ('name', 'orgSpecificName'):
                if hasattr(request, field):
                    val = getattr(request, field)
                    if val:
                        setattr(grade, field, str(val))
        if not request.orgSpecificName:
            grade.orgSpecificName = str(request.name)
        grade.orgKey = registeredUser.orgKey 
        grade.key = ndb.Key(Grade, str(request.name))
        grade.put()
        return message_types.VoidMessage()
    
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
            
    @endpoints.method(message_types.VoidMessage, GradeOutputForm,
            path='getGrades', http_method='POST', name='getGrades')
    def getGrades(self, request):
        """Configure the school classes"""
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        grades = Grade.query().fetch()
        return GradeOutputForm(grades=[self._copyGradestoForm(grade) for grade in grades])
    
    
    @endpoints.method(SectionForm, message_types.VoidMessage,
            path='registerSection', http_method='POST', name='registerSection')
    def registerSection(self, request):
        user = endpoints.get_current_user()
        user_id = helper.getUserId()
        registeredUser = helper.getRegisteredUser()
        if not registeredUser:
            raise endpoints.NotFoundException(
                'User is not registered to perform operation')
        namespace_manager.set_namespace(self._getNamespace(registeredUser))
        if request.delete == True:
            if request.sectionWebSafeKey:
                section_key = ndb.Key(urlsafe=request.sectionWebSafeKey)
                section_key.delete()
            else:
                endpoints.NotFoundException('Not a valid section key')
            return message_types.VoidMessage()
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
            for field in ('name', 'none'):
                if hasattr(request, field):
                    if field == 'name':
                        val = getattr(request, field)
                        if val:
                            setattr(section, field, str(val)) 
                            section.nameUpper = str(val).upper()
                        else:
                            raise endpoints.NotFoundException('Not a valid name')
                    else:
                        val = getattr(request, field)
                        if val:
                            setattr(section, field, str(val)) 
        section.organizerUserId = registeredUser.orgKey
        section.put()
        return message_types.VoidMessage()
    
    
    @endpoints.method(SubjectForm, message_types.VoidMessage,
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
        else:
            if request.code:
                subject = Subject()
                # subject_id = Subject.allocate_ids(size=1, parent=ndb.Key(urlsafe=getattr(request, 'gradeWebSafeKey')))[0]
                subject_key = ndb.Key(Subject, str(request.code))
                subject.key = subject_key
            else:raise endpoints.NotFoundException('Not a valid code')
        if request:
                for field in ('name', 'code', 'book'):
                    if hasattr(request, field):
                        val = getattr(request, field)
                        if val:
                            setattr(subject, field, val)
                if not request.mandatory:
                    subject.mandatory = request.mandatory
                subject.nameUpper = str(request.name).upper()
                subject.organizerUserId = registeredUser.orgKey
                subject.put()
            
        return message_types.VoidMessage()
    @ndb.transactional(xg=True)
    def _saveStudent(self, student, organization):
        student.put()
        organization.put()
        
    @endpoints.method(StudentForm, message_types.VoidMessage,
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
            student.rollNumber = organization.studentCount
        if request:
            for field in ('studentFees', 'studentName', 'studentAge', 'sectionWebSafeKey', 'subjectWebSafeKey'):
                if hasattr(request, field):
                    val = getattr(request, field)
                    if val:
                        setattr(student, field, str(val)) 
            if request.gradeWebSafeKey:
                student.gradeKey = ndb.Key(urlsafe=request.gradeWebSafeKey)
            if request.sectionWebSafeKey:
                student.sectionKey = ndb.Key(urlsafe=request.sectionWebSafeKey)
            subject_keys = []
            if request.subjectWebSafeKey:
                for key in request.subjectWebSafeKey:
                    print key
                    if ndb.Key(urlsafe=key) not in subject_keys:
                        subject_keys.append(ndb.Key(urlsafe=key))
                student.subjectKey = subject_keys
                
        student.orgKey = registeredUser.orgKey
        student.createdBy = registeredUser.key
        self._saveStudent(student, organization)
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
         
api = endpoints.api_server([SchoolManagementAPI]) 
