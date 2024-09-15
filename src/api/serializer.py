from rest_framework  import serializers
from .models import Transactions    # import our Transaction object

# now how do we turn this into json?

class TransactionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Transactions
        fields = '__all__'