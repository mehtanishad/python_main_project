from django.db import models


Select_Role = (
    ('T', 'Teacher'),
    ('S', 'Student'),
)

# Create your models here.
class Role(models.Model):
    # Role_Type = models.CharField(max_length=8,default=str())
    Role_Type = models.CharField(max_length=5, choices=Select_Role, default=str(), blank=True)
     
    class Meta:
        db_table="role"

    def __str__(self) -> str:
        return self.Role_Type

# Create your models here.
class Master(models.Model):
    Email=models.EmailField(unique=True)
    Password=models.CharField(max_length=50, default=str())
    IsActive=models.BooleanField(default=False)

    class Meta:
        db_table="master"

    def __str__(self) -> str:
        return self.Email

class Common(models.Model):
    Master=models.ForeignKey(Master, on_delete=models.CASCADE)

    Name=models.CharField(max_length=50)
    DateOfBirth=models.DateField(default='2022-11-21')
    DateOfJoining=models.DateField(default='2022-11-21')
    Address=models.CharField(max_length=100)

    class Meta:
        db_table="common"

    def __str__(self) -> str:
        return self.Name if self.Name else self.Master.Email


class Student(models.Model):
    Common=models.ForeignKey(Common, on_delete=models.CASCADE)

    Roll_Number=models.CharField(max_length=20)

    class Meta:
        db_table="student"

    def __str__(self) -> str:
        return self.Common.Name if self.Common.Name else self.Common.Master.Email

class Teacher(models.Model):
    Common=models.ForeignKey(Common, on_delete=models.CASCADE)

    Compensation=models.CharField(max_length=10)

    class Meta:
        db_table="teacher"
    
    def __str__(self) -> str:
        return  self.Common.Name if self.Common.Name else self.Common.Master.Email


class Club(models.Model):
    Club_Name=models.CharField(max_length=50)
    Open_Time=models.CharField(max_length=50,default='10:00 AM')
    Close_Time=models.CharField(max_length=50,default='04:00 PM')
    Head_Of_Club=models.CharField(max_length=50,default=str())
    Contact=models.CharField(max_length=10,default=str())
    
    class Meta:
        db_table = 'club'

    def __str__(self) -> str:
        return self.Club_Name


class Book(models.Model):
    Book_Name=models.CharField(max_length=40)
    Author_Name=models.CharField(max_length=40)
    Price=models.CharField(max_length=40)
    Time_Period=models.CharField(max_length=40)

    class Meta:
        db_table = 'book'

    def __str__(self) -> str:
        return self.Book_Name




class Department(models.Model):
    Depart_Name=models.CharField(max_length=40)
    HeadOfDepart=models.CharField(max_length=40)
    Total_Faculty=models.CharField(max_length=20)

    class Meta:
        db_table='department'
    
    def __str__(self)-> str:
        return self.Depart_Name

class Event(models.Model):
    Event_Name=models.CharField(max_length=40)
    Event_Date=models.DateField(default='2022-11-21')
    Event_Time=models.CharField(max_length=10)
    Chief_Guest=models.CharField(max_length=20)

    class Meta:
        db_table='event'
    
    def __str__(self)-> str:
        return self.Event_Name