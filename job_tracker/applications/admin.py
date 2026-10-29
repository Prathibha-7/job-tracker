from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job_role", "company", "user", "application_date", "status")
    list_filter = ("status", "application_date")
    search_fields = ("company", "job_role", "user__username", "user__email")
