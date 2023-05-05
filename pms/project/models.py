from django.db import models
from user.models import User
# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=30,null=False)
    desc = models.CharField(max_length=500)
    tech = models.CharField(max_length=100)
    estimatedHrs = models.IntegerField()
    startdate = models.DateTimeField()
    completitiondate = models.DateTimeField()
    
    class Meta:
        db_table = 'project'
        
    def __str__(self):
        return self.title 
    
class ProjectTeam(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    class Meta:
        db_table = 'team'
        
class Status(models.Model):
    name = models.CharField(max_length=20,null=False,unique=True)
    
    class Meta:
        db_table = 'status'
        
    def __str__(self):
        return self.name
    
class ProjectModule(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=False)
    desc = models.CharField(max_length=30)
    estimatedHrs = models.IntegerField()
    
    class Meta:
        db_table = 'module'
        
    def __str__(self):
        return self.name
    
prioritychoices = (('high', 'high'), ('low', 'low'),('medium', 'medium'))   
statuschoices = (('Completed', 'Completed'), ('inProgress', 'inProgress'),('Pending', 'Pending')) 

class Task(models.Model):
    module = models.ForeignKey(ProjectModule,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    status = models.CharField(choices=statuschoices,max_length=20)
    title = models.CharField(max_length=20)
    priority = models.CharField(choices=prioritychoices,max_length=20)
    desc = models.CharField(max_length=500,null=False)
    
    class Meta:
        db_table = 'task'
        
    def __str__(self):
        return self.title
        
class UserTask(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    taskid = models.ForeignKey(Task,on_delete=models.CASCADE)
    
    class Meta:
       db_table = 'user_task'