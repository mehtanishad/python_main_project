from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from random import randint
import os
import random

# Create your views here.
data={}
def index(request):
    return render(request,'index.html',data)

def signin_page(request):
    return render(request,'signin_page.html')

def signup_page(request):
    return render(request,'signup_page.html')

def forgot_pwd_page(request):
    return render(request,'forgot_pwd_page.html')

def otp_page(request):
    return render(request,'otp_page.html')

def maintenance_page(request):
    return render(request,'maintenance_page.html')

def profile_page_teacher(request):
    return render (request,'profile_page_teacher.html',data)

def update_profile_page(request):
    return render(request,'update_profile_page.html')


def student_page(request):
    if 'email' in request.session:
        student_page_data(request) #load student data
        return render(request,'student_page.html', data)
    return render(request,'student_page.html')


def teacher_page(request):
    if 'email' in request.session:
        teacher_page_data(request) #load student data
        return render(request,'teacher_page.html', data)
    return render(request,'teacher_page.html')


# def club_page(request):
# #     if 'email' in request.session:
#     club_page_data(request) #load student data
#     return render(request,'club_page.html', data)
#     return render(request,'club_page.html')

def add_data(request):
    return render(request,'add_data.html')

def department_page(request):
    department_data(request)
    return render(request,'department_page.html', data)
    
def event_page(request):
    event_data(request)
    return render(request,'event_page.html', data)

def book_page(request):
    # if 'email' in request.session:
    book_page_data(request) #load student data
    return render(request,'book_page.html', data)
    # return render(request,'book_page.html')



def add_club_page(request):
    return render(request,'add_club_page.html')


def club_page(request):
    club_data(request) #load club data
    return render(request,'club_page.html', data)


#club data
def club_data(request):
    print(request.POST)
    club = Club.objects.all()
    data['club'] = club


# Add club's    
def add_club(request):
    print(request.POST)
    
    Club.objects.create(
        Club_Name=request.POST['club_name'],
        Open_Time=request.POST['open_time'],
        Close_Time=request.POST['close_time'],
        Head_Of_Club=request.POST['head_of_club'],
        Contact=request.POST['contact']
        )

    print('successfully')
    return redirect(club_page)


def profile_page(request):
    print(request.session['email'])
    if 'email' in request.session:
        try:
            try:
                profile_data(request)
                return render(request,'profile_page.html',data)
            except:
                profile_data_2(request)
                return redirect(profile_page_teacher)
        except Exception as err:
            print("data not availabe ! submit your data admin side & relogin")
    return redirect(update_profile_page)

#signup_functionality
def signup(request):
    print(request.POST)
    password = request.POST['password']
    if password == request.POST['confirm_password']:
        master = Master.objects.create(Email = request.POST['email'],Password = password)
        role=Role.objects.create(Role_Type = request.POST['role_type'])
        common=Common.objects.create(Master = master)
        print('Signup successfully.')
        if role.Role_Type == 'student':
            print('Student')
            Student.objects.create(Common=common)
        else:
            print('teacher')
            Teacher.objects.create(Common=common)
    else:
        print('both password should be same.')
        return redirect(signup_page)

    return redirect(signin_page)


# signin functionality
def signin(request):
    print(request.POST)
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.Password == request.POST['password']:
            request.session['email'] = master.Email
            return redirect(profile_page)

        else:
            return render(request, "signin_page.html",{'error':"Password does not match"})
    except Master.DoesNotExist as err:
        return render(request,"signin_page.html",{'error':"User does not Exists Please SignUp"})

main_path = settings.MEDIA_ROOT

# load profile data
def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = Common.objects.get(Master = master)
    user_roll = Student.objects.get(Common=user_profile)

    user_profile.first_name = user_profile.Name.split()[0]
    user_profile.last_name = user_profile.Name.split()[1]
    user_roll.roll_number = user_roll.Roll_Number


    user_profile.DateOfBirth = user_profile.DateOfBirth.strftime("%Y-%m-%d")
    user_profile.DateOfJoining = user_profile.DateOfJoining.strftime("%Y-%m-%d")

    data['user_data'] = user_profile
    data['roll_user'] = user_roll
    
    return redirect(profile_page)

main_path = settings.MEDIA_ROOT

# profile update functionality
def profile_update(request):
    print(request.POST)
    master = Master.objects.get(Email = request.session['email'])
    user_profile = Common.objects.get(Master = master)
    user_roll = Student.objects.get(Common=user_profile)
    # teacher = Teacher.objects.get(Common=user_profile)

    user_profile.Name =' '.join([request.POST['first_name'], request.POST['last_name']])
    user_profile.DateOfBirth = request.POST['dateofbirth']
    user_profile.DateOfJoining = request.POST['dateofjoining']
    user_profile.Address = request.POST['address']
    user_roll.Roll_Number = request.POST['roll_number']
     
    file_path = os.path.join(main_path, 'profiles')


    user_profile.save()
    user_roll.save()

    return redirect(profile_page)


# logout functionality
def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return redirect(signin_page)
    
    return redirect(profile_page)


# Profile Change Password functionality
def password_reset(request):
    master = Master.objects.get(Email = request.session['email'])
    if master.Password == request.POST['current_password']:
        if request.POST['new_password'] == request.POST['confirm_password']:
            master.Password = request.POST['new_password']
            master.save()
            return redirect(signin_page)
        else:
            print('both password should be same.')
            return redirect(profile_page)
    else:
        print('password does not matched.')
    return redirect(profile_page)



