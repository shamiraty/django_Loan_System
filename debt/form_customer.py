from django import forms
from .models import Customer
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.core.exceptions import ValidationError
from PIL import Image

#Region List fo drop down
REGION = (
    ('Default', "Tanzania"),
    ('Dodoma', "Dodoma"),
    ('Tanga', "Tanga"),
    ('Arusha', "Arusha"),
    ('Tabora', "Tabora"),
    ('Mwanza', "Mwanza"),
    ('Kigoma', "Kigoma"),
    ('Kilimanjaro', "Kilimanjaro"),
    ('Pwani', "Pwani"),
    ('Morogoro', "Morogoro"),
    ('Singida', "Singida"),
    ('Shinyanga', "Shinyanga"),
)

#Business List fo drop down
BUSINESS = (
    ('Small Business', 'Small Business'),
    ('Medium Sized', 'Medium Sized'),
    ('Interprise', 'Interprise'),
    ('Education', 'Education'),
    ('Agriculture', 'Agriculture'),
)
#Main Customer Form
class CustomerAdd(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

        #This widget defines Multiple Radio Button for BusinessType and Options selection for Resident
        widgets = {

            'Resident': forms.Select(choices=REGION, attrs={'class': 'form-control', 'style': 'font-size:18px;'}),
            'BusinessType': forms.CheckboxSelectMultiple(choices=BUSINESS,
                                                         attrs={'class': 'form-control', 'style': 'font-size:18px;'}),
            'DateOfBirth': DatePickerInput()
        }

 #this function validates PassPort Size
    def clean_PassportSize(self):
        passport_size = self.cleaned_data.get('PassportSize')
        if passport_size:
            if passport_size.size > 1024 * 1024:  # 1 MB
                raise ValidationError('Passport size should be less than 1 MB.')
            if not passport_size.name.lower().endswith(('.png', '.jpeg', '.jpg')):
                raise ValidationError('Passport should be in PNG or JPEG format.')
        return passport_size
    
#this function validates NationalID
    def clean_NationalID(self):
        national_id = self.cleaned_data.get('NationalID')
        if national_id:
            if national_id.size > 1024 * 1024:  # 1 MB
                raise ValidationError('National ID size should be less than 1 MB.')
            if not national_id.name.lower().endswith(('.png', '.jpeg', '.jpg')):
                raise ValidationError('National ID should be in PNG or JPEG format.')
        return national_id
    
#this function validates PhoneNumber
    def clean_PhoneNumber(self):
        phone_number = self.cleaned_data.get('PhoneNumber')
        if phone_number:
            # Remove any non-digit characters
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # Check if the length is exactly 9 digits
            if len(phone_number) != 10:
                raise ValidationError('Phone number should be 10 digits long.')

            self.cleaned_data['PhoneNumber'] = phone_number
        return phone_number

#this function validates CustomerNationalID
    def clean_CustomerNationalID(self):
        customer_national_id = self.cleaned_data.get('CustomerNationalID')
        if customer_national_id and len(customer_national_id) > 9:
            raise ValidationError('Customer National ID should be less than 9 characters.')
        return customer_national_id
    def clean_PassportSize(self):
        passport_size = self.cleaned_data.get('PassportSize')
        if passport_size:
            if passport_size.size > 1024 * 1024:  # 1 MB
                raise ValidationError('Passport size should be less than 1 MB.')
            if not passport_size.name.lower().endswith(('.png', '.jpeg', '.jpg')):
                raise ValidationError('Passport should be in PNG or JPEG format.')
            # Validate image dimensions
            max_width = 800
            max_height = 600
            image = Image.open(passport_size)
            width, height = image.size
            if width > max_width or height > max_height:
                raise ValidationError(f'Passport size should be {max_width} x {max_height} pixels or smaller.')

        return passport_size

