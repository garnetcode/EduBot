
"""Importing required libraries"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from config.fields import PseudonymizedField
from config.utils import mask, unmask
from subscriptions.models import Subscription



class CustomUserManager(BaseUserManager):
    """Custom user model manager where phone_number is the unique identifiers"""

    def create_superuser(self, phone_number, password, **other_fields):
        """Create and save a SuperUser with the given phone_number and password."""""

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )
        return self.create_user(phone_number, password, **other_fields)

    def create_user(self, phone_number, password, **other_fields):
        """Create and save a User with the given phone_number and password."""
        if not phone_number:
            raise ValueError(
                'You must provide phone number'
            )
        user = self.model(phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    """ User Model """
    phone_number = PseudonymizedField(
        models.CharField,
        (mask, unmask),
        max_length=20,
        unique=True,
        blank=True,
    )
    role = models.CharField(max_length=7, choices=(
            ("ADMIN", "ADMIN"),
            ("TUTOR", "TUTOR"),
            ("STUDENT", "STUDENT"),
            ("ORACLE", "ORACLE")
        ), default="STUDENT"
    )
    enrolled_courses = models.ManyToManyField(
        'courses.Course',
        related_name="enrolled_students",
        blank=True
    )
    ongoing_session = models.JSONField(default=dict, null=True)
    sex = models.CharField(max_length=6, choices=(
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("OTHER", "OTHER")
    ), default="OTHER"
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    class Meta:
        """Meta definition for User."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """Unicode representation of User."""
        #pylint: disable=no-member
        return f'{self.username if self.username else self.id}'

    def get_full_name(self):
        """Get full name of user"""
        return f'{self.first_name} {self.last_name}'
    
    def has_active_permission_for_course(self, course):
        """Check if user has permission for course"""
        print("CHECKING SUBSCRIPTION FOR : ", self, course, Subscription.objects.filter(user=self, course__code=course).exists(), Subscription.objects.filter(user=self, course__code=course, expiry_date__gte=datetime.now()).exists())
        if Subscription.objects.filter(user=self, course__code=course, expiry_date__gte=datetime.now()).exists():
            subscription = Subscription.objects.filter(user=self, course__code=course, expiry_date__gte=datetime.now()).first()
            print("ACCESS PERMISSION : ", subscription.package.access_permissions)
            if subscription.package.access_permissions in ['2', '3', '4']:
                return True
        return False
    
    def course_package(self, course):
        """Get course package"""
        if Subscription.objects.filter(user=self, course__code=course).exists():
            subscription = Subscription.objects.filter(user=self, course__code=course).first()
            return subscription.package
        return None
    
    def call_permissions(self, course):
        """Get call permissions"""
        # ('1', 'Curated Content'),
        # ('2', 'Curated Content + Whatsapp Calls'),
        # ('3', 'Curated Content + Whatsapp Calls + Zoom Calls'),
        # ('4', 'Curated Content + Whatsapp Calls + Zoom Calls + Live Classes')
        permissions = {
            1: ['Curated Content'],
            2: ['Curated Content', 'Whatsapp Calls'],
            3: ['Curated Content', 'Whatsapp Calls', 'Zoom Calls'],
            4: ['Curated Content', 'Whatsapp Calls', 'Zoom Calls', 'Live Classes']
        }
        if Subscription.objects.filter(user=self, course__code=course).exists():
            subscription = Subscription.objects.filter(user=self, course__code=course).first()
            return permissions[int(subscription.package.access_permissions)-1]
        return []


    @classmethod
    def filter_by_phone_number(cls, phone):
        """Filter user by phone number"""
        return cls.objects.filter(phone_number=phone).first()
    