# forgot password
def forgot_password(request):
	if request.method=="POST":
		try:
			master = Master.objects.get(Email=request.POST['email'])
                        
			subject = 'OTP for forgot Password'
			otp=random.randint(1000,9999)
			message = f'Hi {master.Email}, Your OTP : '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [master.Email,]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'verify_otp.html',{'email':master.Email,'otp':otp})
		except:
			msg="Your are Not a register User !!!"
			return render(request,'forgot_pwd_page.html',{'msg':msg})
	else:
		return render(request,'forgot_pwd_page.html')



def verify_otp(request):
	if request.method=="POST":
		email=request.POST['email']
		otp=request.POST['otp']
		uotp=request.POST['uotp']

		print(">>>>>>>>OTP : ",otp)
		print(">>>>>>>>UOTP : ",uotp)
		print(">>>>>>>>Email : ",email)
		if uotp==otp:
			return render(request,'create_pwd.html', {'email':email})
		else:
			msg="OTP Does not Matched !!!"
			return render(request,'verify_otp.html',{'msg':msg})
	else:
		return render(request,'verify_otp.html')


def create_pwd(request):
     if request.method=="POST":
        try:
            master=Master.objects.get(Email = request.POST['Email'])
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>Here : ",master)
            if request.POST['new_pwd'] == request.POST['confirm_pwd']:
                master.Password = request.POST['new_pwd']
                master.save()
                return redirect(signin_page)
            else:
                msg="New Password & Confirm Password Does not Matched !!"
                return render(request,'create_pwd.html',{'msg':msg})
        except:
            msg2="User Not Exist Please SignUp !!!"
            return render(request,'create_pwd.html',{'msg2':msg2})
     else:
             return render(request,'create_pwd.html')


# profile update functionality
def profile_update_teacher(request):
    print(request.POST)
    master = Master.objects.get(Email = request.session['email'])
    user_profile = Common.objects.get(Master = master)
    teacher=Teacher.objects.get(Common=user_profile)

    user_profile.Name =' '.join([request.POST['first_name'], request.POST['last_name']])
    user_profile.DateOfBirth = request.POST['dateofbirth']
    user_profile.DateOfJoining = request.POST['dateofjoining']
    user_profile.Address = request.POST['address']
    teacher.Compensation=request.POST['compensation']
    

    user_profile.save()
    teacher.save()
    return redirect(profile_page)


# profile_update_teacher
def profile_data_2(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = Common.objects.get(Master = master)
    teacher=Teacher.objects.get(Common=user_profile)

    user_profile.first_name = user_profile.Name.split()[0]
    user_profile.last_name = user_profile.Name.split()[1]
    teacher.compensation=teacher.Compensation

    user_profile.DateOfBirth = user_profile.DateOfBirth.strftime("%Y-%m-%d")
    user_profile.DateOfJoining = user_profile.DateOfJoining.strftime("%Y-%m-%d")

    data['user_data'] = user_profile
    data['teacher_data']=teacher
    
    return redirect(profile_page_teacher)


#student data
def student_page_data(request):
    print(request.POST)
    student = Student.objects.all()
    # print(student)
    data['student'] = student
    # return redirect(student)


#teacher data
def teacher_page_data(request):
    print(request.POST)
    teacher = Teacher.objects.all()
    data['teacher'] = teacher



#book data
def book_page_data(request):
    print(request.POST)
    book = Book.objects.all()
    data['book'] = book


# Add Book's    
def add_book_data(request):
    print(request.POST)
    
    Book.objects.create(
        Book_Name=request.POST['book_name'],
        Author_Name=request.POST['author_name'],
        Price=request.POST['price'],
        Time_Period=request.POST['time_period']
        )
    # book.save()
    print('successfully')
    return redirect(book_page)



# Add department    
def add_department(request):
    print(request.POST)
    
    Department.objects.create(
        Depart_Name=request.POST['depart_name'],
        HeadOfDepart=request.POST['headofdepart'],
        Total_Faculty=request.POST['total_faculty'],
        )

    print('successfully')
    return redirect(department_page)

#department data
def department_data(request):
    # print(request.POST)
    department = Department.objects.all()
    data['department'] = department


# Add Event  
def add_event(request):
    print(request.POST)
    
    Event.objects.create(
        Event_Name=request.POST['event_name'],
        Event_Date=request.POST['event_date'],
        Event_Time=request.POST['event_time'],
        Chief_Guest=request.POST['chief_guest'],
        )

    print('successfully')
    return redirect(event_page)


#event data
def event_data(request):
    # print(request.POST)
    event = Event.objects.all()
    data['event'] = event


# Delete account Functionality
def delete_account_function(request):
    print(request.POST)
    master=Master.objects.get(Email = request.session['email'])
    master.delete()
    return redirect(signup_page)

def update_profile_function(request):
    print(request.POST)
    master = Master.objects.get(Email = request.session['email'])
    common= Common.objects.get(Master = master)

    common.Name = ' '.join([request.POST['first_name'], request.POST['last_name']])
    common.DateOfBirth = request.POST['dateofbirth']
    common.DateOfJoining = request.POST['dateofjoining']
    common.Address = request.POST['address']

    common.save()
    return redirect(signin_page)



def club_delete(request,club_name):
    print(request.POST)
    club=Club.objects.filter(Club_Name=club_name)
    club.delete()
    return redirect(club_page)

def book_delete(request,book_name):
    print(request.POST)
    book=Book.objects.filter(Book_Name =book_name)
    book.delete()
    return redirect(book_page)