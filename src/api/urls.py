from django.urls import path 
from .views import get_transactions, create_transaction, transaction_detail

urlpatterns = [
    path('transactions/', get_transactions, name='get_transactions'),
    path('createTransaction/', create_transaction, name='create_transaction'),
    path('transactionDetail/<int:pk>', transaction_detail, name='transaction_detail')
]