from django.db import models
from django.core.mail send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core.validators import MinLengthValidator


class Employee(AbstractBaseUser):
    # A person related fields
    first_name          = models.CharField()
    second_name         = models.CharField()
    last_name           = models.CharField()
    date_of_bith        = models.DateField(blank=True)
    address             = models.CharField(blank=True)
    tel_number          = models.CharField(blank=True)
    email               = models.EmailField(blank=True, unique=True)

    # Job related fields
    position            = models.CharField(blank=False)
    hourly_pay_rate     = models.DecimalField(decimal_places=2)
    start_date          = models.DateField()
    end_date            = models.DateField(null=True)
    is_employeed        = models.BooleanField()
    nin                 = models.CharField(max_length=9, unique=True)
    is_manager          = models.BooleanField(blank=False)
    is_supervisor       = models.BooleanField(blank=False)
    is_employee         = models.BooleanField(blank=False)
    profile_picture     = models.ImageField(upload_to='employee_profile_picture/', default='employee_profile_picture/default.png')
    pin                 = models.IntegerField('Pincode', max_length=4, validators=[MinLengthValidator(4)], unique=True)


    '''
    REQUIRED for AbstractBaseUser class
    '''
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = EmployeeModelManager()

    USERNAME_FIELD = 'pin'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_manager', 'is_supervisor', 'is_employee']

    class Meta:
        verbose_name = _('emplpyee')
        verbose_name_plural = _('employees')

    def get_full_name(self):
        '''
        Returns the full name of an employee
        '''
        full_name = f"{self.first_name} {self.second_name} {self.last_name}"
        return first_name.strip() 

    def get_short_name(self):
        '''
        Returns the short name of an employee
        '''
        return self.first_name
    
    def email_employee(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this Employee
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    '''
    Required functions for custom users
    '''
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class EmployeeModelManager(BaseUserManager):


