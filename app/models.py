from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.name)
    
class Chat(models.Model):
    group = models.ForeignKey(to=Group,on_delete=models.CASCADE,related_name="_chat")
    content = models.TextField()
    timestamp= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{str(self.group)} created {str(self.timestamp)}"