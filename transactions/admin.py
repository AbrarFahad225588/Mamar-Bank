from django.contrib import admin
from .views import send_transactions_email
from .models import Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approve','bankrupt']
    actions = ['mark_bankrupt']

    def mark_bankrupt(self, request, queryset):
        queryset.update(bankrupt=True)
        self.message_user(request, "Selected transactions marked as bankrupt.")
    mark_bankrupt.short_description = "Mark selected transactions as bankrupt"


    def save_model(self, request, obj, form, change):
        if obj.loan_approve ==True:
            obj.account.balance += obj.amount
            obj.balance_after_transaction = obj.account.balance
            obj.account.save()
            send_transactions_email(obj.account.user, obj.amount, "Loan Approval", "transactions/admin_email.html")
        super().save_model(request, obj, form, change)
