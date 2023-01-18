"""Models for the courses app."""
import random
import string
from django.db import models

# pylint: disable = no-name-in-module
from users.models import User


def generate_code(letter=True, number=True, length=4):
    """Generate a random code."""
    if letter and number:
        return 'C' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length - 1))
    elif letter:
        return 'C' + ''.join(random.choices(string.ascii_uppercase, k=length - 1))
    elif number:
        return 'C' + ''.join(random.choices(string.digits, k=length - 1))
    else:
        raise ValueError('At least one of letter or number must be True')


class Course(models.Model):
    """Course Model"""
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=10, default=generate_code)
    duration = models.IntegerField()
    description = models.TextField()
    instructors = models.ManyToManyField(
        User,
        related_name="tutor_courses"
    )
    students = models.ManyToManyField(
        User,
        related_name="student_courses"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Unicode representation of Course."""
        return f"{self.name} - {self.code}"

    class Meta:
        """Meta definition for Course."""

        verbose_name = "Course"
        verbose_name_plural = "Courses"
