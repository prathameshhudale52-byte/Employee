from django import forms
from .models import Employee,Department,Role

class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields='__all__'


class DepartmentForm(forms.ModelForm):
    class Meta:
        model=Department
        fields='__all__'


class RoleForm(forms.ModelForm):
    class Meta:
        model=Role
        fields='__all__'



from .models import Leave

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
