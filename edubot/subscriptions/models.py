"Imports"
from django.db import models


class Subscription(models.Model):
    """ Subscription Model """
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_subscription"
    )

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="course_subscription"
    )

    package = models.ForeignKey(
        "packages.Package",
        on_delete=models.CASCADE,
        related_name="package_subscription",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        """Meta definition for Subscription."""
        unique_together = ("user", "course")
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
