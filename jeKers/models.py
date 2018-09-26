from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

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
        return "%s, %s, %s, %s" % (self.name, self.department, self.status, self.presence)

class Logs(models.Model):
    log_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    action = models.CharField(max_length=500)

    def __str__(self):
        return "[%s] %s | %s " % (self.log_time.strftime("%Y-%m-%d %H:%M"), self.name, self.action)

@receiver(pre_save, sender=JeKer, dispatch_uid="add_logs")
def add_logs(sender, instance, **kwargs):
    before = JeKer.objects.filter(name=instance.name).first()
    after = instance
    messg = ""
    if not after:
        messg += "[removed '" + before.name + "']"

    if( not before):
        messg += "[added '"+after.name +"']"
    else:
        if(before.name != instance.name):
            messg += "[name change from '" + before.name + "' to '" + after.name + "']"
        if(before.department != instance.department):
            messg += "[department change from '" + before.department + "' to '" + after.department + "']"
        if(before.status != instance.status):
            messg += "[status change from '" + before.status + "' to '" + after.status + "']"
        if(before.mac_address != instance.mac_address):
            messg += "[mac_address change from '" + before.mac_address + "' to '" + after.mac_address + "']"
        if(before.presence != instance.presence):
            messg += "[presence change from '" + str(before.presence) + "' to '" + str(after.presence) + "']"

    log = Logs(name=instance.name, action=messg)
    log.save()
    print(log)

