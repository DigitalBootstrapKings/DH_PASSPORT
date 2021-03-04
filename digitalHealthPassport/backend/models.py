from django.db import models

# User Model

class User(models.Model):
    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    DOB = models.DateField(null=True)
    OHIP = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=1024, null=True)
    secureToken = models.CharField(max_length=1024, null=True)
    phoneNumber = models.CharField(max_length=10, null=True)
    verified_user = models.BooleanField(default=False)
    vaccineStatus = models.BooleanField(default=False) 
    exposure = models.BooleanField(default=False) 

    def __str__(self):
        return f'Phone: {str(self.phoneNumber)} Email: {self.email} Password: {self.password}'

class Vaccinated(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    vaccinationDate = models.DateField()
    vaccinationType = models.CharField(max_length=30)


class CovidTest(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTaken = models.DateField()
    testResults = models.BooleanField()

class OneTimeText(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    oneTimeValue = models.CharField(max_length=7)
    stillValid = models.BooleanField()
    
class Employee(models.Model):
    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=1024, null=True)
    secureToken = models.CharField(max_length=1024, null=True)