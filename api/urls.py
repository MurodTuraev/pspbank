from django.urls import path
from api.views import index, InitiateTransactionAPIView, PerformTransactionAPIView, TerminationTransactionAPIView, CheckPolisAPIView

urlpatterns = [
    path('InitiateTransactionRequest/', InitiateTransactionAPIView.as_view(), name='initiate'),
    path('PerformTransactionRequest/', PerformTransactionAPIView.as_view(), name='perform'),
    path('TerminationTransactionRequest/', TerminationTransactionAPIView.as_view(), name='terminate'),
    path('CheckPolisRequest/', CheckPolisAPIView.as_view(), name='chekpolis'),
]