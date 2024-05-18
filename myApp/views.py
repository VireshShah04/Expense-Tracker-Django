from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime as dt

# Create your views here.
def index(request):
    if request.method == 'POST':
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            # Create an instance of the expense form but don't save it yet
            expense = expense.save(commit = False) 
            # Set the user field of the expense to the currently logged-in user
            expense.user = request.user
            expense.save()
            
    expense_form = ExpenseForm()
    expenses = Expense.objects.filter(user = request.user.id)
    total_expense = expenses.aggregate(Sum('amount'))

    # Logic to calculate 365 days expenses
    last_year = dt.date.today() - dt.timedelta(days=365)
    data_year = Expense.objects.filter(date__gt = last_year, user = request.user.id)
    last_year_expense = data_year.aggregate(Sum('amount'))

    # Logic to calculate 30 days expenses
    last_month = dt.date.today() - dt.timedelta(days=30)
    data_month = Expense.objects.filter(date__gt = last_month, user = request.user.id)
    last_month_expense = data_month.aggregate(Sum('amount'))

    # Logic to calculate 30 days expenses
    last_week = dt.date.today() - dt.timedelta(days=7)
    data_week = Expense.objects.filter(date__gt = last_week, user = request.user.id)
    last_week_expense = data_week.aggregate(Sum('amount'))

    # Logic to calculate daily expense
    daily_expense = Expense.objects.filter(user = request.user.id).values('date').order_by('date').annotate(sum = Sum('amount'))
    
    # Logic to calculate expense based on category
    category_expense = Expense.objects.filter(user = request.user.id).values('category').annotate(sum = Sum('amount'))
    print(category_expense)

    context = {'expense_form': expense_form, 
               'expenses': expenses, 
               'total_expense': total_expense, 
               'last_year_expense': last_year_expense, 
               'last_month_expense': last_month_expense, 
               'last_week_expense': last_week_expense,
               'daily_expense': daily_expense,
               'category_expense': category_expense,
            }
    return render(request, 'index.html', context=context)


def edit_expense(request, id):
    expense = Expense.objects.get(id = id)
    expense_form = ExpenseForm(instance = expense)
    if request.method == 'POST':
        expense = ExpenseForm(request.POST, instance=expense)
        if expense.is_valid():
            expense.save()
            return redirect('myapp:index')
    
    return render(request, 'edit.html', {'expense_form': expense_form})


def delete_expense(request, id):
    if request.method == 'POST' and 'delete' in request.POST:
        expense = Expense.objects.get(id = id)
        expense.delete()
        return redirect('myapp:index')