from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core.validators import MinLengthValidator

class EmployeeModelManager(BaseUserManager):

    def create_user(self, pin, first_name, last_name, permission_level,  password=None,**extra_fields):
        if not pin:
            raise ValueError("You must provide pin")
        user = self.model(
            pin=pin,
            permission_level=permission_level,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, pin,first_name,last_name, permission_level, password=None, **extra_fields):
        user = self.create_user(
            pin=pin,
            permission_level=permission_level,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_unusable_password()
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser):

    MANAGER = 1
    SUPERVISER = 2
    EMPLOYEE = 3
    AUTHORIZATION = (
        (MANAGER, 'Manager'),
        (SUPERVISER, 'Superviser'),
        (EMPLOYEE, 'Employee')
    )

    # Person related fields
    first_name          = models.CharField(max_length=20)
    second_name         = models.CharField(blank=True, max_length=20)
    last_name           = models.CharField(max_length=20)
    date_of_birth        = models.DateField(blank=True, null=True)
    address             = models.CharField(max_length=60, blank=True)
    tel_number          = models.CharField(blank=True, max_length=12)
    email               = models.EmailField(blank=True)

    # Job related fields
    position            = models.CharField(blank=False, max_length=20)
    hourly_pay_rate     = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    start_date          = models.DateField(blank=True, null=True,)
    end_date            = models.DateField(blank=True, null=True,)
    is_employeed        = models.BooleanField(blank=True, null=True,)
    nin                 = models.CharField(max_length=9, blank=True, null=True, unique=True)
    permission_level    = models.IntegerField(choices=AUTHORIZATION, default=EMPLOYEE)
    profile_picture     = models.ImageField(upload_to='staticfiles/img/employee_profile_picture/', default='staticfiles/img/employee_profile_picture/default.png')
    pin                 = models.IntegerField('Pincode', unique=True)
    password            = models.CharField(blank=True, max_length=100)

    
    # REQUIRED for AbstractBaseUser class
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = EmployeeModelManager()

    USERNAME_FIELD = 'pin'
    REQUIRED_FIELDS = ['first_name', 'last_name','permission_level']

    # Returns the full name of an employee
    def get_full_name(self):
        full_name = f"{self.first_name} {self.second_name} {self.last_name}"
        return full_name.strip() 

    # Returns the short name of an employee
    def get_short_name(self):
        
        return self.first_name
    
    def email_employee(self, subject, message, from_email=None, **kwargs):
        #Sends an email to this Employee
        send_mail(subject, message, from_email, [self.email], **kwargs)

    
    # Required functions for custom users
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.first_name


