"""Imports for packages models."""
from django.db import models


class Package(models.Model):
    """Package Model"""
    name = models.CharField(max_length=255, null=False, blank=False, choices=(
        ('bronze', 'BRONZE'),
        ('silver', 'SILVER'),
        ('gold', 'GOLD'),
        ('platinum', 'PLATINUM'),
    ),
        default='bronze')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2
                                )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service_type = models.CharField(
        max_length=255,
        choices=(
            ('course_registration', 'Course Registration'),
            ('assignment_outsourcing', 'Assignment Outsourcing'),
        ), default='course_registration'
    )
    access_permissions = models.CharField(
        max_length=255,
        choices=(
            ('1', 'Curated Content'),
            ('2', 'Curated Content + Whatsapp Calls'),
            ('3', 'Curated Content + Whatsapp Calls + Zoom Calls'),
            ('4', 'Curated Content + Whatsapp Calls + Zoom Calls + Live Classes')
        ), default='1'
    )

    def __str__(self):
        """Unicode representation of Package."""
        return f"{self.name}"

    def get_permissions(self):
        """Get permissions for package."""
        permissions = {
            '1': 'Curated Content',
            '2': 'Curated Content + Whatsapp Calls',
            '3': 'Curated Content + Whatsapp Calls + Zoom Calls',
            '4': 'Curated Content + Whatsapp Calls + Zoom Calls + Live Classes'
        }
        return permissions[self.access_permissions]

    class Meta:
        """Meta definition for Package."""

        verbose_name = "Package"
        verbose_name_plural = "Packages"
