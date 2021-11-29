from django.urls import path
from . import views


urlpatterns = [
    path("", views.NumberListView.as_view(), name="list_view"),
    path("number/<int:pk>/", views.NumberView.as_view(), name="number_view"),
    path("add_number/", views.NumberEditView.as_view(), name="add_number"),
    path('import_numbers/', views.NumberBulkImportView.as_view(), name='import_numbers'),
    path("<int:pk>/edit/", views.NumberEditView.as_view(), name="number_edit"),
    path("number_bulk_edit/", views.NumberBulkEditView.as_view(), name="number_bulk_edit"),
    path("<int:pk>/delete/", views.NumberDeleteView.as_view(), name="number_delete"),
    path("number_bulk_delete/", views.NumberBulkDeleteView.as_view(), name="number_bulk_delete"),
    path("voice_circuit/<int:pk>/", views.VoiceCircuitView.as_view(), name="voice_circuit_view"),
    path("voice_circuit_list_view/", views.VoiceCircuitListView.as_view(), name="voice_circuit_list_view"),
    path("add_voice_circuit/", views.VoiceCircuitEditView.as_view(), name="add_voice_circuit"),
    path('import_voice_circuits/', views.VoiceCircuitBulkImportView.as_view(), name='import_voice_circuits'),
    path("voice_circuit/<int:pk>/edit/", views.VoiceCircuitEditView.as_view(), name="voice_circuit_edit"),
    path("voice_circuit_bulk_edit/", views.VoiceCircuitBulkEditView.as_view(), name="voice_circuit_bulk_edit"),
    path("voice_circuit/<int:pk>/delete/", views.VoiceCircuitDeleteView.as_view(), name="voice_circuit_delete"),
    path("voice_circuit_bulk_delete/", views.VoiceCircuitBulkDeleteView.as_view(), name="voice_circuit_bulk_delete"),
]
