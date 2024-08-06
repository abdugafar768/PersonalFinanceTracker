from django.shortcuts import render
from rest_framework import generics,status,viewsets,permissions,mixins,views
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from datetime import datetime, timedelta
from drf_multiple_model.views import FlatMultipleModelAPIView, FlatMultipleModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import *
from rest_framework.decorators import api_view



class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer



# class UserDetail(generics.RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class BankAccountView(viewsets.ModelViewSet):
    queryset = BankAccounts.objects.all()
    serializer_class = BankAccountsSerializer
    
    @action(detail=False, methods=['get'])
    def total_balance(self, request):
        total_balance = BankAccounts.objects.aggregate(total=Sum('initial_amount'))['total']
        return Response({'total_balance': total_balance})
    

    


class ExpenseCategoryView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpenseCategoryUpdateDeleteView(mixins.DestroyModelMixin,
                                      mixins.UpdateModelMixin,
                                      generics.GenericAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
    
class IncomeCategoryView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class IncomeCategoryDeletView(
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class SubCategoryExpenseView(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         generics.GenericAPIView):
    queryset = SubCategoriesExpense.objects.all()
    serializer_class = SubCategoriesExpenseSerializer
    
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class SubCategoryExpenseUDView(mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin,
                               generics.GenericAPIView):
    queryset = SubCategoriesExpense.objects.all()
    serializer_class = SubCategoriesExpenseSerializer
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.delete(request,  *args, **kwargs)
    

class ExpenseView(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    
    

    
    @action(detail=False, methods=['get'])
    def total_expense(self, request):
        total = self.get_queryset().aggregate(total=Sum('value'))['total']
        return Response({'Total Expase':total})
    
    @action(detail=False, methods=['get'])
    def this_month_expense(self, request):
        start_date = datetime.today().replace(day=1)
        end_date = datetime.today()
        total = self.get_queryset().filter(date__range=(start_date, end_date)).aggregate(total=Sum('value'))['total'] or 0
        return Response({'This month Expense': total})

    @action(detail=False, methods=['get'])
    def last_month_expense(self, request):

        last_day_of_last_month = datetime.today().replace(day=1) - timedelta(days=1)
     
        
        first_day_of_last_month = last_day_of_last_month.replace(day=1)
        
        total = self.get_queryset().filter(date__range=(first_day_of_last_month, last_day_of_last_month)).aggregate(total=Sum('value'))['total'] or 0
        return Response({'Last Month Expense': total})

class IncomeView(viewsets.ModelViewSet):
    queryset = Income.objects.all().order_by('-date')
    serializer_class = IncomeSerializer
    
    @action(detail=False, methods=['get'])
    def total_income(self,request):
        total = self.get_queryset().aggregate(total=Sum('value'))['total']
        return Response({'Total Income': total})
    
    @action(detail=False, methods=['get'])
    def last_month_income(self,request):
        # Geçen ayın son gününü bul
        last_day_of_last_month = datetime.today().replace(day=1) - timedelta(days=1)
        # Geçen ayın ilk gününü bul
        first_day_of_last_month = last_day_of_last_month.replace(day=1)
        
        total = self.get_queryset().filter(date__range=(first_day_of_last_month, last_day_of_last_month)).aggregate(total=Sum('value'))['total'] or 0
        return Response({'Last month income': total})
    
    @action(detail=False, methods=['get'])
    def this_month_income(self, request):
        start_date = datetime.today().replace(day=1)
        end_date = datetime.today()
        total = self.get_queryset().filter(date_range=(start_date,end_date)).aggregate(total=Sum(['value']))['total'] or 0
        return Response({'This Month Income':total})



    
class MultiQuerySetView(views.APIView):
    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', False)

        if category:
            expense_queryset = Expense.objects.filter(category__name=category)
            income_queryset = Income.objects.filter(category__name=category)
        else:
            expense_queryset = Expense.objects.all()
            income_queryset = Income.objects.all()


        expense_serializer = ExpenseSerializer(expense_queryset, many=True)
        income_serializer = IncomeSerializer(income_queryset, many=True)

        combined_data = [
            {"type": "expense", **item} for item in expense_serializer.data
        ] + [
            {"type": "income", **item} for item in income_serializer.data
        ]
        
        
        combined_data_sorted = sorted(combined_data, key=lambda x: x.get('date', ''), reverse=True)


        data = {
            'combined': combined_data_sorted
        }

        return Response(data, status=status.HTTP_200_OK)
    
    
    
# @api_view(['GET'])
# def projects_and_news(request):
#     if request.method == 'GET':
#  
#         expense = Expense.objects.all()
#         income = Income.objects.all()


#         serializer1 = ExpenseSerializer(expense, many=True, context={'request': request})
#         serializer2 = IncomeSerializer(income, many=True, context=  {'request': request})

#         data = {
#             'expense': serializer1.data,
#             'income': serializer2.data
#         }

#         return Response(data, status=status.HTTP_200_OK)




    