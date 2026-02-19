from django.db import models

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ("membership", "Membership Inquiry"),
        ("training", "Personal Training"),
        ("classes", "Group Classes"),
        ("facility", "Facility Tour"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
