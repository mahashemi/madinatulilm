from django.urls import path
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from .models import ContactMessage, Question
from .serializers import ContactMessageSerializer, QuestionSerializer, PublicQASerializer

app_name = "api_contact"


class ContactCreateView(ListCreateAPIView):
    queryset = ContactMessage.objects.none()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(ip_address=self.request.META.get("REMOTE_ADDR"))


class QuestionCreateView(ListCreateAPIView):
    queryset = Question.objects.none()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(ip_address=self.request.META.get("REMOTE_ADDR"))


urlpatterns = [
    path("",        ContactCreateView.as_view(),                                                                              name="contact"),
    path("ask/",    QuestionCreateView.as_view(),                                                                             name="ask"),
    path("public-qa/", ListAPIView.as_view(queryset=Question.objects.filter(is_public=True, status="answered"), serializer_class=PublicQASerializer), name="public-qa"),
]
