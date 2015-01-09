import datetime

from django.db import models
from django.utils import timezone

class User(models.Model):
    """
    The User model contains basic information about the user.
    """
    username = models.CharField(max_length=100)
    email    = models.EmailField(max_length=254)
    def __str__(self):
        return self.username
        
class ToDoItem(models.Model):
    """
    The ToDoItem model contains all of the information related to a 
    single to-do item.
    """
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    create_date = models.DateTimeField(db_index=True, auto_now_add=True)
    due_date = models.DateTimeField(db_index=True)
    priority = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """
        Returns True if the due date has passed, otherwise False.
        """
        return timezone.now() >= self.due_date
        
    def is_due_within_7_days(self):
        """
        Returns True if the due date is within the next 7 days, otherwise False.
        """
        now = timezone.now()
        return now <= self.due_date <= now + datetime.timedelta(days=7) 
    
    def is_due_within_14_days(self):
        """
        Returns True if the due date is between 7 and 14 days from now, 
        otherwise False.
        """
        now = timezone.now()
        7days = now + datetime.timedelta(days=7, seconds=1)
        14days = now + datetime.timedelta(days=14)
        return 7days <= self.due_date <= 14days
        
    def is_due_more_than_14_days(self):
        """
        Returns True if the due date is more than 14 days away, otherwise
        False.
        """
        14days = timezone.now() + datetime.timedelta(days=14, seconds=1)
        return 14days <= self.due_date
        
    