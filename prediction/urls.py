from django.urls import path
from .views import IndexView, HistoryView, PredictAPIView

app_name = 'prediction'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('history/', HistoryView.as_view(), name='history'),
    path('api/predict/', PredictAPIView.as_view(), name='api_predict'),
]
