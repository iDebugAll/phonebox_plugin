from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.APIRootView = views.PhoneBoxPluginRootView

router.register(r'numbers', views.NumberViewSet)

app_name = "phonebox_plugin-api"
urlpatterns = router.urls
