from django.urls import path

from .views import MarkNotificationReadView, NotificationListView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('<int:pk>/', MarkNotificationReadView.as_view(), name='notification-detail'),
]
