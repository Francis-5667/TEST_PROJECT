from django.db import models

class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)  # Primary key
    name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)  # Primary key
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    classroom = models.ForeignKey(Classroom,related_name='students',on_delete=models.CASCADE)

    def __str__(self):
        return self.name


