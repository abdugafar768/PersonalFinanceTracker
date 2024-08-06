from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'bankaccounts', BankAccountView)
router.register(r'income',IncomeView)
router.register(r'expense',ExpenseView)

urlpatterns = [
    #For USER
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('router/', include(router.urls)),
    
    
    path('expense_cagegory/', ExpenseCategoryView.as_view(), name='expense-list-create'),
    path('expense_cagegory/<int:pk>/', ExpenseCategoryUpdateDeleteView.as_view(), name='expense-detail'),
    
    path('income_cagegory/', IncomeCategoryView.as_view()),
    path('income_cagegory/<int:pk>/', IncomeCategoryDeletView.as_view()),
    
    path('subcategoryexpense/', SubCategoryExpenseView.as_view(), name='sub_category_list_create'),
    path('subcategoryexpense/<int:pk>/',SubCategoryExpenseUDView.as_view()),
    
    
   path('multi-queryset/', MultiQuerySetView.as_view(), name='multi_queryset'),
#    path('list/',projects_and_news)

]

