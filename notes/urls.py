from django.urls import path
from .views import NoteView

urlpatterns = [
    path('', NoteView.as_view()),
    path('<int:pk>', NoteView.as_view()),
]