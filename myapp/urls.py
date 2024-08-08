# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

router = DefaultRouter()

router.register(r'bankaccounts', BankAccountView, basename='bankaccount')
router.register(r'expenses', ExpenseView, basename='expense')
router.register(r'incomes', IncomeView, basename='income')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    path('expense-categories/', ExpenseCategoryView.as_view(), name='expense-categories'),
    path('expense-categories/<int:pk>/', ExpenseCategoryUpdateDeleteView.as_view(), name='expense-category-UD'),
    
    path('income-categories/', IncomeCategoryView.as_view(), name='income-categories'),
    path('income-categories/<int:pk>/', IncomeCategoryDeletView.as_view(), name='income-category-detail'),
    
    path('subcategories-expense/', SubCategoryExpenseView.as_view(), name='subcategories-expense'),
    path('subcategories-expense/<int:pk>/', SubCategoryExpenseUDView.as_view(), name='subcategories-expense-UD'),
    
    path('subcategories-income/', SubCategoryIncomeView.as_view(), name='subcategories-income'),
    path('subcategories-income/<int:pk>/', SubCategoryIncomeUDView.as_view(), name='subcategories-income-UD'),
    
    
    path('multiquery/', MultiQuerySetView.as_view(), name='multiquery'),
    path('router/', include(router.urls)),
]
