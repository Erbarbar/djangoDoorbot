from django.db import models

# Create your models here.
class JeKer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    DEPATRMENT_NAME = (
        ('TECH','Tecnologia'),
        ('INT', 'Interno'),
        ('INO', 'Inovação'),
        )
    department = models.CharField(max_length=4, choices=DEPATRMENT_NAME)
    STATUS_NAME = (
        ('EST', 'Estagiário'),
        ('JUN', 'Júnior'),
        ('SEN', 'Sénior'),
        ('CEO', 'CEO'),
        ('COO', 'COO'),
        )
    status = models.CharField(max_length=3, choices = STATUS_NAME)
    mac_address = models.CharField(max_length=5)
    presence = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
