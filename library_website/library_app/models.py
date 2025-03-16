from django.db import models
from django.core.validators import RegexValidator
import os

class SeatBooking(models.Model):
    name = models.CharField(max_length=100)

    phone_validator = RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits.")
    phone = models.CharField(max_length=10, unique=True, validators=[phone_validator])

    aadhar_validator = RegexValidator(regex=r'^\d{12}$', message="Aadhar number must be 12 digits.")
    aadhar_number = models.CharField(max_length=12, unique=True, validators=[aadhar_validator])

    address = models.TextField()

    SHIFT_CHOICES = [
        ('Morning', 'Morning Shift'),
        ('Afternoon', 'Afternoon Shift'),
        ('Evening', 'Evening Shift'),
    ]
    shift = models.CharField(max_length=50, choices=SHIFT_CHOICES)

    PRICE_DICT = {
        'Morning': 100.00,
        'Afternoon': 150.00,
        'Evening': 200.00,
    }

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    student_id = models.CharField(max_length=30, unique=True, blank=True, editable=False)

    def generate_student_id(self):
        """Generate student ID from name and phone number"""
        return f"{self.name.replace(' ', '')}_{self.phone[-4:]}"

    def get_upload_path(instance, filename, category, folder):
        """Return custom upload path with structured naming"""
        ext = filename.split('.')[-1]  # Get file extension (jpg, png, etc.)
        new_filename = f"{instance.student_id}_{category}.{ext}"  # studentid_category.ext
        return os.path.join(folder, new_filename)

    def profile_upload_path(instance, filename):
        return instance.get_upload_path(filename, "profile", "profile_pics/")

    def aadhar_front_upload_path(instance, filename):
        return instance.get_upload_path(filename, "aadharfront", "aadhar_pics/")

    def aadhar_back_upload_path(instance, filename):
        return instance.get_upload_path(filename, "aadharback", "aadhar_pics/")

    picture = models.ImageField(upload_to=profile_upload_path)
    aadhar_front = models.ImageField(upload_to=aadhar_front_upload_path)
    aadhar_back = models.ImageField(upload_to=aadhar_back_upload_path)

    def save(self, *args, **kwargs):
        """Assigns student ID and sets amount before saving."""
        if not self.student_id:
            self.student_id = self.generate_student_id()

        if self.shift in self.PRICE_DICT:
            self.amount = self.PRICE_DICT[self.shift]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.student_id} ({self.shift}: ₹{self.amount})"
