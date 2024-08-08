from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from .managers import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    password_created_at = models.DateTimeField(null=True)
    last_login = models.DateTimeField(default=timezone.now)
    last_logout = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
class BankAccounts(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    account_currency = models.CharField(max_length=50)
    initial_amount = models.FloatField()
    notes = models.TextField()
    
    
    def save(self, *args, **kwargs):
        if not self.user and hasattr(self, 'request') and self.request.user.is_authenticated:
            self.user = self.request.user
        
        super().save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.name
    
    
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    

class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)
    
    
    def __str__(self) -> str:
        return self.name
    
    
    
class SubCategoriesExpense(models.Model):
    name = models.CharField(max_length=50)
    expanse_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    
    
class SubCategoriesIncome(models.Model):
    name = models.CharField(max_length=50)
    income_category = models.ForeignKey(IncomeCategory,on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return self.name


        

class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    value = models.FloatField()
    account = models.ForeignKey(BankAccounts, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    notes = models.TextField(blank=True, null=True)
    
    
    create_at = models.DateTimeField(auto_now_add=True)  
    update_at = models.DateTimeField(auto_now=True) 
    
    def save(self, *args, **kwargs):
        
        if self.pk is None: 
            if self.account:
                account = BankAccounts.objects.get(id=self.account.id)
                if account.initial_amount < self.value:
                    raise ValidationError("Insufficient funds in the account.")
        
 
        super(Expense, self).save(*args, **kwargs)
        

        if self.account and self.value:
            try:
                account = BankAccounts.objects.get(id=self.account.id)
                account.initial_amount -= self.value
                account.save()
            except BankAccounts.DoesNotExist:
                raise ValidationError("Account does not exist.")

    def __str__(self):
        return f"{self.category.name} - {self.value} - {self.date} - {self.account.name }"




class Income(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    value = models.FloatField()
    account = models.ForeignKey(BankAccounts, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    notes = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        
        if self.pk is None:
            if self.account:
                account = BankAccounts.objects.get(id=self.account.id)
            
                if account.initial_amount + self.value < 0:
                    raise ValidationError("Account balance would be negative.")
        
        super(Income, self).save(*args, **kwargs)
        
        
        if self.account and self.value:
            try:
                account = BankAccounts.objects.get(id=self.account.id)
                account.initial_amount += self.value
                account.save()
            except BankAccounts.DoesNotExist:
                raise ValidationError("Account does not exist.")
            
            
    def __str__(self):
        return f"{self.category.name} - {self.value} - {self.date} - {self.account.name }"