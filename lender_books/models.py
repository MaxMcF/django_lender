from django.db import models
import datetime

class Book(models.Model):
    CHECKEDOUT = [
        ('available', 'Available'),
        ('checked-out', 'Checked-out'),
    ]

    YEARS = [(str(i), str(i))for i in range(1900, 2018)]

    isbn = models.CharField(max_length=48)
    title = models.CharField(max_length=48)
    author = models.CharField(max_length=48)
    year = models.CharField(choices=YEARS, max_length=4)
    status = models.CharField(choices=CHECKEDOUT, default='checked-out', max_length=48)
    date_added = models.DateTimeField(auto_now_add=True)
    last_borrowed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Book: {self.title} ({self.status})'

    def __repr__(self):
        return f'< Book: {self.title} | Author: {self.author} | Year: {self.year} | ISBN: {self.isbn} | Date_Added: {self.date_added} | Last_Borrowed {self.last_borrowed} | ({self.status}) >'
