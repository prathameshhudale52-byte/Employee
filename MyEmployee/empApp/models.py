from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    dname = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.dname


class Role(models.Model):
    rname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.rname


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    salary = models.IntegerField()
    joining_date = models.DateField(null=True)   # rename from date

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.fname



class Leave(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee.fname} - {self.status}"
