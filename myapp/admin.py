from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin


admin.site.register([CustomUser, 
                     BankAccounts,
                     IncomeCategory, 
                     SubCategoriesExpense,
                     SubCategoriesIncome,
                     Expense, 
                     Income])

admin.site.register(ExpenseCategory, DraggableMPTTAdmin)