from django.urls import path
from . import views


urlpatterns = [
    path("", views.NumberListView.as_view(), name="list_view"),
    path("<int:pk>/", views.NumberView.as_view(), name="number_view"),
    path("add_number/", views.NumberEditView.as_view(), name="add_number"),
    path('import_numbers/', views.NumberBulkImportView.as_view(), name='import_numbers'),
    path("<int:pk>/edit/", views.NumberEditView.as_view(), name="number_edit"),
    path("number_bulk_edit", views.NumberBulkEditView.as_view(), name="number_bulk_edit"),
    path("<int:pk>/delete/", views.NumberDeleteView.as_view(), name="number_delete"),
    path("number_bulk_delete", views.NumberBulkDeleteView.as_view(), name="number_bulk_delete"),
]
