from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (confirmAttendanceAPIView, eventListCreateAPIView,
                    reviewSerializerAPIView, reviewSerializerDetailView)

router=DefaultRouter()
router.register("all-events",eventListCreateAPIView)
router.register("reviews",reviewSerializerDetailView)
router.register("confirm-attendance",confirmAttendanceAPIView)


urlpatterns = [
    path("",include(router.urls)),
    path("event/<int:event_pk>/reviews/",reviewSerializerAPIView.as_view(),name="event_reviews"),
]
