from rest_framework import serializers
from .models import CustomUser, BankAccounts, ExpenseCategory, IncomeCategory, SubCategoriesExpense, SubCategoriesIncome, Expense, Income
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude=["last_login", "last_logout", "created_at", "password_created_at", "is_active", "is_staff"]
        
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

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
        


class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'


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
    class Meta:
        model = Expense
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
