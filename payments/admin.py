from django.contrib import admin
from payments.models import Transaction, Payment

# Register your models here.


admin.site.register(Payment)
admin.site.register(Transaction)