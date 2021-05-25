from django.core import paginator
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import  auth
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import NewUser
from ed.models import Institution,Branch, Students,SupportingDoc,Course,introBanner,instituteBanner,planBanner,Staff,instituteBranch,institutionCourse
from django.contrib import messages
from django.core.mail import send_mail
import pymongo,json
from django.http import JsonResponse,HttpResponse
from django.conf import settings
import datetime,os
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.core import serializers
# import pandas as pd

# Create your views here.
@login_required(login_url="login")
def index(request):
    request.session['title'] = ""
    # pagetitle ={ title : "Eduvy, India's first online admission facilitating app"}
    if request.user.email:
        return redirect("dashboard")
    else:
        return login(request)


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("dashboard")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("login")
    else:

        return render(request, "index.html")
    return render(request, "index.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url="login")
def dashboard(request):
    # users  = Institution.objects.get(user = request.user.id)
    # request.session['college_name']  = users.name
    # request.session['college_id']  = users.id
    # print(request.session['college_name'])
    # print(request.session['college_id'])
    request.session['title'] = "Dashboard"
    return render(request, "dashboard.html")
    

def send_email(subject, body, email):
    try:
        email_msg = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], reply_to=[email])
        email_msg.send()
        return "Message sent :)"
    except:
        return redirect('dashboard')


@login_required(login_url="login")
def institution(request):
    request.session['title'] = "Institution"
    try:
        if request.method == "POST":
            name = request.POST['institution_name']
            institution_code = request.POST['institution_code']
            state = request.POST['state']
            city = request.POST['city']
            address = request.POST['address']
            chairman_name = request.POST['chairman_name']
            contact_person_name = request.POST['contact_person_name']
            contact_person_email = request.POST['contact_person_email']
            contact_person_phone = request.POST['contact_person_phone']
            institution_image = request.FILES['institution_image']
            status = request.POST['status']
            randompass = NewUser.objects.make_random_password()
            print(randompass)
            userreg = NewUser(email = contact_person_email,is_institute = True,is_active =True) 
            userreg.set_password(randompass)     
            userreg.save()
            print(userreg.id)
            InstituteSave = Institution(user = userreg.id, institutionCode = institution_code, name = name, chairmanName = chairman_name, contactPersonEmail = contact_person_email, contactPersonName = contact_person_name, contactPersonPhone = contact_person_phone, address = address, image = institution_image , Status = status, cityId = city, stateID = state,)
            InstituteSave.save()
            subject = 'welcome to Eduvy'
            message = f'Hi, thank you for registering in Eduvy.Your Password is {randompass}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [contact_person_email, ]
            send_mail( subject, message, email_from, recipient_list )
            return redirect('institution')
    except Exception :
        institutes = Institution.objects.all()
        paginator = Paginator(institutes,10)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            institute = paginator.page(page)
        except(EmptyPage,InvalidPage):
            institute = paginator.page(paginator.num_pages) 
        return render(request,'institutions.html',{'institute':institute})
    if request.user.is_superuser:
        institutes = Institution.objects.all()
        paginator = Paginator(institutes,10)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            institute = paginator.page(page)
        except(EmptyPage,InvalidPage):
            institute = paginator.page(paginator.num_pages) 
        return render(request,'institutions.html',{'institute':institute})

@csrf_exempt
def statecity(request):
    if request.method == "POST":
        state_id = request.POST['state_id']
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        # Database Name
        db = client["eduvy"]
        
        # Collection Name
        con = db["Citites"]
        myquery = { "stateId": state_id }
        x = con.find(myquery)
        city= []
        for data in x:
            cityid  = data['id']
            cityName = data['city']
            c = {"id" : cityid,"city" : cityName}
            city.append(c)
        print(city)
        data = json.dumps(city)
        return HttpResponse(data)
    return redirect('institution')

