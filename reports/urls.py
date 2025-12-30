from django.urls import path
from reports.views import AttendanceSummaryReport, MembershipStatusReport, MembershipPlanReport,MonthlyMembershipReport, MembershipExpirySoonReport, FeedbackReportAPIView

urlpatterns = [
    path('attendance/summary/', AttendanceSummaryReport.as_view(), name="attendance-summary"),
    path('memberships/status/', MembershipStatusReport.as_view(), name="memberships-status"),
    path('memberships/plans/', MembershipPlanReport.as_view(), name="memberships-plans"),
    path('memberships/monthly/', MonthlyMembershipReport.as_view(), name="memberships-monthly"),
    path('memberships/expiring-soon/', MembershipExpirySoonReport.as_view(), name="memberships-expiring-soon"),
    path('feedback/', FeedbackReportAPIView.as_view(), name='feedback-report'),

]
