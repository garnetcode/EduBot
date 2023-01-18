"""Models for the assignments app."""
from django.db import models


class PendingWork(models.Model):
    """PendingWork Model"""
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    file = models.FileField(upload_to="pending_work")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=255,
        choices= (
            ('In Progress', 'In Progress'),
            ('Published', 'Published'),
        ), default='In Progres'
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="pending_works"
    )

    uploaded_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="pending_works",
        null=True,


    )
    submitted_assignments = models.ManyToManyField(
        "assignments.Assignment",
        related_name="pending_works",
        blank=True
    )
    deadline = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        """Unicode representation of PendingWork."""
        return f"{self.title}"

    class Meta:
        """Meta definition for PendingWork."""

        verbose_name = "PendingWork"
        verbose_name_plural = "PendingWorks"

class Assignment(models.Model):
    """Assignment Model"""
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    file = models.FileField(upload_to="assignments")
    assignment_type = models.CharField(
        max_length=255,
        choices= (
            ('Outsourced', 'Outsourced'),
            ('In-House', 'In-House'),
        ), default='In-House'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=255,
        choices= (
            ('Pending', 'Pending'),
            ('Awaiting Payment', 'Awaiting Payment'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
        ), default='Pending'
    )
    payment = models.ForeignKey(
        "payments.Payment",
        on_delete=models.CASCADE,
        related_name="assignments",
        null=True
    )

    referenced_work = models.ForeignKey(
        "assignments.PendingWork",
        on_delete=models.CASCADE,
        related_name="assignments",
        null=True
    )

    submitted_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    def __str__(self):
        """Unicode representation of Assignment."""
        return f"{self.title}"

    def submit(self):
        """Submit assignment."""
        #pylint: disable=no-member
        self.referenced_work.submitted_assignments.add(self)
        self.status = "Completed"
        self.save()

    class Meta:
        """Meta definition for Assignment."""

        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
