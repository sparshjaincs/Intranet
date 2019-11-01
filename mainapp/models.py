from django.db import models
from users.models import Position
# Create your models here.


class NewProvisionalEmployeeMail(models.Model):
    STATUS_CHOICES = [
    ("Permanent", ("Permanent")),
    ("Temporary", ("Temporary")),
    ("Contractor", ("Contractor")),
    ("Intern", ("Intern"))
    ]
    PAY_CHOICES = [
    ('Fixed', ("Fixed")),
    ('Performance Based', ("Performance Based")),
    ('Not Assigned', ("Not Assigned")),
    ]
    POSITION_CHOICES = ()
    for i, name in enumerate(Position.objects.values_list('position_name')):
        POSITION_CHOICES += ((i, name[0]),)
    email = models.EmailField(max_length=70, null=False, blank=False, unique=False)
    token = models.TextField(blank=False, null=False)
    offer_sent_by = models.CharField(max_length=50)
    position_name = models.IntegerField(choices=POSITION_CHOICES, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    name=models.CharField(max_length=30)
    username=models.CharField(max_length=30)
    pay = models.IntegerField(default=0)
    title = models.CharField(max_length=25, null=True, blank=True)
    pay_type = models.CharField(max_length=20,choices=PAY_CHOICES,  null=True, blank=True)
    emp_type = models.CharField(max_length=20,choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(self.offer_sent_by) +" to " + str(self.email)


    def clean(self):
        if(NewProvisionalEmployeeMail.objects.filter(email=str(self.email)).exists()):
            NewProvisionalEmployeeMail.objects.filter(email=str(self.email)).delete()

    def save(self, **kwargs):
        self.clean()
        return super(NewProvisionalEmployeeMail, self).save(**kwargs)
