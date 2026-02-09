from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+254712345678'"
    )

    phone = models.CharField(
        max_length=15,
        validators=[phone_validator],
        blank=True,
        null=True,
        help_text="Your contact phone number"
    )

    whatsapp = models.CharField(
        max_length=15,
        validators=[phone_validator],
        blank=True,
        null=True,
        help_text="Your WhatsApp number for bookings"
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text="Tell us about yourself"
    )

    is_host = models.BooleanField(
        default=False,
        help_text="Check if user is a property host"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_full_name(self):
        """Get user's full name"""
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name if full_name else self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when a new user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Create profile if it doesn't exist
        UserProfile.objects.create(user=instance)