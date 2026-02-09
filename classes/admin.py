from django.contrib import admin
from classes.models import FitnessClass, ClassBooking, Trainer

# Register your models here.

admin.site.register(FitnessClass)
admin.site.register(ClassBooking)
admin.site.register(Trainer)