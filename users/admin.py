from django.contrib import admin
from .models import Profile, Department, Position, Emp_position, Works_in

# Register your models here.
admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Emp_position)
admin.site.register(Works_in)
