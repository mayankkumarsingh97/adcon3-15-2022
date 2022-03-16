import csv
import re
from common.utils import *
# from common.models import User,Address
# from accounts.models import Tags,Account
# from contacts.models import Contact
# from teams.models import Teams
# from master.models import Observation
import instrument.models
import job.models
from job.models import JobItems
from opportunity.models import Opportunity
import observation.models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms import ModelForm, ModelChoiceField
from django.forms import ImageField
from certificates.models import *
from .models import *
email_regex = "^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$"
from .models import Observation
class ObservationForm(forms.ModelForm):
    cal_observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control','label':'Observation', 'disabled': 'true'}))
    # pages_no = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    job = forms.ModelChoiceField(required=False,queryset=job.models.Jobs.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    jobitems = forms.ModelChoiceField(required=False,queryset=JobItems.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    equipment = forms.ModelMultipleChoiceField(required=False,queryset=instrument.models.instrumentMaster.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    # equipment = forms.ForeignKey(instrumentMaster, related_name="Equipment_Master", blank=True, null=True, on_delete=forms.SET_NULL)
    # obs_table = forms.ManyToManyField(required=False,observationtable, blank=True, null=True, related_name="observation_table")
    calibration_performed_at = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    ref_standard = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    environmental_condition = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    procedure_no = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    # calibrated_by = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    # checked_by = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    # # calibration_procedure_no = forms.ForeignKey("CaliProceNo", related_name="Calibration Procedure No", on_delete=forms.SET_NULL, blank=True, null=True)
    # created_by = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    # created_on = forms.DateTimeField(required=False,widget=forms.TextInput(attrs={'type':'date','class':'form-control'}))
    class Meta:
        model = Observation
        fields="__all__"
        exclude = ('calibrated_by','checked_by', 'created_by', 'created_on')



class observationValueForm(forms.Form):
    company_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    address = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    date_of_calibration = forms.DateTimeField(required=False,widget=forms.TextInput(attrs={'type':'date','class':'form-control'}))
    contact_no = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation =forms.ModelMultipleChoiceField(required=False,queryset=siteColObservation.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))

    class Meta:
        model = siteobservation


class siteColObservationForm(forms.Form):
    cal_no = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    item_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    Ranged = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    LC = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    type = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    Make = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    Sno = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    Location = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    pid = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    unit = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    Engineer = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    customer_sign = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
    observation =forms.ModelMultipleChoiceField(required=False,queryset=observationValue.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))

    class Meta:
        model = siteColObservation


