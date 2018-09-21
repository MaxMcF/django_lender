from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
import datetime

class Book(models.Model):
    CHECKEDOUT = [
        ('available', 'Available'),
        ('checked-out', 'Checked-out'),
    ]

    YEARS = [(str(i), str(i))for i in range(1900, 2018)]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=48)
    title = models.CharField(max_length=48)
    author = models.CharField(max_length=48)
    year = models.CharField(choices=YEARS, max_length=4)
    status = models.CharField(choices=CHECKEDOUT, default='checked-out', max_length=48)
    date_added = models.DateTimeField(auto_now_add=True)
    last_borrowed = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Book: {self.title} ({self.status})'

    def __repr__(self):
        return f'< Book: {self.title} | Author: {self.author} | Year: {self.year} | ISBN: {self.isbn} | Date_Added: {self.date_added} | Last_Borrowed {self.last_borrowed} | ({self.status}) >'

@receiver(models.signals.post_save, sender=Book)
def set_book_complete_date(sender, instance, **kwargs):
    if instance.status == 'checked-out' and not instance.date_completed:
        instance.date_completed = timezone.now()
        instance.save()