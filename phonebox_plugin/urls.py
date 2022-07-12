"""phonebox_plugin URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
## Numbers
    path("", views.NumberListView.as_view(), name="number_list"),
    path("number/add", views.NumberEditView.as_view(), name="number_add"),
    path("number/<int:pk>/", views.NumberView.as_view(), name="number_view"),
    path("number/<int:pk>/edit/", views.NumberEditView.as_view(), name="number_edit"),
    path("number/<int:pk>/delete/", views.NumberDeleteView.as_view(), name="number_delete"),
    path("number/list", views.NumberListView.as_view(), name="number_list"),
    path('number/import', views.NumberBulkImportView.as_view(), name='number_import'),
    path("number_bulk_edit/", views.NumberBulkEditView.as_view(), name="number_bulk_edit"),
    path("number_bulk_delete/", views.NumberBulkDeleteView.as_view(), name="number_bulk_delete"),

## Voice_circuits
    path("voice_circuit/add", views.VoiceCircuitEditView.as_view(), name="voice_circuit_add"),
    path("voice_circuit/<int:pk>/", views.VoiceCircuitView.as_view(), name="voice_circuit_view"),
    path("voice_circuit/<int:pk>/edit/", views.VoiceCircuitEditView.as_view(), name="voice_circuit_edit"),
    path("voice_circuit/<int:pk>/delete/", views.VoiceCircuitDeleteView.as_view(), name="voice_circuit_delete"),
    path("voice_circuit/list", views.VoiceCircuitListView.as_view(), name="voice_circuit_list"),
    path('voice_circuit/import', views.VoiceCircuitBulkImportView.as_view(), name='voice_circuit_import'),
    path("voice_circuit_bulk_edit/", views.VoiceCircuitBulkEditView.as_view(), name="voice_circuit_bulk_edit"),
    path("voice_circuit_bulk_delete/", views.VoiceCircuitBulkDeleteView.as_view(), name="voice_circuit_bulk_delete"),

## PBX
    path("pbx/add", views.PBXEditView.as_view(), name="pbx_add"),
    path("pbx/<int:pk>/", views.PBXView.as_view(), name="pbx_view"),
    path("pbx/<int:pk>/edit/", views.PBXEditView.as_view(), name="pbx_edit"),
    path("pbx/<int:pk>/delete/", views.PBXDeleteView.as_view(), name="pbx_delete"),
    path("pbx/list", views.PBXListView.as_view(), name="pbx_list"),
    path('pbx/import', views.PBXBulkImportView.as_view(), name='pbx_import'),
    path("pbx_bulk_edit/", views.PBXBulkEditView.as_view(), name="pbx_bulk_edit"),
    path("pbx_bulk_delete/", views.PBXBulkDeleteView.as_view(), name="pbx_bulk_delete"),
]