from rest_framework import serializers
from .models import CustomUser, BankAccounts, ExpenseCategory, IncomeCategory, SubCategoriesExpense, SubCategoriesIncome, Expense, Income
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','fullname','email','password']
        
        
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.password_created_at = timezone.now()
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if validated_data.get('password',False):
            instance.set_password(validated_data['password'])
            instance.password_created_at = timezone.now()
            
            instance.save()
            
            del validated_data['password']
        
        user = super().update(instance, validated_data)
        return user
    
    
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.refresh_token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            self.fail('bad_token')


class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'
        read_only_fields = ['user']


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name']


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = '__all__'


class SubCategoriesExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriesExpense
        fields = '__all__'


class SubCategoriesIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriesIncome
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=BankAccounts.objects.none())
    
    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'value', 'account', 'date', 'time', 'notes']
        read_only_fields = ['user']
    
    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields['account'].querysetv = BankAccounts.objects.filter(user=user)
    


class IncomeSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=BankAccounts.objects.none())
    class Meta:
        model = Income
        fields = ['id', 'user', 'category', 'value', 'account', 'date', 'time', 'notes']
        read_only_fields = ['user']
        
    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields['account'].queryset = BankAccounts.objects.filter(user=user)