@login_required(login_url="login")
@csrf_exempt
def branch(request):
    request.session['title'] = "Branch"
    if request.method == "POST":
        BranchCode = request.POST["branch_code"]
        Branchname = request.POST["branch_name"]
        Image = request.FILES["branch_image"]
        Status = request.POST["status"]
        BranchSave = Branch(user = request.user.id, BranchCode=BranchCode, BranchName=Branchname, Image=Image, Status=Status)
        BranchSave.save()
        return redirect('branch')
    bran = Branch.objects.all()
    paginator = Paginator(bran,10)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        branch = paginator.page(page)
    except(EmptyPage,InvalidPage):
        branch = paginator.page(paginator.num_pages)
    return render(request, "branch.html", {"branches": branch})


@login_required(login_url="login")
@csrf_exempt
def course(request):
    request.session['title'] = "Course"
    try:
        if request.method == "POST":
            BranchID = request.POST['branch_id']
            CourseCode = request.POST["course_code"]
            Coursename = request.POST["course_name"]
            Duration = request.POST['duration']
            Descrip = request.POST['description']
            Doc = request.POST['documents']
            Image = request.FILES["course_image"]
            Status = request.POST["status"]
            print(BranchID)
            

            CourseSave = Course(user = request.user.id,
                Branch=BranchID, CourseCode=CourseCode, CourseName=Coursename, CourseDuration=Duration, CourseDescription = Descrip, SupDoc = Doc, CourseImage = Image, Status = Status
            )
            CourseSave.save()
            return redirect("course")
    except Exception as e:
        messages.warning(request, 'Your account expires in three days.')
        print("Oops!", e.__class__, "occurred.")
    if request.user.is_superuser:
        courses = Course.objects.all()
        paginator = Paginator(courses,10)
        try:
            page = int(request.GET.get('page',1))
        except:
            page = 1
        try:
            course = paginator.page(page)
        except(EmptyPage,InvalidPage):
            course = paginator.page(paginator.num_pages)
        print(course)
        branch = Branch.objects.all()
        sup = SupportingDoc.objects.all()
        context = {"course" : course,"branch" : branch,"sup" : sup}
        return render(request, "course.html", context)
    elif request.user.is_institute:
        course = Course.objects.filter(user=request.user.id)
        branch = Branch.objects.all()
        sup = SupportingDoc.objects.all()
        context = {"course" : course,"branch" : branch,"sup" : sup}
        return render(request, "course.html", context)

