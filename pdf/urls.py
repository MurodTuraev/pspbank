from django.urls import path
from .views import render_pdf_view, prod_template

urlpatterns = [
    path('', render_pdf_view, name='render-pdf'),
    path('prod_template/', prod_template, name='prod_template'),
]