from django.contrib import admin
from memberships.models import MembershipPlan, Subscription

# Register your models here.

admin.site.register(MembershipPlan)
admin.site.register(Subscription)