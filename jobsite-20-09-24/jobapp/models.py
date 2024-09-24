from django.db import models
from django.conf import settings

from authapp.models import*

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    workplace_type = models.CharField(max_length=50, choices=[('Remote', 'Remote'), ('Office', 'Office')])
    salary = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    posted_date = models.DateField()
    
    job_type = models.CharField(max_length=50, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ])
    location = models.CharField(max_length=100, choices=[
        ('Mumbai', 'Mumbai'),
        ('Bengaluru', 'Bengaluru'),
        ('Delhi', 'Delhi'),
        ('Kerala', 'Kerala')
    ])
    
    job_category = models.CharField(max_length=100, choices=[
        ('Automotive-Jobs', 'Automotive-Jobs'),
        ('HealthCare', 'HealthCare'),
        ('Customer-Service', 'Customer-Service'),
        ('Project-Management', 'Project-Management'),
        ('Development', 'Development'),
        ('Design', 'Design'),
        ('Marketing', 'Marketing'),
        ('Accounting-Finance', 'Accounting-Finance'),
        
    ],  null=True,  
        blank=True, )

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    employee = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={"is_employee":True})
    cover_letter = models.TextField()
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Application by {self.employee} for {self.job}"
