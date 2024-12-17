from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator

class Employee(models.Model):
    """Represents an employee who can manage influencers."""
    first_name = models.CharField(
        max_length=50, 
        validators=[
            MaxLengthValidator(50, "First name cannot exceed 50 characters"),
            MinLengthValidator(1, "First name is required")
        ]
    )
    last_name = models.CharField(
        max_length=50, 
        validators=[
            MaxLengthValidator(50, "Last name cannot exceed 50 characters"),
            MinLengthValidator(1, "Last name is required")
        ]
    )
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Influencer(models.Model):
    """Represents an influencer in the system."""

    first_name = models.CharField(
        max_length=50, 
        validators=[
            MaxLengthValidator(50, "First name cannot exceed 50 characters"),
            MinLengthValidator(1, "First name is required")
        ]
    )
    last_name = models.CharField(
        max_length=50, 
        validators=[
            MaxLengthValidator(50, "Last name cannot exceed 50 characters"),
            MinLengthValidator(1, "Last name is required")
        ]
    )
    manager = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_influencers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SocialMediaAccount(models.Model):
    """Represents a social media account for an influencer."""
    SOCIAL_MEDIA_PLATFORMS = [
        ('INSTAGRAM', 'Instagram'),
        ('TIKTOK', 'TikTok')
    ]

    influencer = models.ForeignKey(
        Influencer, 
        on_delete=models.CASCADE, 
        related_name='social_media_accounts'
    )
    platform = models.CharField(
        max_length=10, 
        choices=SOCIAL_MEDIA_PLATFORMS
    )
    username = models.CharField(
        max_length=50, 
        validators=[
            MaxLengthValidator(50, "Username cannot exceed 50 characters"),
            MinLengthValidator(1, "Username is required")
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['influencer', 'platform', 'username']
        ordering = ['created_at']

    def __str__(self):
        return f"{self.platform}: {self.username}"