@csrf_exempt
def delete_branch(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = Branch.objects.get(id=id)
        if len(instance.Image) > 0:
            os.remove(instance.Image.path)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(branch)


@csrf_exempt
def delete_insitute_course(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = institutionCourse.objects.get(id=id)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(institutecourse)

@csrf_exempt
def delete_institutebranch(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = instituteBranch.objects.filter(id=id)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(instituteBranch)

@csrf_exempt
def delete_institutebanner(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = instituteBanner.objects.get(id=id)
        if len(instance.Image) > 0:
            os.remove(instance.Image.path)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(institutebanner)


@csrf_exempt
def delete_introbanner(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = introBanner.objects.get(id=id)
        if len(instance.Image) > 0:
            os.remove(instance.Image.path)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(introbanner)


@csrf_exempt
def delete_institute(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = Institution.objects.get(id=id)
        if len(instance.image) > 0:
            os.remove(instance.image.path)
        instance.delete()
        # userDelete = NewUser.objects.get(email = instance.contactPersonEmail) 
        print(instance)
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(institution)

@csrf_exempt
def delete_course(request):
    if request.method == "POST":
        id = request.POST["id"]
        print(id)
        instance = Course.objects.get(id=id)
        if len(instance.CourseImage) > 0:
            os.remove(instance.CourseImage.path)
        instance.delete()
        return redirect(branch)
        # data = true
        # return JsonResponse(data)
    return redirect(branch)


@csrf_exempt
def list_branch(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = Branch.objects.filter(id=id).values()
        Code = instance[0]['BranchCode']
        Name = instance[0]['BranchName']
        Image = instance[0]['Image']
        Status = instance[0]['Status']
        ID = instance[0]['id']
        print(Image)
        context = [ID,Code,Name,Image,Status]
        data = json.dumps(context)
        return HttpResponse(data)

@csrf_exempt
def list_staff(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = Staff.objects.filter(id=id).values()
        Name = instance[0]['name']
        fatehrName = instance[0]['fatehrName']
        email = instance[0]['email']
        phone = instance[0]['phone']
        dob = instance[0]['DOB']
        gender = instance[0]['gender']
        marital = instance[0]['maritalStatus']
        nationality = instance[0]['nationality']
        anuual_salary = instance[0]['annualSalary']
        designation = instance[0]['designation']
        branch = instance[0]['branchId']
        aadhaarNumber = instance[0]['aadhaarNumber']
        panNumber = instance[0]['panNumber']
        DateofJoin = instance[0]['DateofJoin']
        id = instance[0]['id']
        Image = instance[0]['image']        
        Status = instance[0]['Status']
        context = [Name,fatehrName,email,phone,dob,gender,marital,nationality,anuual_salary,designation,branch,aadhaarNumber,panNumber,DateofJoin,id,Image,Status]
        print(context)
        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()
        data = json.dumps(context,default = myconverter)
        return HttpResponse(data)

@csrf_exempt
def list_institute(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = Institution.objects.filter(id=id).values()
        print(instance)
        Name = instance[0]['name']
        State = instance[0]['stateID']
        City = instance[0]['cityId']
        Address = instance[0]['address']
        Chairman = instance[0]['chairmanName']
        Chairperson = instance[0]['contactPersonName']
        email = instance[0]['contactPersonEmail']
        phone = instance[0]['contactPersonPhone']
        image = instance[0]['image']
        Status = instance[0]['Status']
        ID = instance[0]['id']
        institutionCode = instance[0]['institutionCode']
        context = [ID,Name,State,City,Address,Chairman,Chairperson,email,phone,image,Status,institutionCode]
        data = json.dumps(context)
        return HttpResponse(data)


@csrf_exempt
def list_course(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = Course.objects.filter(id=id).values()
        Code = instance[0]['CourseCode']
        Name = instance[0]['CourseName']
        branch_id = instance[0]['Branch']
        duration = instance[0]['CourseDuration']
        desc = instance[0]['CourseDescription']
        Image = instance[0]['CourseImage']
        Status = instance[0]['Status']
        ID = instance[0]['id']
        context = [ID,Code,Name,branch_id,duration,desc,Image,Status]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)
    return HttpResponse("hello")


@csrf_exempt
def list_doc(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = SupportingDoc.objects.filter(id=id).values()
        Name = instance[0]['DocumentName']
        Status = instance[0]['Status']
        ID = instance[0]['id']
        context = [Name,Status,ID]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)
    return HttpResponse("hello")

@csrf_exempt
def list_planbanner(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = planBanner.objects.filter(id=id).values()
        Image = instance[0]['Image']
        Title = instance[0]['Title']
        Description = instance[0]['Description']
        Status = instance[0]['Status']
        ID = instance[0]['id']
        context = [ID,Image,Title,Description,Status]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)
    return HttpResponse("hello")

@csrf_exempt
def list_introbanner(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = introBanner.objects.filter(id=id).values()
        Image = instance[0]['Image']
        Title = instance[0]['Title']
        Description = instance[0]['Description']
        Status = instance[0]['Status']
        ID = instance[0]['id']
        context = [ID,Image,Title,Description,Status]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)
    return HttpResponse("hello")

@csrf_exempt
def list_institutebanner(request):
    if request.method == "POST":
        id = request.POST['id']
        instance = instituteBanner.objects.filter(id=id).values()
        Image = instance[0]['Image']
        Title = instance[0]['Title']
        Status = instance[0]['Status']
        ID = instance[0]['id']
        context = [ID,Image,Title,Status]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)
    return HttpResponse("hello")


@csrf_exempt 
def update_branch(request):

    if request.method == "POST":
        ID = request.POST['_id']
        code = request.POST['branch_code']
        Name = request.POST['branch_name']
        branch = Branch.objects.get(id = ID)
        status = request.POST['status']
        branch.BranchName = Name
        branch.BranchCode = code
        branch.Status = status
        branch.save()

    return redirect('branch')

@csrf_exempt 
def update_institute(request):

    if request.method == "POST":
        ID = request.POST['_id']
        branch = Institution.objects.get(id = ID)
        name = request.POST['institution_name']
        code = request.POST['institution_code']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']
        chairman_name = request.POST['chairman_name']
        contact_person_name = request.POST['contact_person_name']
        contact_person_email = request.POST['contact_person_email']
        contact_person_phone = request.POST['contact_person_phone']
        if len(request.FILES) != 0:
            if len(branch.image) > 0:
                os.remove(branch.image.path)
            branch.image = request.FILES['institution_image']
        status = request.POST['status']
        branch.institutionCode  = code
        branch.contactPersonEmail  = contact_person_email
        branch.name = name
        branch.stateID = state
        branch.cityId = city
        branch.address = address
        branch.chairmanName = chairman_name
        branch.contactPersonName = contact_person_name
        branch.contactPersonPhone = contact_person_phone
        branch.Status = status
        branch.save()
        # new = NewUser.objects.filter(email = contact_person_email)
    return redirect('institution')


@csrf_exempt     
def update_course(request):

    if request.method == "POST":
        ID = request.POST['id']
        ID = int(ID)
        branchid = request.POST['branch_id']
        branch = Course.objects.get(id = ID)
        code = request.POST['course_code']
        Name = request.POST['course_name']
        Duruation = request.POST['duration']
        description = request.POST['description']
        if len(request.FILES) != 0:
            if len(branch.CourseImage) > 0:
                os.remove(branch.CourseImage.path)
            branch.CourseImage = request.FILES['course_image']
        status = request.POST['status']
        branch.CourseName = Name
        branch.Branch = branchid
        branch.CourseDuration = Duruation
        branch.CourseDescription = description
        branch.CourseCode = code
        branch.Status = status
        branch.save()

    return redirect('course')

@csrf_exempt 
def update_doc(request):

    if request.method == "POST":
        ID = request.POST['_id']
        
        Name = request.POST['name']
        status = request.POST['status']
        doc = SupportingDoc.objects.get(id = ID)
        doc.DocumentName = Name
        doc.Status = status
        doc.save()

    return redirect('supporting_documents')


@login_required(login_url="login")
@csrf_exempt 
def supporting_documents(request):
    
    request.session['title'] = "Supporting Documents"
    if request.method == "POST":
        DocName = request.POST['name']
        Status = request.POST['status']
        sup_doc = SupportingDoc(DocumentName = DocName, Status = Status)
        sup_doc.save()
        return redirect(supporting_documents)
    sup_document = SupportingDoc.objects.all()
    paginator = Paginator(sup_document,10)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        sup_doc = paginator.page(page)
    except(EmptyPage,InvalidPage):
        sup_doc = paginator.page(paginator.num_pages)
    return render(request,"supporting-document.html",{'sup_doc': sup_doc})

@csrf_exempt
def delete_supporting_doc(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = SupportingDoc.objects.filter(id=id)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(supporting_documents)

@login_required(login_url="login")
@csrf_exempt
def introbanner(request):    
    request.session['title'] = "Intro Banner"
    if request.method == "POST":
        userid = request.user.id
        Image = request.FILES['intro_banner_image']
        Title = request.POST['title']
        Desc = request.POST['description']
        status = request.POST['status']
        introsave = introBanner(user = userid, Title = Title, Description = Desc, Status = status, Image = Image)
        introsave.save()
        return redirect(introbanner)
    
    intro  = introBanner.objects.all()
    return render(request,"intro-banner.html",{'intro': intro})


@login_required(login_url="login")
@csrf_exempt
def planbanner(request):
    request.session['title'] = "Plan Banner"
    if request.method == "POST":
        userid = request.user.id
        Image = request.FILES['intro_banner_image']
        Title = request.POST['title']
        Desc = request.POST['description']
        status = request.POST['status']
        plansave = planBanner(user = userid, Title = Title, Description = Desc, Status = status, Image = Image)
        plansave.save()
        return redirect(planbanner)
    
    plan  = planBanner.objects.all()
    return render(request,"plan-banner.html",{'plan': plan})

@login_required(login_url="login")
@csrf_exempt
def institutebanner(request):
    request.session['title'] = "Institute Banner"
    if request.method == "POST":
        userid = request.user.id
        Image = request.FILES['banner_image']
        Title = request.POST['title']
        status = request.POST['status']
        institutesave = instituteBanner(user = userid, Title = Title,Status = status, Image = Image)
        institutesave.save()
        return redirect(institutebanner)
    if request.user.is_superuser:
        institute  = instituteBanner.objects.all()
        return render(request,"institute-banner.html",{'institute': institute})
    if request.user.is_institute:
        institute  = instituteBanner.objects.filter(user=request.user.id)
        return render(request,"institute-banner.html",{'institute': institute})


@csrf_exempt
def delete_planbanner(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = planBanner.objects.get(id=id)
        if len(instance.Image) > 0:
            os.remove(instance.Image.path)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(planbanner)

@login_required(login_url="login")
@csrf_exempt
def profile(request):
    if request.method == "POST":
        ID = request.POST['_id']
        brochure = request.FILES['brochure']
        name = request.POST['name']
        address = request.POST['address']
        chairman_name = request.POST['chairman_name']
        contact_person_name = request.POST['contact_person_name']
        contact_person_email = request.POST['contact_person_email']
        contact_person_phone = request.POST['contact_person_phone']
        description = request.POST['description']
        institution_image = request.FILES['institution_logo']
        status = request.POST['status']
        branch = Institution.objects.get(id = ID)
        branch.contactPersonEmail  = contact_person_email
        branch.name = name
        branch.address = address
        branch.chairmanName = chairman_name
        branch.contactPersonName = contact_person_name
        branch.contactPersonPhone = contact_person_phone
        branch.image = institution_image
        branch.Status = status
        branch.description = description
        branch.brochure = brochure
        branch.save()
        return redirect('profile')

    user = Institution.objects.get(id=request.user.id)
    print(user)
    return render(request,'profile.html',{'user':user})


@csrf_exempt
def update_planbanner(request):
    if request.method == "POST":
        ID = request.POST['id']
        ID = request.POST['id']
        Image = request.FILES['intro_banner_image']
        Title = request.POST['title']
        Description = request.POST['description']
        status = request.POST['status']
        branch = planBanner.objects.get(id = ID)
        if len(request.FILES) != 0:
            if len(branch.Image) > 0:
                os.remove(branch.Image.path)
            branch.Image = Image
        branch.Title= Title
        branch.Description = Description
        branch.Status = status
        branch.save()
        return redirect(planbanner)
    return redirect(planbanner)

@csrf_exempt
def update_introbanner(request):
    if request.method == "POST":
        ID = request.POST['id']
        Image = request.FILES['intro_banner_image']
        Title = request.POST['title']
        Description = request.POST['description']
        status = request.POST['status']
        branch = introBanner.objects.get(id = ID)
        if len(request.FILES) != 0:
            if len(branch.Image) > 0:
                os.remove(branch.Image.path)
            branch.Image = Image
        branch.Title= Title
        branch.Description = Description
        branch.Status = status
        branch.save()
        return redirect(introbanner)
    return redirect(introbanner)
    
@csrf_exempt
def update_institutebanner(request):
    if request.method == "POST":
        ID = request.POST['id']
        Image = request.FILES['banner_image']
        Title = request.POST['title']
        status = request.POST['status']
        branch = instituteBanner.objects.get(id = ID)
        if len(request.FILES) != 0:
            if len(branch.Image) > 0:
                os.remove(branch.Image.path)
            branch.Image = Image
        branch.Title= Title
        branch.Status = status
        branch.save()
        return redirect(institutebanner)
    return redirect(institutebanner)

@login_required(login_url="login")
@csrf_exempt
def college(request):
    request.session['title'] = "Colleges"
    if request.method == "POST":
        name = request.POST['institution_name']
        adddress = request.POST['address']
        chairmanName = request.POST['chairman_name']
        contactPersonName = request.POST['contact_person_name']
        contactPersonEmail = request.POST['contact_person_email']


        return redirect('college')
    if request.user.is_superuser:
        users = Institution.objects.all
        return render(request,"college.html",{'users': users})
    elif request.user.is_institute:
        users = Institution.objects.filter(user = request.user.id)
        return render(request,'college.html',{'users':users})
    else:
        return redirect('dashboard')


@login_required(login_url="login")
@csrf_exempt
def staff(request):    
    request.session['title'] = "Staff"
    try:
        if request.method == "POST":
            image = request.FILES['staff_image']
            name = request.POST['name']
            father_name = request.POST['father_name']
            email = request.POST['email']
            phone = request.POST['phone']
            dob = request.POST['dob']
            gender = request.POST['gender']
            marital_status = request.POST['marital_status']
            nationality = request.POST['nationality']
            annual_salary = request.POST['annual_salary']
            designation = request.POST['designation']
            branch = request.POST['branch']
            aadhaar_number = request.POST['aadhaar_number']
            pan_number = request.POST['pan_number']
            join_date = request.POST['join_date']
            status = request.POST['status']        
            randompass = NewUser.objects.make_random_password()
            print(randompass)
            userreg = NewUser(email = email,is_institute_staff = True,is_active =True) 
            userreg.set_password(randompass)     
            userreg.save()
            subject = 'welcome to Eduvy'
            message = f'Hi, thank you for registering in Eduvy.Your Password is {randompass}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )
            staffSave = Staff(
                institutionID = request.user.id,
                image = image,
                name = name,
                fatehrName = father_name,
                nationality= nationality,
                email = email,
                phone = phone,
                DOB= dob,
                gender = gender,
                maritalStatus = marital_status,
                annualSalary = annual_salary, 
                designation = designation, 
                branchId = branch, 
                aadhaarNumber = aadhaar_number, 
                panNumber = pan_number,
                DateofJoin = join_date,
                Status = status)
            staffSave.save()
            return redirect('staff')
    except Exception as e:
        messages.warning(request, 'Some Error Occured')
        print("Oops!", e.__class__, "occurred.")
    if request.user.is_superuser:
        staff = Staff.objects.all()
        branch = Branch.objects.all()
        context = {'staff':staff,'branch':branch}
        return render(request,'staff.html',context)
    elif request.user.is_institute:
        staff = Staff.objects.filter( institutionID = request.user.id)
        print(staff)
        branch = Branch.objects.all()
        context = {
            'staff':staff,
            # 'branch':branch
            }
        return render(request,'staff.html',context)

@login_required(login_url="login")
@csrf_exempt
def institute_branch(request):
    if request.method == 'POST':
        branchCode = request.POST['branch_code']
        branch = request.POST['branch']
        status = request.POST['status']
        userid =  request.user.id
        instiid = Institution.objects.get( user = userid)        
        instbranch = instituteBranch(institutionId = instiid.id,branchCode = branchCode,branchId = branch,Status=status)
        instbranch.save()
        return redirect('institute_branch')
    if request.user.is_superuser:
        instibranch = instituteBranch.objects.all()        
        branch = Branch.objects.all()
        context = {'branch':branch,'insti':instibranch}
        return render(request,'institute-branch.html',context)
    if request.user.is_institute:        
        userid =  request.user.id
        instiid = Institution.objects.get( user = userid) 
        instibranch = instituteBranch.objects.filter(institutionId = instiid.id)        
        branch = Branch.objects.all()
        context = {'branch':branch,'insti':instibranch}
        return render(request,'institute-branch.html',context)

@csrf_exempt
def list_institute_branch(request):
    if request.method == 'POST':
        id  = request.POST['id']
        instance = instituteBranch.objects.filter(id = id).values()
        # instiID = instance[0]['institutionId']
        Code = instance[0]['branchCode']
        print(instance[0]['branchId'])
        Branch = instance[0]['branchId']
        # Branch = "hello"
        Status = instance[0]['Status']
        ID = instance[0]['id']
        # print(Image)
        context = [ID,Code,Branch,Status]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)


@csrf_exempt
def list_institute_course(request):
    if request.method == "POST":
        id = request.POST['id']
        courses = institutionCourse.objects.filter(id = id).values()
        code = courses[0]['courseCode']
        branch = courses[0]['branchId']
        course = courses[0]['courseId']
        fee = courses[0]['courseFee']
        ID = courses[0]['id']
        status = courses[0]['Status']
        print(status)
        context = [code,branch,course,fee,ID,status]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)

@csrf_exempt
def update_institutebranch(request):
    if request.method == "POST":
        ID = request.POST['id'] 
        code = request.POST['branch_code']
        Branch = request.POST['branch']
        status = request.POST['status']
        branch = instituteBranch.objects.get(id = ID)
        branch.branchId = Branch
        branch.branchCode = code
        branch.Status = status
        branch.save()

    return redirect(institute_branch)

@csrf_exempt
def update_institute_course(request):
    if request.method == "POST":
        ID = request.POST['id']
        branch = institutionCourse.objects.get(id = ID)
        code = request.POST['course_code']
        branch = request.POST['branch']
        course = request.POST['course']
        fee = request.POST['fee']
        status = request.POST['status']
        # branch.BranchName = Name
        branch.courseCode = code
        branch.courseFee = fee
        # branch.Image = Image
        branch.Status = status
        branch.save()

    return redirect(institutecourse)

@login_required(login_url="login")
@csrf_exempt
def institutecourse(request):
    try:
        if request.method == 'POST':
            code = request.POST['course_code']
            branch = request.POST['branch']
            course = request.POST['course']
            fee = request.POST['fee']
            status = request.POST['status']
            userid =  request.user.id
            instiid = Institution.objects.get( user = userid)      
            course = institutionCourse.objects.create(institutionId = instiid.id,courseCode = code,courseFee = fee, branchId = branch, courseId = course, Status = status)
            course.save()
            return redirect(institutecourse)
    except Exception as e:
        print(str(e))
    if request.user.is_superuser:
        insticourse = institutionCourse.objects.all()
        course = Course.objects.all()
        branch = Branch.objects.all()
        return render(request,'institute-course.html',{'insticoures':insticourse,'branch':branch,'course':course})
    elif request.user.is_institute :        
        userid =  request.user.id
        instiid = Institution.objects.get( user = userid) 
        insticourse = institutionCourse.objects.filter(institutionId = instiid.id)
        instibranch = instituteBranch.objects.filter(institutionId = instiid.id).values()
        branch = Branch.objects.all()
        print(instibranch)
        course = Course.objects.all()
        return render(request,'institute-course.html',{'insticoures':insticourse,'branch':branch,'instibranch':instibranch,'course':course})

@csrf_exempt
def list_institute_branch_courses(request):
    if request.method == "POST":
        # branchId = request.POST['branchId']
        # print(branchId)
        # b = instituteBranch.objects.get(id = branchId)
        # print(b)
        # bran = b[0]['branchId']
        print('-------------------------------------------------------------------------')
        # c = Course.objects.filter(id=id).values()
        # course= []
        # for data in c:
        #     courseid  = data[0]['id']
        #     CourseName = data[0]['CourseName']
        #     c = {"id" : courseid,"name" : CourseName}
        #     course.append(c)

        # data = json.dumps(course)
        # return HttpResponse("hello")

        branch = request.POST['branchId']
        branch = int(branch) 
        print(branch)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        # Database Name
        db = client["eduvytest"]
        
        # Collection Name
        con = db["Courses"]
        myquery = { "Branch": branch }
        x = con.find(myquery)
        print(x)
        course= []
        for data in x:
            courseid  = data['id']
            print("hello")
            courseName = data['CourseName']
            c = {"id" : courseid,"course" : courseName}
            course.append(c)
        print(course)
        data = json.dumps(course)
        
        return HttpResponse(data)


@login_required(login_url="login")
@csrf_exempt
def students(request):
    try:
        if request.method == "POST":
            batch = request.POST['batch']
            batch_section = request.POST['batch_section']
            course_id = request.POST['course_id'] 
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            guardian_name = request.POST['guardian_name']
            guardian_phone = request.POST['guardian_phone']
            guardian_phone = request.POST['guardian_phone']
            print(course_id)
            course = institutionCourse.objects.get(courseId = course_id)
            print(course)
            course_code = course.courseCode
            branch_id = course.branchId
            admission = course.admissionid
            admission = admission + 1
            print(admission)
            course.admissionid = admission
            course.save()
            branch = Branch.objects.get(id = branch_id)
            print(branch)
            branch_code = branch.BranchCode
            institutionId = branch.user
            userid =  request.user.id
            instiid = Institution.objects.get( user = userid)
            print(instiid)
            institutioncode = instiid.institutionCode
            studentid = str(institutioncode) + str(batch) + str(branch_code) + str(course_code) + str(admission)
            print(studentid)
            randompass = NewUser.objects.make_random_password()
            print(123)
            userreg = NewUser(email = email,is_student = True,is_active =True) 
            userreg.set_password(123)  #change this at the time of deployment   
            userreg.save()
            subject = 'welcome to Eduvy'
            message = f'Hi, thank you for registering in Eduvy.Your Password is {randompass}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            # send_mail( subject, message, email_from, recipient_list )
            student = Students(batch = batch,batchSection=batch_section,studentID=studentid,institutionId=instiid.id,name=name,email=email,branchId= branch_id,courseId = course_id,phone = phone,address =address,guardianName = guardian_name,guardianPhone = guardian_phone)
            print(student)
            student.save()
            return redirect(students)
    except Exception as e:
        print(str(e))
    if request.user.is_superuser:
        course = Course.objects.all()
        student = Students.objects.all()
        context = {'course':course,'student':student}
        return render(request,'students.html',context)
    if request.user.is_institute:
        institution = Institution.objects.get(user = request.user.id)
        insticourse = institutionCourse.objects.filter(institutionId = institution.id)
        course = Course.objects.all()
        print(course)
        userid =  request.user.id
        instiid = Institution.objects.get( user = userid)
        student = Students.objects.filter(institutionId = instiid.id)
        context = {'course':course,'student':student,'insticourse':insticourse}
        return render(request,'students.html',context)

@csrf_exempt
def list_course_duration(request):
    if request.method == "POST":
        cid = request.POST['course']
        course = Course.objects.filter(id = cid).values()
        courseduration = course[0]['CourseDuration']
        data = json.dumps(courseduration)
        
        return HttpResponse(data)


@csrf_exempt
def list_student(request):
    if request.method == "POST":
        id = request.POST['id']
        student = Students.objects.get(id = id)
        batch = student.batch
        batchSection = student.batchSection
        name = student.name
        email = student.email
        guardianName = student.guardianName
        guardianPhone = student.guardianPhone
        address = student.address
        courseId = student.courseId
        studentID = student.id
        context = [batch,batchSection,name,email,guardianName,str(guardianPhone),address,courseId,studentID]
        print(context)
        data = json.dumps(context)
        return HttpResponse(data)

        

@csrf_exempt
def delete_student(request):
    if request.method == "POST":
        id = request.POST["id"]
        instance = Students.objects.filter(id=id)
        instance.delete()
        # return redirect(branch)
        data = {
        'is_taken': "deleted"
        }
        return JsonResponse(data)
    return redirect(students)

import datetime
from json import JSONEncoder

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

@csrf_exempt
def search_branch(request):
    if request.method == "POST":
        searched = request.POST['search']
        bran = Branch.objects.filter(BranchName__icontains=searched).values()
        length = len(list(bran))
        # print(length)
        branch = []
        for i in range(0,length):
            b = list(bran)[i]
            branch.append(b)
        # data = json.dumps(bran)
        # print(branch)
        # print(list(bran))
        # return JsonResponse(branch)
        data = json.dumps(branch,indent=4, cls=DateTimeEncoder)
        return HttpResponse(data)

    # return render(request,'demo.html')  