class etItemForm(forms.Form):
    dimension_category = forms.ChoiceField(required=False,choices=dimensioncategory,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    types = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    parameter_range = forms.ChoiceField(required=False,choices=parameters,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    nominal_value = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control nomVal'}))
    nom_1 = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control nomN nom1'}))
    nom_2 = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control nomN nom2'}))
    nom_3 = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control nomN nom3'}))
    nom_4 = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control nomN  nom4'}))
    nom_5 = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control nomN nom5'}))

    value_in = forms.ChoiceField(required=False,choices=parameters,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    observation_1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs1'}))
    observation_2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs2'}))
    observation_3 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs3'}))
    observation_4 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN  obs4'}))
    observation_5 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs5'}))
    observation_6 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs6'}))
    uncertainity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    after_conversion = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    instru_range = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control rangeN'}))
    error = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget = forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = etItem


class MassItemForm(forms.Form):
    dimension_category = forms.ChoiceField(required=False,choices=dimensioncategory,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    types = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    Std_Value_A_1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs1'}))
    uuc_value_b_1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs2'}))
    Std_Value_A1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs3'}))
    reportZ = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN obs4'}))
    linearity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN linearity'}))
    drift = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN drift'}))
    eccentricity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control obsN eccentricity'}))
    uncertainity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    after_conversion = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    error = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget = forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = MassItem


class PressureForm(forms.ModelForm):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    starting_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control ','id':'id_starting_temp'}))
    ending_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control ','id':'id_ending_temp'}))
    pressure_item =forms.ModelMultipleChoiceField(required=False,queryset=etItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertainity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))
    middle_temp = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control ', 'id': 'id_middle_temp'}))
    starting_humidity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control ','id':'id_starting_humadity'}))
    middle_humidity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control ','id':'id_middle_humadity'}))
    ending_humidity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control ','id':'id_ending_humadity'}))
    class Meta:
        model = Pressure
        fields='__all__'

class VolumetricForm(forms.Form):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    starting_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    ending_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    water_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    humidity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    volumetric_item =forms.ModelMultipleChoiceField(required=False,queryset=etItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertainity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = Volumetric

class ETForm(forms.ModelForm):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    temp1 = forms.CharField(required=False, label="Starting Temperature", widget=forms.TextInput(attrs={'type':'text','class':'form-control temp1', 'label': 'Starting temperature'}))
    temp2 = forms.CharField(required=False,label="Middle Temperature",widget=forms.TextInput(attrs={'type':'text','class':'form-control temp2'}))
    temp3 = forms.CharField(required=False,label="End Temperature",widget=forms.TextInput(attrs={'type':'text','class':'form-control temp3'}))

    rh1 = forms.CharField(required=False,label="Starting Humidity",widget=forms.TextInput(attrs={'type':'text','class':'form-control rh1'}))
    rh2 = forms.CharField(required=False,label="Middle Humidity",widget=forms.TextInput(attrs={'type':'text','class':'form-control rh2'}))
    rh3 = forms.CharField(required=False,label="End Humidity",widget=forms.TextInput(attrs={'type':'text','class':'form-control rh3'}))
    ET_item =forms.ModelMultipleChoiceField(required=False,queryset=etItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertainity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = etobservation
        fields='__all__'

class WeighingForm(forms.ModelForm):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    starting_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    ending_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    humidity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    zero_error = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    weighing_item =forms.ModelMultipleChoiceField(required=False,queryset=etItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertain = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = WeighingBalance
        fields = '__all__'
        # fields = ['observation_number','starting_temp','ending_temp','humidity','zero_error','remarks']

class DimensionForm(forms.ModelForm):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    starting_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    ref_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    ending_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    dimension_item =forms.ModelMultipleChoiceField(required=False,queryset=etItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertainity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = dimobservation
        fields='__all__'


class WeightForm(forms.ModelForm):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    starting_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    ending_temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    humidity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    zero_error = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    mass_item =forms.ModelMultipleChoiceField(required=False,queryset=etItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertain = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','data-size':'10','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = Weight
        fields='__all__'


class RPMItemForm(forms.Form):
    value_in = forms.ChoiceField(required=False,choices=ranges,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    value = forms.ChoiceField(required=False,choices=IndicatedValue,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    observation_1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_3 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_4 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_5 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))


    class Meta:
        model = RPMItem

class RPMForm(forms.Form):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    rh = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    rpm_item =forms.ModelMultipleChoiceField(required=False,queryset=RPMItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertain = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget = forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = RPM

class TimeEnergyForm(forms.Form):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    rh = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    TimeEnergy_item =forms.ModelMultipleChoiceField(required=False,queryset=RPMItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertain = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget = forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = TimeEnergy

class ThermalLogDetForm(forms.Form):
    set_temp_value = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    logging_date = forms.DateTimeField(required=False,widget=forms.TextInput(attrs={'type':'date','class':'form-control'}))
    stating_time = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    end_time = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))

    class Meta:
        model = thermalloggingDetails

class ThermalMpForm(forms.Form):
    chamber_size_L1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    chamber_size_L2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    chamber_size_L3 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    location = forms.ChoiceField(required=False,choices=Location,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    n1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n3 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n4 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n5 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n6 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n7 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n8 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n9 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n10 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n11= forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n12= forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n13= forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n14= forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n15= forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    n16= forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))


    class Meta:
        model = ThermalMPItem


class TheramMPForm(forms.Form):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    rh = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    thermalmp_item =forms.ModelMultipleChoiceField(required=False,queryset=ThermalMPItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    logging_details =forms.ModelMultipleChoiceField(required=False,queryset=thermalloggingDetails.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget = forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = ThermalMP

class ThermalItemForm(forms.Form):
    indicated_value = forms.ChoiceField(required=False,choices=Indicated,widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control ','data-style':'select-with-transition'}))
    observation_1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_3 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_4 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    observation_5 = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    sensor_length = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    immersion_depth = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))



    class Meta:
        model = ThermalItem


class ThermalForm(forms.Form):
    observation_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    temp = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    humidity = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    thermal_item =forms.ModelMultipleChoiceField(required=False,queryset=ThermalItem.objects.all(),widget=forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true','multiple':'multiple'}))
    uncertain = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    calibratedBy = forms.ModelChoiceField(required=False,queryset=User.objects.all(),widget = forms.Select(attrs={'type':'select','class':'selectpicker form-control bg-white','data-style':'select-with-transition','id':'select-source','data-live-search':'true'}))
    is_approved = forms.BooleanField(required=False,widget=forms.TextInput(attrs={'type':'checkbox'}))

    class Meta:
        model = Thermal
