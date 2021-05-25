from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from datetime import date
from multiselectfield import MultiSelectField
from django.utils import timezone


def branch_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Branches/{0}/{1}'.format(instance.BranchName,filename)
def course_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Courses/{0}/{1}'.format(instance.CourseName,filename)


# Create your models here.
class Institution(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return '{0}/{1}'.format(instance.name, filename)
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return '{0}/{1}'.format(instance.name, filename)
    user = models.IntegerField(verbose_name="Users",default=1)
    institutionCode = models.CharField(verbose_name="Institution Code",default="000",max_length=150,unique=True)
    name = models.CharField(verbose_name="Institution Name",default="Name",max_length=150,unique=True)
    chairmanName = models.CharField(verbose_name="Chairman Name",default="Chairman Name", max_length=150)
    contactPersonName = models.CharField(verbose_name="Contact Person Name",default="Contact Person Name", max_length=150)
    contactPersonPhone = PhoneNumberField(blank=True)
    contactPersonEmail = models.EmailField(verbose_name="Contact Person Email", default="Contact Person Email",max_length=150)
    address =  models.CharField(verbose_name="Address",default="Address",max_length=500)
    image = models.ImageField(verbose_name="Image",upload_to=user_directory_path, default='static/images/brochure.jpg')
    status = [('Active','Active'),('Inactive','Inactive')]
    Status = models.CharField(verbose_name="Status",choices=status,default="Active",max_length=50)
    cityId = models.IntegerField(verbose_name="City ID",default=1)
    stateID = models.IntegerField(verbose_name="State Id",default=1)
    logo = models.ImageField(upload_to=user_directory_path, default='brochure.jpg')
    description = models.TextField(_(
        'description'), max_length=500, blank=True)
    brochure = models.ImageField(upload_to =user_directory_path, default='brochure.jpg')
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Institution'
        managed = True
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'


# Create your models here.
class Branch(models.Model):
    user = models.IntegerField(verbose_name="User",default=1)
    BranchCode = models.CharField(max_length=10,verbose_name="Branch Code",unique=True,blank=True)
    BranchName = models.CharField(max_length=100,verbose_name="Branch Name",unique=True,blank=True)
    Image = models.ImageField(upload_to = branch_upload,verbose_name="BranchImage")
    status = [('Active' , 'Active'),('Inactive','Inactive')]
    Status = models.CharField(max_length=20,choices=status)
    DateofJoin = models.DateField(verbose_name="Date of Joining",default=date.today) 
    def __str__(self):
        return self.BranchName
    
    class  Meta:
        db_table = 'Branch'
        managed = True
        verbose_name = 'Branch' 
        verbose_name_plural = 'Branches'
        ordering = ['-DateofJoin']

class SupportingDoc(models.Model):
    user = models.IntegerField(verbose_name="User",default=1)
    DocumentName = models.CharField(max_length=25,default=None,verbose_name="Supporting Documents",unique=True)
    status = [('Active', 'Active'),('Inactive','Inactive')]
    Status = models.CharField(max_length=25,choices=status)
    DateofAdd = models.DateField(verbose_name="Date of Joining",default=date.today)
    def __str__(self):
        return self.DocumentName
    
    class Meta:
        db_table = 'SupportingDocuments'
        managed = True
        verbose_name = 'Supporting Document'
        verbose_name_plural = 'Supporting Documents'

class Course(models.Model):    
    user = models.IntegerField(verbose_name="User",default=1)
    CourseCode = models.CharField(max_length=10,verbose_name="Course Code",unique=True)
    CourseName = models.CharField(max_length=100,verbose_name="Course Name",unique=True)
    Branch = models.IntegerField(verbose_name="branch",default=1)
    CourseDuration = models.IntegerField(verbose_name="Course Duration")
    CourseDescription = models.TextField(verbose_name="Course Description")
    CourseImage = models.ImageField(upload_to= course_upload)
    status = [('Active' , 'Active'),('Inactive','Inactive')]
    Status = models.CharField(max_length=20,choices=status)
    DateofJoin = models.DateField(verbose_name="Date of Joining",default=date.today)
    SupDoc = models.CharField(verbose_name="Supporting Doc",max_length=25,default=None)
    # SupDoc = MultiSelectField(choices="",max_length=100)
    CourseImage = models.ImageField(verbose_name="Course Image")


    def __str__(self):
        return self.CourseName
    

    class Meta:
        db_table = 'Courses'
        managed = True
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class planBanner(models.Model):
    user = models.IntegerField(verbose_name="User ID",default=1)
    Title = models.CharField(verbose_name="Title",default="Title",max_length=150 )
    Description = models.CharField(verbose_name="Description",default="Description",max_length=500 )
    status = [('Active','Active'),('Inactive','Inactive')]
    Status = models.CharField(verbose_name="Status",default="Active",choices=status,max_length=150)
    Image = models.ImageField(upload_to= "Planbanner/")
    date = models.DateField(default=date.today)
    def __str__(self):
        return self.Title

    class Meta:
        db_table = 'PlanBanner'
        managed = True
        verbose_name = 'Planbanner'
        verbose_name_plural = 'Planbanners'


class introBanner(models.Model):
    user = models.IntegerField(verbose_name="User ID",default=1)
    Title = models.CharField(verbose_name="Title",default="Title",max_length=150 )
    Description = models.CharField(verbose_name="Description",default="Description",max_length=500 )
    status = [('Active','Active'),('Inactive','Inactive')]
    Status = models.CharField(verbose_name="Status",default="Active",choices=status,max_length=150)
    Image = models.ImageField(upload_to= "Introbanner/")
    date = models.DateField(default=date.today)
    def __str__(self):
        return self.Title

    class Meta:
        db_table = 'IntroBanner'
        managed = True
        verbose_name = 'Introbanner'
        verbose_name_plural = 'Introbanners'

class instituteBanner(models.Model):
    user = models.IntegerField(verbose_name="User ID",default=1)
    Title = models.CharField(verbose_name="Title",default="Title",max_length=150 )
    status = [('Active','Active'),('Inactive','Inactive')]
    Status = models.CharField(verbose_name="Status",default="Active",choices=status,max_length=150)
    Image = models.ImageField(upload_to= "institutebanner/")
    date = models.DateField(default=date.today)
    def __str__(self):
        return self.Title

    class Meta:
        db_table = 'instituteBanner'
        managed = True
        verbose_name = 'institutebanner'
        verbose_name_plural = 'institutebanners'


class Staff(models.Model):
    
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'Staff/{0}/{1}'.format(instance.name, filename)
    institutionID = models.IntegerField(verbose_name="Institution ID",default=1)
    image = models.ImageField(verbose_name="Image",upload_to=user_directory_path, default='static/images/brochure.jpg')
    name = models.CharField(verbose_name="Name",max_length=150,default="Staff Name",unique=True)
    fatehrName = models.CharField(verbose_name="Father's Name",max_length=150,default="Father Name")
    nationality = models.CharField(verbose_name="Nationality",max_length=150,default="Indian")
    email = models.EmailField(verbose_name="Email",max_length=254,default="email@email.com",unique=True)
    phone = PhoneNumberField(blank=True)
    DOB  = models.DateField(verbose_name="Date of Birth")
    gen = [('Male','Male'),('Female','Female'),('Other','Other')]
    marital = [('Single','Single'),('Married','Married'),('Widowed','Widowed'),('Divorced','Divorced')]
    status = [('Active','Active'),('Inactive','Inactive')]
    gender = models.CharField(verbose_name="Gender",choices=gen,default="Male",max_length=150)
    maritalStatus = models.CharField(verbose_name="Marital Status",choices=marital,default="Single",max_length=150)
    annualSalary = models.IntegerField(verbose_name="Annual Salary",default=25000)
    designation = models.CharField(verbose_name="Designation",max_length=150,default="Founder")
    branchId = models.IntegerField(default=1,verbose_name="Branch")
    aadhaarNumber = PhoneNumberField(blank= True)
    panNumber = models.CharField(verbose_name="Pan Number",max_length=254,default="Pan132V2hh")
    DateofJoin = models.DateField(default=date.today)
    Status = models.CharField(choices=status,verbose_name="Status",max_length=254)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'Staff'
        managed = True
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'



class Students(models.Model):
    batch = models.IntegerField(verbose_name='Batch',default=date.today().year)
    batchSection = models.CharField(verbose_name="batch year", max_length=254, default="1st year")
    studentID = models.CharField(verbose_name="Student ID",default="BRANCH-COURSE-BATCH-AdID",max_length=120)
    institutionId = models.CharField(verbose_name="Institution ID",default=1,max_length=150)
    name = models.CharField(verbose_name="Student Name",default="Name",max_length=150)
    email = models.CharField(verbose_name="Student Email",default="email@email.com",max_length=245)
    branchId = models.IntegerField(verbose_name="Branch",default=1)
    courseId = models.IntegerField(verbose_name="Course",default=1)
    phone = PhoneNumberField(blank=True)
    documents = models.ImageField(blank=True)
    address = models.CharField(verbose_name="Address",max_length=600,default="address")
    guardianName = models.CharField(verbose_name="Gaurdian Name",default="Gaurdian Name",max_length=150)
    guardianPhone = PhoneNumberField(blank=True)
    DateOfJoin = models.DateField(default=date.today,verbose_name="Date of Join")
    
    class Meta:
        db_table = 'Student'
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    

    def __str__(self):
        return self.name
    

class instituteBranch(models.Model):
    institutionId= models.IntegerField(verbose_name="Institution ID",default=1)
    branchCode = models.CharField(verbose_name="Branch Code",default="BSC",max_length=150,unique=True)
    branchId = models.IntegerField(verbose_name='Branch ID',default=1)
    # branchId = models.ForeignKey(Branch,related_name="branch",on_delete=models.CASCADE)
    status = [('Active','Active'),('Inactive','Inactive')]
    Status = models.CharField(choices=status,verbose_name="Status",max_length=254)
    dateCreated = models.DateField(default=date.today,verbose_name="Date Created")

    def __str__(self):
        return self.branchCode
    
    class Meta:
        db_table = 'InstitutionBranch'
        managed = True
        verbose_name = 'InstitutionBranch'
        verbose_name_plural = 'InstitutionBranches'

class institutionCourse(models.Model):
    id = models.AutoField(primary_key=True)
    institutionId= models.IntegerField(verbose_name="Institution ID",default=1)
    courseCode = models.CharField(verbose_name="Course Code",default="BSC",max_length=150,unique=True)
    courseFee = models.CharField(verbose_name="Course Fee",default="100000",max_length=150)
    branchId = models.IntegerField(verbose_name='Branch ID',default=1)
    courseId = models.IntegerField(verbose_name='Course ID',default=1)
    status = [('Active','Active'),('Inactive','Inactive')]
    Status = models.CharField(choices=status,verbose_name="Status",max_length=254)
    admissionid = models.IntegerField(verbose_name="Students",default=0)
    dateCreated = models.DateField(default=date.today,verbose_name="Date Created")
    
    def __str__(self):
        return self.courseCode
    
    class Meta:
        db_table = 'InstitutionCourse'
        managed = True
        verbose_name = 'InstitutionCourse'
        verbose_name_plural = 'InstitutionCourses'

    

