from django.contrib import admin
from . import models
from django.utils.html import format_html

#Register Department
admin.site.register(models.Department)
 
#Register Loan
class LoanAdmin(admin.ModelAdmin):
    list_per_page = 9
    list_max_show_all = 9
    list_editable = ['Status','loanStatus',]
    list_display = (
     'Customer', 'loanStatus', 'RequestedAmount', 'QualityAssurance', 'Insurance',
    'Interest', 'ActualDebt', 'CashReceivable', 'MonthlyInstallment','Status','status','_')
   #change icons to status
    def _(self,obj):
        if obj.Status=='Approved':
            return True
        elif obj.Status=='Pending':
             return None
        else:
            return False
    _.boolean=True
   #colors
    def status(self,obj):
      if obj.Status=="Approved":
            color='#00F142'
      elif obj.Status=="Pending":
             color='#CEBB00'
      else:
           color='#FF0000'
      return format_html('<strong><p style="color:{}">{}</p></strong>'.format(color,obj.Status))
    status.allow_tags=True  
admin.site.register(models.Loan, LoanAdmin)


#Register Customer
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 9
    list_max_show_all = 9
    list_editable = ['PhoneNumber','Resident']
    search_fields = ('FirstName','PhoneNumber',)
    list_display = ('FirstName', 'Resident', 'PhoneNumber', 'RegisteredDate','BusinessType', 'image_tag', 'national_id')
admin.site.register(models.Customer, CustomerAdmin)

#Register Business Target
class TargetAdmin(admin.ModelAdmin):
    list_per_page = 9
    list_max_show_all = 9
    list_editable = ['Amount',]
    search_fields = ('Amount',)
    list_display = ('id','Amount',)
admin.site.register(models.Target, TargetAdmin)

#Register Employee
class EmployeeAdmin(admin.ModelAdmin):
    list_per_page = 9
    list_max_show_all = 9
    list_editable = ['DepartmentName',]
    search_fields = ('EmployeeID',)
    list_display = ('FullName','EmployeeID','DepartmentName','RegisteredDate')
admin.site.register(models.Employee, EmployeeAdmin)




