from django.urls import path

# import all of our views from the login application.
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('import', views.import_webinar, name="import"),
    path('participant/<email>', views.participant_details, name="participant_details"),
    path('webinar/<int:webinar_no>', views.webinar_no, name="webinar_no"),
    path('webinar/<int:webinar_no>/new', views.webinar_new_registrants, name="webinar_new_registrants"),
    path('webinar/<int:webinar_no>/attendees', views.webinar_attendees, name="webinar_attendees"),
    path('webinar/<int:webinar_no>/attendees/new', views.webinar_new_attendees, name="webinar_new_attendees"),
    path('webinar/<int:webinar_no>/cert', views.webinar_cert, name="webinar_cert"),
    path('webinar/<int:webinar_no>/cert/<int:time_for_certificates>', views.webinar_cert_time, name="webinar_cert_time"),
    path('webinar/<int:webinar_no>/cert/link', views.webinar_cert_link, name="webinar_cert_link"),
    path('chart', views.chart, name="chart"),
    path('test', views.test, name="test"),
]