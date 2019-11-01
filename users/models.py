from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.core.exceptions import ValidationError, FieldError
# Create your models here.
from django.utils import timezone


class Profile(models.Model):
    STATUS_CHOICES = [
    ("Permanent", ("Permanent")),
    ("Temporary", ("Temporary")),
    ("Contractor", ("Contractor")),
    ("Intern", ("Intern"))
    ]
    GENDER_CHOICES = (
    (1, ("Male")),
    (2, ("Female")),
    (3, ("Not Specified"))
    )
    PAY_CHOICES = [
    ('Fixed', ("Fixed")),
    ('Performance Based', ("Performance Based")),
    ('Not Assigned', ("Not Assigned")),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    emp_type = models.CharField(max_length=20,choices=STATUS_CHOICES, null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    user_active = models.BooleanField(default=True)
    contact = models.CharField(max_length=13, blank=True)
    whatsapp = models.CharField(max_length=13, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=3)
    pay_type = models.CharField(max_length=20,choices=PAY_CHOICES,  null=True, blank=True)
    pay = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='users/images', default='users/images/default.jpg')
    title = models.CharField(max_length=25, null=True, blank=True)
    #manager_username = models.ForeignKey(User, blank=True, null=True, to_field='username',related_name='manager_username', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Department(models.Model):
    name = models.CharField(max_length=20, unique=True)
    base_offer = models.IntegerField(null=False, default=0, blank=False)
    min_pay = models.IntegerField(null=False, default=0, blank=False)

    mantis = models.TextField()
    slack = models.TextField()
    whatsapp = models.TextField()

    def __str__(self):
        return self.name

class Position(models.Model):
    # POS_CHOICES = (
    # (1, ("CEO")),
    # (2, ("Dev Manager")),
    # (3, ("Testing Manager")),
    # (4, ("Developer")),
    # (5, ("Tester")),
    # )
    position_name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.position_name


class Emp_position(models.Model):

    emp_uname = models.OneToOneField(User, related_name='emp_name', to_field='username', on_delete=models.CASCADE)
    position_name = models.ForeignKey(Position, related_name='position', to_field='position_name', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.emp_uname) + " " + str(self.position_name)



class Works_in(models.Model):
    emp_name = models.ForeignKey(User, related_name='works_emp_name', to_field='username', on_delete=models.CASCADE)
    dept_name = models.ForeignKey(Department, blank=False, null=False, to_field='name',related_name='works_on_dept', on_delete=models.CASCADE)

    class Meta:
        unique_together = ["emp_name", "dept_name"]

    def __str__(self):
        return str(self.emp_name) + " " + str(self.dept_name)


    def clean(self):
        emp_list = list(Works_in.objects.filter(dept_name=str(self.dept_name)).values_list('emp_name'))
        count = Emp_position.objects.filter(emp_uname__in=emp_list, position_name="Manager")
        is_manager = Emp_position.objects.filter(emp_uname = self.emp_name, position_name='Manager')
        # first the employee position should be added and then only department
        if(len(Emp_position.objects.filter(emp_uname = self.emp_name)) == 0):
            raise ValidationError(f"{self.emp_name}'s Position hasn't been added yet")
        if len(count)>=1 and len(is_manager)>=1:
            raise ValidationError('Manager already assigned to this department')
