from django.contrib import admin
from .models import CustomUser, Category,  Expense
from django.contrib import admin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'amount', 'is_staff', 'is_superuser', ]
    list_filter = ['username' ]
    list_display = ['username']

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category', {'fields': ['name', 'user']}),
        ('Amount', {'fields': ['budget']}),
        ('Date', {'fields': ['date']})
    ]
    list_display = ('name', 'user', 'budget', 'date')

    list_filter = ['name', 'user', 'date']
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'category', 'description')
    
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
