from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    def is_authenticated(self):
        return True
  
    def hashed_password(self, password=None):  
        if not password:  
            return self.password  
        else:  
            return hashlib.md5(password).hexdigest()  
          
    def check_password(self, password):  
        if self.hashed_password(password) == self.password:  
            return True  
        return False  
# Create your models here.
