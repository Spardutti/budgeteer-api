from django.contrib import admin
from .models import CustomUser, MonthlyIncome, WeeklyCategory, WeeklyExpense
from django.contrib import admin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'amount', 'is_staff', 'is_superuser', ]
    list_filter = ['username', 'amount']
    list_display = ['username', 'amount']

class WeeklyCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Weekly Category', {'fields': ['name', 'user']}),
        ('Amount', {'fields': ['amount']}),
        ('Date', {'fields': ['year', 'month', 'week']})
    ]
    list_display = ('name', 'user', 'amount', 'week')

    list_filter = ['name', 'user', 'week']

class WeeklyExpenseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields':['user']}),
        ('Category', {'fields': ['weekly_category']}),
        ('Amount', {'fields':['amount']})
    ]
    list_display = ('id', 'amount', 'user', 'weekly_category')
    list_filter = ['user', 'weekly_category']

class MonthlyIncomeAdmin(admin.ModelAdmin):
    fieldsets =  [
       
        ('User', {'fields': ['user']}),
        ('Amount', {'fields': ['amount']}),
        ('Balance', {'fields': ['account_balance']}),
        ('Month', {'fields':['month']}),
        ('Year', {'fields':['year']})
    ]
    list_display = ('id', 'user', 'amount', 'account_balance', 'month', 'year')
    
admin.site.register(CustomUser, UserAdmin)
admin.site.register(WeeklyCategory, WeeklyCategoryAdmin)
admin.site.register(WeeklyExpense, WeeklyExpenseAdmin)
admin.site.register(MonthlyIncome, MonthlyIncomeAdmin)
