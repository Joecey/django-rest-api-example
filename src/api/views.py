from django.shortcuts import render # This is used for templating, don't worry about this for now

# import packages for rest api 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status   # use this to return correct response codes
from .models import Transactions
from .serializer import TransactionSerializer

# Create your views here.

@api_view(['GET'])
def get_transactions(request):
    transactions = Transactions.objects.all() # get all of the transactions in database
    serializer = TransactionSerializer(transactions, many=True) # many lets us know that we can expect a list
    return Response(serializer.data) # make sure to specify `.data here!`
    
    
@api_view(['POST'])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    
    # is the data given valid?
    if serializer.is_valid():
        serializer.save()   # save to database if valid
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# here we specify multiple CRUD actions
@api_view(['GET', 'PUT', 'DELETE'])
def transaction_detail(request, pk):
    try:
        transaction = Transactions.objects.get(pk=pk)
    except Transactions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # if the record is found, perform you action
    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TransactionSerializer(transaction, data=request.data)
        
        # if valid, save the user in the corresponding primary key 
        if serializer.is_valid():
            serializer.save()   # save to database if valid
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        transaction.delete() # delete record from database
        return Response(status=status.HTTP_204_NO_CONTENT)
