"""atlan_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from collect import views

router = DefaultRouter()
router.register(r'integration', views.IntegrationActionViewSet)
router.register(r'form', views.FormViewSet)
router.register(r'response', views.ResponseViewSet)

urlpatterns = [
        path('integrations/', views.ListIntegrations.as_view()),
        path('form/submit/', views.SubmitForm.as_view()),
] + router.urls
