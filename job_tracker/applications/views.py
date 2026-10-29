from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import JobApplicationForm, RegistrationForm
from .models import JobApplication


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "applications/register.html", {"form": form})


@login_required
def dashboard(request):
    applications = JobApplication.objects.filter(user=request.user)
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    if query:
        applications = applications.filter(
            Q(company__icontains=query) | Q(job_role__icontains=query)
        )
    if status in JobApplication.Status.values:
        applications = applications.filter(status=status)

    return render(
        request,
        "applications/dashboard.html",
        {
            "applications": applications,
            "query": query,
            "selected_status": status,
            "statuses": JobApplication.Status.choices,
        },
    )


@login_required
def application_create(request):
    form = JobApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.save()
        messages.success(request, "Job application added.")
        return redirect("dashboard")
    return render(
        request,
        "applications/application_form.html",
        {"form": form, "page_title": "Add application"},
    )


@login_required
def application_update(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    form = JobApplicationForm(request.POST or None, instance=application)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Job application updated.")
        return redirect("dashboard")
    return render(
        request,
        "applications/application_form.html",
        {"form": form, "page_title": "Edit application"},
    )


@login_required
@require_POST
def application_update_status(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    status = request.POST.get("status", "")
    if status not in JobApplication.Status.values:
        messages.error(request, "Choose a valid application status.")
    else:
        application.status = status
        application.save(update_fields=["status", "updated_at"])
        messages.success(
            request,
            f"Status updated to {application.get_status_display()}.",
        )
    return redirect("dashboard")


@login_required
def application_delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        application.delete()
        messages.success(request, "Job application deleted.")
        return redirect("dashboard")
    return render(
        request,
        "applications/application_confirm_delete.html",
        {"application": application},
    )
