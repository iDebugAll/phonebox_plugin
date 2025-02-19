from django.urls import path, include
from . import views
from utilities.urls import get_model_urls

app_name = "phonebox_plugin"

urlpatterns = (
    path(
        "numbers/",
        include(get_model_urls("phonebox_plugin", "number", detail=False)),
    ),
    path(
        "numbers/<int:pk>/",
        include(get_model_urls("phonebox_plugin", "number")),
    ),
    path(
        "voicecircuits/",
        include(get_model_urls("phonebox_plugin", "voicecircuit", detail=False)),
    ),
    path(
        "voicecircuits/<int:pk>/",
        include(get_model_urls("phonebox_plugin", "voicecircuit")),
    ),
)
