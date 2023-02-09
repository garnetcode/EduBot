"""Material Models"""
from django.db import models

class CourseMaterial(models.Model):
    """Course Material Model"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    content_type = models.CharField(max_length=255,
        choices=(
            ("video", "Video"),
            ("audio", "Audio"),
            ("document", "Document"),
            ("image", "Image"),
            ("other", "Other"),
        )
    )
    # content is a file field with a custom upload_to path and maximum file size is 100MB
    file = models.FileField(upload_to="materials/")
    course = models.ForeignKey(
        "courses.Course", related_name="materials", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"