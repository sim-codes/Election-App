from django import forms
from .models import PollingUnit, Lga


class PollingUnitForm(forms.ModelForm):
    class Meta:
        model = PollingUnit
        fields = (
            "polling_unit_id",
            "ward_id",
            "lga_id",
            "polling_unit_number",
            "polling_unit_name",
            "polling_unit_description",
            "entered_by_user",
        )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    # self.fields["city"].queryset = City.objects.none()
