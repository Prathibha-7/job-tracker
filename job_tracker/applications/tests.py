from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import JobApplication


class JobTrackerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alex",
            email="alex@example.com",
            password="SecurePass123!",
        )
        self.client.force_login(self.user)

    def create_application(self, **overrides):
        values = {
            "user": self.user,
            "company": "Acme",
            "job_role": "Python Developer",
            "status": JobApplication.Status.APPLIED,
        }
        values.update(overrides)
        return JobApplication.objects.create(**values)

    def test_registration_creates_account_and_logs_user_in(self):
        self.client.logout()
        response = self.client.post(
            reverse("register"),
            {
                "username": "sam",
                "email": "sam@example.com",
                "password1": "StrongPass123!xyz",
                "password2": "StrongPass123!xyz",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(username="sam").exists())

    def test_login_is_required_for_dashboard(self):
        self.client.logout()

        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
        )

    def test_user_can_create_edit_filter_and_delete_application(self):
        create_response = self.client.post(
            reverse("application_create"),
            {
                "company": "Northstar",
                "job_role": "Backend Engineer",
                "application_date": "2026-10-28",
                "status": JobApplication.Status.INTERVIEW,
                "job_url": "https://example.com/jobs/1",
                "notes": "Technical interview next week",
            },
        )
        application = JobApplication.objects.get(company="Northstar")
        self.assertEqual(application.user, self.user)
        self.assertRedirects(create_response, reverse("dashboard"))

        dashboard_response = self.client.get(
            reverse("dashboard"),
            {"q": "backend", "status": JobApplication.Status.INTERVIEW},
        )
        self.assertContains(dashboard_response, "Northstar")
        self.assertContains(dashboard_response, "Backend Engineer")

        update_response = self.client.post(
            reverse("application_update", args=[application.pk]),
            {
                "company": "Northstar Labs",
                "job_role": "Backend Engineer",
                "application_date": "2026-10-28",
                "status": JobApplication.Status.SELECTED,
                "job_url": "",
                "notes": "",
            },
        )
        application.refresh_from_db()
        self.assertEqual(application.company, "Northstar Labs")
        self.assertEqual(application.status, JobApplication.Status.SELECTED)
        self.assertRedirects(update_response, reverse("dashboard"))

        delete_response = self.client.post(
            reverse("application_delete", args=[application.pk])
        )
        self.assertFalse(JobApplication.objects.filter(pk=application.pk).exists())
        self.assertRedirects(delete_response, reverse("dashboard"))

    def test_search_filters_by_company_or_role_and_status(self):
        self.create_application(company="Orbit", job_role="Data Analyst")
        self.create_application(
            company="Pine Labs",
            job_role="Product Designer",
            status=JobApplication.Status.REJECTED,
        )

        response = self.client.get(
            reverse("dashboard"),
            {"q": "product", "status": JobApplication.Status.REJECTED},
        )

        self.assertContains(response, "Pine Labs")
        self.assertNotContains(response, "Orbit")

    def test_user_can_update_application_status_from_dashboard(self):
        application = self.create_application()

        response = self.client.post(
            reverse("application_update_status", args=[application.pk]),
            {"status": JobApplication.Status.INTERVIEW},
        )

        application.refresh_from_db()
        self.assertEqual(application.status, JobApplication.Status.INTERVIEW)
        self.assertRedirects(response, reverse("dashboard"))

    def test_status_update_rejects_invalid_status(self):
        application = self.create_application()

        response = self.client.post(
            reverse("application_update_status", args=[application.pk]),
            {"status": "in_progress"},
        )

        application.refresh_from_db()
        self.assertEqual(application.status, JobApplication.Status.APPLIED)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(list(response.wsgi_request._messages)[0].level_tag, "error")

    def test_user_cannot_access_another_users_application(self):
        application = self.create_application()
        other_user = User.objects.create_user(username="other", password="pass12345")
        application.user = other_user
        application.save()

        response = self.client.get(
            reverse("application_update", args=[application.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_registration_page_renders(self):
        self.client.logout()

        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create your account")
