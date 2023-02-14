from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('signin_page/', signin_page, name='signin_page'),
    path('', signup_page, name='signup_page'),
    path('profile_page/', profile_page, name='profile_page'),
    path('profile_data/',profile_data,name='profile_data'),
    path('profile_update/',profile_update,name='profile_update'),
    path('forgot_pwd_page/',forgot_pwd_page,name='forgot_pwd_page'),
    path('otp_page/',otp_page,name='otp_page'),
    path('profile_page_teacher/',profile_page_teacher,name='profile_page_teacher'),
    path('student_page/',student_page,name='student_page'),
    path('teacher_page/',teacher_page,name='teacher_page'),
    # path('club_page/',club_page,name='club_page'),
    path('book_page/',book_page,name='book_page'),
    # path('add_book_page/',add_book_page,name='add_book_page'),
    # path('club_page_data/',club_page_data,name='club_page_data'),
    path('add_club_page/',add_club_page,name='add_club_page'),
    path('add_club/',add_club,name='add_club'),
    path('club_page/',club_page,name='club_page'),
    path('update_profile_page/',update_profile_page,name='update_profile_page'),
    path('department_page/',department_page,name='department_page'),
    path('event_page/',event_page,name='event_page'),
    path('maintenance_page/',maintenance_page,name='maintenance_page'),



    path('profile_data_2/',profile_data_2,name='profile_data_2'),
    path('profile_update_teacher/',profile_update_teacher,name='profile_update_teacher'),
    path('password_reset/', password_reset, name='password_reset'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('otp_creation/', otp_creation, name='otp_creation'),
    path('otp_send/', otp_send, name='otp_send'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('student_page_data/', student_page_data, name='student_page_data'),
    path('teacher_page_data/', teacher_page_data, name='teacher_page_data'),
    # path('club_data/', club_data, name='club_data'),
    path('book_page_data/', book_page_data, name='book_page_data'),
    path('add_book_data/', add_book_data, name='add_book_data'),
    path('add_data/',add_data,name='add_data'),
    path('delete_account_function/',delete_account_function,name='delete_account_function'),
    path('update_profile_function/',update_profile_function,name='update_profile_function'),

    path('club_delete/<str:club_name>',club_delete,name='club_delete'),
    path('book_delete/<str:book_name>',book_delete,name='book_delete'),

     path('add_event/',add_event,name='add_event'),
    path('add_department/',add_department,name='add_department'),
    path('event_data/',event_data,name='event_data'),
    path('department_data/',department_data,name='department_data'),  
     
     
]
