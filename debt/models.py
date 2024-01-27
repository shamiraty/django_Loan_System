from django.db import models
from django.utils.html import mark_safe

#this list dictionaries are for model, to pick a list when entering Data
STATUS={
    ('Pending','Pending'),
    ('Approved','Approved'),
    ('Rejected','Rejected')
}
LOAN_STATUS={
    ('Active','Active'),
    ('Not Active','Not Active'),
  
}

class Department(models.Model):
    DepartmentName = models.CharField(max_length=250)
    HeadOfDepartment = models.CharField(max_length=250)
    RegisteredDate = models.DateTimeField(auto_now_add=True)
    DepartmentId = models.CharField(max_length=250, primary_key=True)
    def __str__(self):
        return self.DepartmentName

class Employee(models.Model):
    FirstName = models.CharField(max_length=250)
    LastName = models.CharField(max_length=250)
    FullName = models.CharField(max_length=250)
    EmployeeID = models.CharField(max_length=250, primary_key=True)
    DepartmentName = models.ForeignKey(Department, on_delete=models.CASCADE)
    RegisteredDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.FirstName + " " + self.LastName


class Customer(models.Model):
    FirstName = models.CharField(max_length=250)
    LastName = models.CharField(max_length=250)
    FullName = models.CharField(max_length=250)
    CustomerNationalID = models.CharField(max_length=250, primary_key=True)
    Resident = models.CharField(max_length=250)
    PhoneNumber = models.CharField(max_length=250)
    BusinessType = models.CharField(max_length=250)
    RegisteredDate = models.DateTimeField(auto_now_add=True)
    DateOfBirth = models.DateTimeField(auto_now=False)
    PassportSize=models.ImageField(upload_to='Passports/')
    NationalID=models.ImageField(upload_to='Documents/')
    
    #show image to admin site
    def __str__(self):
        return self.FirstName + " " + self.LastName
    def image_tag(self):
            return mark_safe('<img src="%s"width="50"style="border-radius:4px">'% (self.PassportSize.url))
    def national_id(self):
            return mark_safe('<img src="%s"width="50"style="border-radius:4px">'% (self.NationalID.url))

class Loan(models.Model):
    LoanID = models.CharField(max_length=250)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    loanStatus = models.CharField(max_length=50,null=True,choices=LOAN_STATUS,default='Active')
    RequestedAmount = models.FloatField()
    QualityAssurance = models.FloatField(default=0.02, editable=False)
    Insurance = models.FloatField(default=0.03, editable=False)
    Duration = models.IntegerField(editable=False)
    Interest = models.FloatField(default=0.1, editable=False)
    ActualDebt = models.IntegerField(editable=False)
    CashReceivable = models.IntegerField(editable=False)
    MonthlyInstallment = models.IntegerField(default=0.15, editable=False)
    RegisteredDate = models.DateTimeField(auto_now_add=True)
    Status=models.CharField(max_length=50,null=True,choices=STATUS,default='Pending')

    #compute loan
    def save(self, *args, **kwargs): 
        # Calculate QualityAssurance, Insurance, Interest as percentages of RequestedAmount
        self.QualityAssurance = 0.02 * self.RequestedAmount
        self.Insurance = 0.03 * self.RequestedAmount
        self.Interest = 0.1 * self.RequestedAmount

        # Calculate ActualDebt 
        self.ActualDebt = 0.1 * self.RequestedAmount

        # Calculate CashReceivable
        self.CashReceivable = self.RequestedAmount - self.Insurance - self.QualityAssurance - self.Interest

        # Calculate MonthlyInstallment based on ActualDebt
        self.MonthlyInstallment = 0.15 * self.ActualDebt

        # Update Duration calculation based on your specific logic
        self.Duration = self.ActualDebt / self.MonthlyInstallment

        super(Loan, self).save(*args, **kwargs)

class Target(models.Model):
    Amount=models.FloatField(default=100000)
    RegisteredDate = models.DateTimeField(auto_now_add=True)





 