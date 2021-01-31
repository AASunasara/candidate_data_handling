from django import forms
from .models import candidates

class CandidateForm(forms.ModelForm):
    verbal_eng_skill_rate = forms.IntegerField(min_value=1, max_value=10)
    contact_no = forms.CharField(min_length=10)
    class Meta:
        model = candidates
        fields = ['timestamp','email','name','city','contact_no','age', 'recent_company', 'job', 'current_ctc', 'fixed_component_in_ctc', 'work_experience_in_months', 'work_6_days_a_week', 'willing_to_relocate_mumbai', 'verbal_eng_skill_rate','skills_you_have_worked','industry_you_have_worked','profile_you_like_to_work', 'matters_most_while_selecting_job', 'latest_resume']
