from django.db import models
from user.models import User
from uuc.models import *
from srf.models import *
from certificates.models import *

from accounts.models import *
from observation.models import *

import math
from .utils import etItemUncertainty

from accounts.models import *
from observation.models import *
from .utils import stdev
from uncertanity.models import etAccessorySpecification

from uuc.models import *
import math
import statistics
from .utils import WeighingItemUncertainty, WeightItemUncertainty, pr_ItemUncertainty, dimItemUncertainty

from django.db.models.signals import post_save
from django.dispatch import receiver

import math


def roundup(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier



SOAKING_REQUIREMENT = True

class Scope(models.Model):
    choice_clarification = (




#
# pressure_unit_conversion = {"Pascal":{"Pascal":1, "bar":0.00001, "psi":0.000145038,  "kg/cm2": 1.01972e-5, "mmH2o": 0.10, "mmHg": 0.00750062, "inHg" 0.0002953, "mbar": 0.01, "mpa": 1e-6, "kpa": 0.001, "inH2o": 0.00401865, "cmH2o": 0.0101972, "hpa": 0.01 },
#                             "bar" :{"Pascal":100000, "bar":1, "psi":14.503773773, "kg/cm2": 1.01972, "mmH2o": 10197.16, "mmHg": 750.062, "inHg" 29.53,"mbar": 1000, "mpa": 0.1, "kpa": 100, "inH2o": 401.865, "cmH2o": 1019.72, "hpa": 1000 },
#                             "psi" :{"Pascal": 6894.76, "bar":0.0689476, "psi":1, "kg/cm2": 0.070307, "mmH2o": 703.07, "mmHg": 51.7149, "inHg" 2.03602, "mbar": 68.9476, "mpa": 0.00689476, "kpa": 6.89476, "inH2o": 27.7076, "cmH2o": 70.307, "hpa": 68.94757293},
#                              "kg/cm2" :{"Pascal":98066.5, "bar":0.980665, "psi":14.2233, "kg/cm2": 1, "mmH2o": 0.0001, "mmHg": 735.559, "inHg" 28.959, "psi": 14.2233, "mbar": 980.665, "mpa": 0.0980665, "kpa": 98.0665, "inH2o": 394.095, "cmH2o": 1000, "hpa": 0.00102 },
#                              "mmH2o" :{"Pascal":9.80665, "bar":10197.162129, "psi":703.069578, "kg/cm2": 10000, "mmH2o": 1, "mmHg": 0.07, "inHg" 345.31554268, "mbar": 10.197162129779, "mpa": 9.80665E-6, "kpa": 101.97162129779, "inH2o": 25.399999830047, "cmH2o": 0.1, "hpa": 0.098063},
#                              "mmHg" :{"Pascal":133.322, "bar":0.00133322, "psi":0.0193368, "kg/cm2": 0.00135951, "mmH2o": 13.60, "mmHg": 1, "inHg" 0.0393701, "mbar": 1.33322, "mpa": 0.000133322, "kpa": 0.133322, "inH2o": 0.535776, "cmH2o": 1.35951, "hpa": 0.75006156130624},
#                              "inHg" :{"Pascal":3386.39, "bar":0.0338639, "psi":0.491154, "kg/cm2": 0.0345316, "mmH2o": 345.32, "mmHg": 25.4, "inHg" 1, "mbar": 33.8639, "mpa": 0.00338639, "kpa": 3.38639, "inH2o": 13.6087, "cmH2o": 34.5316, "hpa": 33.863},
#                              "mbar" :{"Pascal": 100, "bar":0.001, "psi":0.0145038, "kg/cm2": 0.00101972, "mmH2o": 10.20, "mmHg": 0.750062, "inHg" 0.02953,mbar": 1, "mpa": 0.0001, "kpa": 0.1, "inH2o": 0.401865, "cmH2o": 1.01972, "hpa": 1 },
#                              "mpa" :{"Pascal":1000000, "bar":10, "psi":145.038, "kg/cm2": 10.1972, "mmH2o": 101974.428892, "mmHg": 7500.62, "inHg" 295.3,"mbar": 10000, "mpa": 1, "kpa": 1000, "inH2o": 4018.65, "cmH2o": 10197.2, "hpa": 10000 },
#                              "kpa" :{"Pascal": 1000, "bar":0.01, "psi":0.145038, "kg/cm2": 0.0101972, "mmH2o": 101.97162, "mmHg": 7.50062, "inHg" 0.2953,"mbar": 10, "mpa": 0.001, "kpa": 1, "inH2o": 4.01865, "cmH2o": 10.1974, "hpa": 10 },
#                              "inH2o" :{"Pascal":248.84, "bar":0.0024884, "psi":0.0360912, "kg/cm2":0.00253746, "mmH2o": 25.4, "mmHg": 1.86645, "inHg" 0.0734824,"mbar":2.4884, "mpa": 0.00024884, "kpa": 0.24884, "inH2o": 1, "cmH2o": 2.53746, "hpa": 0.4014630},
#                              "cmH2o" :{"Pascal":98.0665, "bar":0.000980665, "psi":0.0142233, "kg/cm2": 0.001, "mmH2o": 10, "mmHg": 0.735559, "inHg" 0.028959,"mbar": 0.980665, "mpa": 9.80665e-5, "kpa": 0.0980665, "inH2o":0.394095, "cmH2o":1, "hpa": 0.980638},
#                              "hpa" :{"Pascal": 100, "bar":0.001, "psi":0.0145037, "kg/cm2": 0.00102, "mmH2o": 10.20, "mmHg": 0.75006157, "inHg": 0.0295299,"mbar": 1, "mpa": 0.0001, "kpa": 0.1, "inH2o": 0.00401865 "cmH2o": 1.019744, "hpa": 1},
#
#                             }

        ('%', "%"),
        ('μm', "μm"),
        ('mm', "mm"),
        ('s', "s"),
        ('°C', '°C'),
        ('bar', 'bar'),
        ('mg', 'mg'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('Pascal', 'Pascal'),
        ('psi', 'psi'),
        ('kg/cm2', 'kg/cm2'),
        ('mmH2o', 'mmH2o'),
        ('mmHg', 'mmHg'),
        ('mbar', 'mbar'),
        ('inHg', 'inHg'),
        ('mbar', 'mbar'),
        ('mpa', 'mpa'),
        ('kpa', 'kpa'),

        ('inH2o', 'inH2o'),
        ('cmH2o', 'cmH2o'),
        ('hpa', 'hpa'),

    )

    result_type = (
        ('unit', 'unit'),
        ('%', '%'),
    )

    parameters_class = (
        ('RPM', 'RPM'),
        ('Dimension', 'Dimension'),
        ('Thermal', 'Thermal'),
        ('Time_Energy', 'Time_Energy'),
        ('Pressure', 'Pressure'),
        ('Pressure_Multi', 'Pressure_Multi'),
        ('Electro_Technical', 'Electro_Technical'),
        ('Volumetric', 'Volumetric'),
        ('Weight', 'Weight'),
        ('Weighing_Balance', 'Weighing_Balance'),
        ('Thermal_Chamber', 'Thermal_Chamber'),
    )

    s_no = models.IntegerField()
    discipline = models.CharField(verbose_name="Discipline / Group", default=0, blank=True, null=True, max_length=255)
    measurand = models.CharField(verbose_name="Measurand", default=0, blank=True, null=True, max_length=255)
    parameter = models.CharField(max_length=200, blank=True, choices=parameters_class, default="Unit", null=True)
    procedure = models.CharField(verbose_name="Calibration or Measurement Method or Procedure", default=0, blank=True, null=True, max_length=255)
    measurement_range = models.CharField(verbose_name="Measurement Range", default=0, blank=True, null=True, max_length=255)
    lower_capability = models.CharField(verbose_name="CMC Lower", default=0, blank=True, null=True,
                                         max_length=255)
    upper_capability = models.CharField(verbose_name="CMC Upper", default=0, blank=True, null=True,
                                        max_length=255)
    units = models.CharField(max_length=200, blank=True, choices=choice_clarification, default="Unit", null=True)

    result_type = models.CharField(max_length=200, blank=True, choices=result_type, default="Unit", null=True)


    def __str__(self):
        return self.discipline






choice_clarification=(
   ('mm', 'mm'),
   ('C', 'C'),
    ('microns', 'microns'),
    ('kg/cm3', 'kgcm3')


)




# Create your models here.
class Observation(models.Model):
    cal_observation_number = models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    parent_srf = models.ForeignKey("srf.SRFItem", related_name="obs_service", on_delete=models.SET_NULL,blank=True,null=True)
    # pages_no = models.CharField(verbose_name="Number of Pages", blank=True, null=True, max_length=255)
    uucForCalibration = models.ForeignKey("uuc.UUCMaster", related_name="uucObservation", on_delete=models.SET_NULL,blank=True,null=True)
    # job = models.ForeignKey("home.Jobs", related_name="job", on_delete=models.SET_NULL,blank=True,null=True)
    # jobitems = models.ForeignKey("home.JobItems", related_name="jobitems", blank=True, null=True, on_delete=models.SET_NULL)
    # equipment = models.ForeignKey("home.instrumentMaster", related_name="Equipment_Master", blank=True, null=True, on_delete=models.SET_NULL)
    # obs_table = models.ManyToManyField(observationtable, blank=True, null=True, related_name="observation_table")
    location = models.CharField(verbose_name="Location", blank=True, null=True, max_length=255)
    calibration_performed_at = models.CharField(verbose_name="Calibration Performed At", blank=True, null=True, max_length=255)
    calibrated_on = models.DateField(verbose_name="Calibrated On", blank=True, null=True,default=datetime.date.today)
    zero_error = models.CharField(verbose_name="Zero Error", blank=True, null=True, max_length=255)
    due_date = models.DateField(verbose_name="Suggested Due date", blank=True, null=True,default=datetime.date.today)
    units = models.CharField(max_length=200,blank=True,choices=choice_clarification,default="Unit",null=True)
    remarks = models.CharField(verbose_name="Remarks", blank=True, null=True, max_length=255)

    operating_range = models.CharField(verbose_name="Operating Range", blank=True, null=True, max_length=255)
    # environmental_condition = models.CharField(verbose_name="Environmental Condition", blank=True, null=True, max_length=255)
    calibrated_by = models.ForeignKey("user.User", related_name="observation_calibrated_by", on_delete=models.SET_NULL, blank=True, null=True)
    checked_by = models.ForeignKey("user.User", related_name="observation_checked_by", on_delete=models.SET_NULL, blank=True, null=True)
    # observation_details= models.FileField(max_length=800,upload_to="media/",null=True)
    # observation_bugdet= models.FileField(max_length=800,upload_to="media/",null=True)
    # certificate= models.FileField(max_length=800,upload_to="media/",null=True)
    is_saves = models.BooleanField(default=False, verbose_name="Observation Save", blank=True)
    submit = models.BooleanField(default=False, verbose_name="Observation Submit", blank=True)
    rejected= models.BooleanField(default=False, verbose_name="Observation Rejected", blank=True)
    approved= models.BooleanField(default=False, verbose_name="Observation Approved", blank=True)
    rejected_by= models.ForeignKey("user.User", related_name="observation_rejected_by", on_delete=models.SET_NULL, blank=True, null=True)
    mode = models.CharField(verbose_name="Mode", blank=True, null=True, max_length=255)
    instrument = models.ManyToManyField("instrument.instrumentMaster",verbose_name="Master Equipment Used")
    scope = models.ForeignKey(Scope, related_name="scope_nabl", on_delete=models.SET_NULL, blank=True, null=True)


    # calibration_procedure_no = models.CharField(verbose_name="Calibration Procedure No", blank=True, null=True, max_length=255)

    def __str__(self):
        return str(self.cal_observation_number)



class Draft(models.Model):
  ulr = models.CharField(max_length=200,verbose_name="ulr",blank=True,null=True)
  account =models.ForeignKey("accounts.Account",verbose_name="account",related_name="Draft_account", on_delete=models.SET_NULL,blank=True,null=True)
  c_no=models.CharField(max_length=200,verbose_name="c_no",blank=True,null=True)
  issue_date=models.DateField(verbose_name="issue_date",default=datetime.date.today,blank=True,null=True)
  observation=models.ForeignKey("observation.Observation",verbose_name="observation",related_name="Draft_observation" ,on_delete=models.SET_NULL,blank=True,null=True)
  is_certified=models.CharField(max_length=200,verbose_name="is_certified",null=True,blank=True)
  created_by = models.ForeignKey("user.User", related_name="Draft_created_by", on_delete=models.SET_NULL, null=True,blank=True)
  created_on = models.DateTimeField(verbose_name="Created on", default=datetime.date.today,blank=True,null=True)






class siteOrderSheet(models.Model):
    job_no = models.CharField(verbose_name="Job number", blank=True, null=True, max_length=255)
    job_order_date = models.DateField(auto_now_add=True,blank=True, null=True)
    executive_name = models.ForeignKey("user.User", on_delete=models.SET_NULL,related_name="site_executive",blank=True, null=True)
    customer_name = models.CharField(verbose_name="Customer Name", blank=True, null=True, max_length=255)
    customer_address = models.CharField(verbose_name="Customer Address", blank=True, null=True, max_length=600)
    contact = models.ForeignKey("contacts.contact", blank=True, null=True, related_name="site_contact", on_delete=models.SET_NULL)
    contact_no = models.CharField(verbose_name="Contact Number", blank=True, null=True, max_length=255)
    date_of_visit = models.DateField(auto_now_add=True,blank=True, null=True)
    attach_detail = models.CharField(verbose_name="Attach Detail", blank=True, null=True, max_length=255)
    approx_qty = models.CharField(verbose_name="Approx Qty. of Job", blank=True, null=True, max_length=255)
    assigned_to = models.ForeignKey("user.User", on_delete=models.SET_NULL,related_name="site_assigned",blank=True, null=True)
    supporting = models.ForeignKey("user.User", on_delete=models.SET_NULL,related_name="site_supporting",blank=True, null=True)
    instructions = models.TextField(blank=True,null=True,verbose_name="Instructions for Engineer")
    is_approved = models.BooleanField(default=False,verbose_name="Is Active",blank=True)
    created_by = models.ForeignKey("user.User", related_name="site_created_by", on_delete=models.SET_NULL, blank=True, null=True)
    created_on = models.DateTimeField(verbose_name="Quotation Created on", blank=True, null=True, default=datetime.date.today)

    def __str__(self):
        return self.job_no

class observationValue(models.Model):
    Sno = models.CharField(verbose_name="S. No.", blank=True, null=True, max_length=25)
    nominal = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=255)
    observed = models.CharField(verbose_name="Observed Value", blank=True, null=True, max_length=255)
    def __str__(self):
        return self.nominal

class siteColObservation(models.Model):
    cal_no = models.CharField(verbose_name="Calibration Number", blank=True, null=True, max_length=255)
    item_name = models.CharField(verbose_name="Item Name", blank=True, null=True, max_length=255)
    Ranged = models.CharField(verbose_name="Range Name", blank=True, null=True, max_length=255)
    LC = models.CharField(verbose_name="L.C.", blank=True, null=True, max_length=255)
    type = models.CharField(verbose_name="Type", blank=True, null=True, max_length=255)
    Make = models.CharField(verbose_name="Make", blank=True, null=True, max_length=255)
    Sno = models.CharField(verbose_name="S. No.", blank=True, null=True, max_length=255)
    Location = models.CharField(verbose_name="Location", blank=True, null=True, max_length=255)
    pid = models.CharField(verbose_name="P.I/D", blank=True, null=True, max_length=255)
    unit = models.CharField(verbose_name="Unit", blank=True, null=True, max_length=255)
    Engineer = models.ForeignKey("user.User", on_delete=models.SET_NULL,related_name="calib_eng",blank=True, null=True,verbose_name="Calibration Engineer")
    customer_sign = models.ImageField(upload_to='customerSign/',blank=True,null=True,verbose_name="Customer Signature")
    observatiovalue = models.ManyToManyField(observationValue,blank=True,verbose_name="Site Observation value",related_name="calib_observation")

    def __str__(self):
        return self.cal_no

class siteobservation(models.Model):
    company_name =  models.CharField(verbose_name="Company Name", blank=True, null=True, max_length=255)
    address = models.CharField(verbose_name="Customer Address", blank=True, null=True, max_length=600)
    date_of_calibration = models.DateField(auto_now_add=True,blank=True, null=True,verbose_name="Date of Callibration")
    contact_no = models.CharField(verbose_name="Contact Number", blank=True, null=True, max_length=30)
    observation = models.ManyToManyField(siteColObservation,blank=True,verbose_name="Site Colabration Observation",related_name="site_observation")
    created_by = models.ForeignKey("user.User", related_name="site_observation_created_by", on_delete=models.SET_NULL, blank=True, null=True)
    created_on = models.DateTimeField(verbose_name="Created on", blank=True, null=True, default=datetime.date.today)
    def __str__(self):
        return self.company_name




class pressureItem(models.Model):
    nominal_value = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=600)
    nomUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=600)
    instrument = models.ForeignKey("uuc.UUCMaster", verbose_name="Instrument Under Calibration",
                                   related_name="srfInstrument_pressure", on_delete=models.CASCADE, null=True, blank=True)
    middle_temp = models.CharField(verbose_name="Middle Temprature", blank=True, null=True, max_length=600)
    startingTemp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    endingTemp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)



    observation1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    observation2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    observation3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    observation4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    observation5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)
    observation6 = models.CharField(verbose_name="Observation Value 6", blank=True, null=True, max_length=600)
    least_count = models.CharField(verbose_name="Least Count", blank=True, null=True, max_length=600)
    obsUnit = models.CharField(verbose_name="Observation Value Unit", blank=True, null=True, max_length=600)
    after_conversion = models.CharField(verbose_name="Average After Conversion", blank=True, null=True, max_length=600)
    duc_id = models.IntegerField(null=True, blank=True)
    zero_deviation = models.CharField(verbose_name="zero deviation", blank=True, null=True, max_length=600)


    @property
    def temp(self):
        temp1 = float(self.startingTemp)
        temp2 = float(self.endingTemp)
        return temp2-temp1

    def __str__(self):
        return str(self.observation1)

    def get_standard_dev(self):
        duc_id = self.instrument.id
        obs1 = self.observation1
        obs2 = self.observation2
        obs3 = self.observation3
        obs4 = self.observation4
        obs5 = self.observation5
        obs6 = self.observation6
        cal_point = self.nominal_value

        nomUnit = self.nomUnit
        obsUnit = self.obsUnit
        diff = self.zero_deviation
        allinstru_list = self.pressure_items.first().observation.instrument.all()

        least_count = self.least_count
        temp_var = self.temp
        calibration_location = self.pressure_items.first().observation.calibration_performed_at

        try:
            scope = self.pressure_items.first().observation.scope

        except:
            scope = None

        abc = pr_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit, diff, allinstru_list, temp_var, scope, calibration_location)
        iNeed = abc['std']

        return iNeed


    def average(self):

        print('/n', self.id)



        if self.observation3 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            avgpr = (f1 + f2) / 2


        elif self.observation4 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            avgpr = ((f1 + f3) / 2 + f2) / 2

        elif self.observation5 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            f4 = float(self.observation4)
            avgpr = ((f1 + f3) / 2 + (f2 + f4) / 2) / 2

        elif self.observation6 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            f4 = float(self.observation4)
            f5 = float(self.observation5)
            avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4) / 2) / 2


        else:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            f4 = float(self.observation4)
            f5 = float(self.observation5)
            f6 = float(self.observation6)
            avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4 + f6) / 3) / 2



        scope_degits_count = str(float(self.pressure_items.first().pressure_item.last().observation2))
        scope_rounding = scope_degits_count[::-1].find('.')

        avgn = roundup(avgpr, int(scope_rounding))

        avgprn = "{:.{}f}".format(avgn, int(scope_rounding))
        print(self.observation2, scope_degits_count, scope_rounding, avgn, avgprn, "kssdhd hdhd bd dfhbfdhfhdfbdfjfdjnf sdnjdsdjf")

        return avgprn



    def pr_ItemUncertainty(self):

        duc_id = self.instrument.id
        obs1 = self.observation1
        obs2 = self.observation2
        obs3 = self.observation3
        obs4 = self.observation4
        obs5 = self.observation5
        obs6 = self.observation6
        cal_point = self.nominal_value

        nomUnit = self.nomUnit
        obsUnit = self.obsUnit
        diff = self.zero_deviation
        temp_var = self.temp
        try:
            scope = self.pressure_items.first().observation.scope

        except:
            scope = None

        least_count = self.least_count
        allinstru_list = self.pressure_items.first().observation.instrument.all()
        calibration_location = self.pressure_items.first().observation.calibration_performed_at


        abc = pr_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit, diff, allinstru_list, temp_var, scope, calibration_location)

        return abc

    def get_man(self):
        try:
            abc = float(self.nominal_value)
        except:
            abc = self.nominal_value
        return abc




class pressuremultiItem(models.Model):
    nominal_value = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=600)
    nomUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=600)
    instrument = models.ForeignKey("uuc.UUCMaster", verbose_name="Instrument Under Calibration",
                                   related_name="srfInstrument_pressure_multi", on_delete=models.CASCADE, null=True,
                                   blank=True)
    middle_temp = models.CharField(verbose_name="Middle Temprature", blank=True, null=True, max_length=600)
    startingTemp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    endingTemp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)

    observation1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    observation2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    observation3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    observation4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    observation5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)
    observation6 = models.CharField(verbose_name="Observation Value 6", blank=True, null=True, max_length=600)
    least_count = models.CharField(verbose_name="Least Count", blank=True, null=True, max_length=600)
    obsUnit = models.CharField(verbose_name="Observation Value Unit", blank=True, null=True, max_length=600)
    after_conversion = models.CharField(verbose_name="Average After Conversion", blank=True, null=True, max_length=600)
    duc_id = models.IntegerField(null=True, blank=True)
    zero_deviation = models.CharField(verbose_name="zero deviation", blank=True, null=True, max_length=600)
    m_instrument = models.ManyToManyField("instrument.instrumentMaster",verbose_name="Master Equipment Used")
    scope = models.ForeignKey(Scope, related_name="scope_nabl_prmul", on_delete=models.SET_NULL, blank=True, null=True)


    @property
    def temp(self):
        temp1 = float(self.startingTemp)
        temp2 = float(self.endingTemp)
        return temp2 - temp1

    def __str__(self):
        return str(self.observation1)

    def get_standard_dev(self):
        duc_id = self.instrument.id
        obs1 = self.observation1
        obs2 = self.observation2
        obs3 = self.observation3
        obs4 = self.observation4
        obs5 = self.observation5
        obs6 = self.observation6
        cal_point = self.nominal_value

        nomUnit = self.nomUnit
        obsUnit = self.obsUnit
        diff = self.zero_deviation
        allinstru_list = self.instrument.all()

        least_count = self.least_count
        temp_var = self.temp
        calibration_location = self.pressure_items.first().observation.calibration_performed_at

        try:
            scope = self.pressure_items.first().observation.scope

        except:
            scope = None

        abc = pr_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit,
                                 diff, allinstru_list, temp_var, scope, calibration_location)
        iNeed = abc['std']

        return iNeed

    def average(self):

        print('/n', self.id)

        if self.observation3 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            avgpr = (f1 + f2) / 2


        elif self.observation4 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            avgpr = ((f1 + f3) / 2 + f2) / 2

        elif self.observation5 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            f4 = float(self.observation4)
            avgpr = ((f1 + f3) / 2 + (f2 + f4) / 2) / 2

        elif self.observation6 == None:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            f4 = float(self.observation4)
            f5 = float(self.observation5)
            avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4) / 2) / 2


        else:
            f1 = float(self.observation1)
            f2 = float(self.observation2)
            f3 = float(self.observation3)
            f4 = float(self.observation4)
            f5 = float(self.observation5)
            f6 = float(self.observation6)
            avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4 + f6) / 3) / 2

        scope_degits_count = str(float(self.pressure_items.first().pressure_item.last().observation2))
        scope_rounding = scope_degits_count[::-1].find('.')

        avgn = roundup(avgpr, int(scope_rounding))

        avgprn = "{:.{}f}".format(avgn, int(scope_rounding))
        print(self.observation2, scope_degits_count, scope_rounding, avgn, avgprn,
              "kssdhd hdhd bd dfhbfdhfhdfbdfjfdjnf sdnjdsdjf")

        return avgprn

    def pr_ItemUncertainty(self):

        duc_id = self.instrument.id
        obs1 = self.observation1
        obs2 = self.observation2
        obs3 = self.observation3
        obs4 = self.observation4
        obs5 = self.observation5
        obs6 = self.observation6
        cal_point = self.nominal_value

        nomUnit = self.nomUnit
        obsUnit = self.obsUnit
        diff = self.zero_deviation
        temp_var = self.temp
        try:
            scope = self.pressure_items.first().observation.scope

        except:
            scope = None

        least_count = self.least_count
        allinstru_list = self.instrument.all()
        calibration_location = self.pressure_items.first().observation.calibration_performed_at

        abc = pr_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit,
                                 diff, allinstru_list, temp_var, scope, calibration_location)

        return abc

    def get_man(self):
        try:
            abc = float(self.nominal_value)
        except:
            abc = self.nominal_value
        return abc


unit_conversion= {"µV":{"µV":1, "mV":0.001, "V":0.000001},
                  "mV":{"µV":1000, "mV":1, "V":0.001},
                  "V":{"µV":1000000, "mV":1000, "V":1},

                  "µA":{"µA":1, "mA":0.001, "A":0.000001},
                  "mA":{"µA":1000, "mA":1, "A":0.001},
                  "A":{"µA":1000000, "mA":1000, "A":1},

                  "Hz":{"Hz":1, "kHz":0.001},
                  "kHz":{"Hz":1000, "kHz":1},

                  "Ω" : {"Ω":1, "kΩ":0.001, "MΩ":0.000001},
                  "kΩ": {"Ω":1000, "kΩ":1, "MΩ":0.001},
                  "KΩ": {"Ω":1000, "KΩ":1, "MΩ":0.001},
                  "MΩ": {"Ω":1000000, "kΩ":1000, "MΩ":1},

                  "pF" : {"pF":1, "nF":0.001, "µF":0.000001, "mF":0.001},
                  "nF": {"pF":1000, "nF":1, "µF":0.001, "mF":0.000001},
                  "µF": {"pF":1000000, "nF":1000, "µF":1, "mF":0.001},
                  "mF": {"pF":1000000000, "nF":1000000, "µF":1000, "mF":1},

                  }


class etItem(models.Model):
    instrument = models.ForeignKey("uuc.UUCMaster",verbose_name="Instrument Under Calibration", related_name="srfInstrument12", on_delete=models.CASCADE, null=True, blank=True)
    dimension_category = models.CharField(max_length = 200,blank=True, null=True,choices = dimensioncategory,default = 'External')
    type = models.CharField(verbose_name="Type", blank=True, null=True, max_length=600)
    parameter_range = models.CharField(max_length = 200,blank=True, null=True,default = 'Parameter/Range')
    instru_range = models.CharField(verbose_name="Instruments Range", max_length = 200,blank=True, null=True)
    instru_range_unit = models.CharField(verbose_name="Instruments Range Unit", max_length=200, blank=True, null=True)
    nominal_value = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=600)
    value_on = models.CharField(max_length = 200,choices = value,default = 'UUC')
    nom_1 = models.CharField(verbose_name="Nominal Value 1", blank=True, null=True, max_length=600)
    nom_2 = models.CharField(verbose_name="Nominal Value 2", blank=True, null=True, max_length=600)
    nom_3 = models.CharField(verbose_name="Nominal Value 3", blank=True, null=True, max_length=600)
    nom_4 = models.CharField(verbose_name="Nominal Value 4", blank=True, null=True, max_length=600)
    nom_5 = models.CharField(verbose_name="Nominal Value 5", blank=True, null=True, max_length=600)

    observation_1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    observation_2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    observation_3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    observation_4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    observation_5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)
    observation_6 = models.CharField(verbose_name="Observation Value 6", blank=True, null=True, max_length=600)
    after_conversion = models.CharField(verbose_name="Average After Conversion", blank=True, null=True, max_length=600)
    error = models.CharField(verbose_name="Error", blank=True, null=True, max_length=600)
    least_count = models.CharField(null=True, blank=True, max_length=30)
    calculation_unit =  models.CharField(null=True, blank=True, max_length=20)
    duc_id = models.IntegerField(null=True, blank=True)
    stableity_of_the_source = models.CharField(null=True, blank=True, verbose_name="Stableity of the Source", max_length=10)
    accessoriesmaster = models.ManyToManyField("instrument.AccessoriesMaster",
                                               verbose_name="Accessories Equipment Used", blank=True, null=True)

    lead_resistance  = models.CharField(verbose_name="Lead Resistance", blank=True, null=True, max_length=600)
    current_value = models.CharField(verbose_name="Current Num Val", blank=True, null=True, max_length=600)
    current_ratio = models.CharField(verbose_name="Current Dnom Val", blank=True, null=True, max_length=600)
    def average(self):
        digit_count = str(self.observation_1)
        rounding = digit_count[::-1].find('.')
        itemNeed = (float(self.observation_1) + float(self.observation_2) + float(self.observation_3) + float(self.observation_4) + float(self.observation_5))
        itemNeed = itemNeed / 5

        return roundup(itemNeed, int(rounding))

    def error(self):
        itemNeed = (float(self.observation_1) + float(self.observation_2) + float(self.observation_3) + float(self.observation_4) + float(self.observation_5))
        avgObs = itemNeed / 5
        nominal_value = float(self.nominal_value)
        valN = nominal_value-avgObs
        return valN

    def etItemUncertainty(self):
        duc_id = self.duc_id
        lc_duc = self.least_count
        lc_duc_unit_parameter = self.type
        cal_point = self.nominal_value
        cal_point_unit = self.calculation_unit
        # obs_point_unit =
        obs1 = self.observation_1
        obs2 = self.observation_2
        obs3 = self.observation_3
        obs4 = self.observation_4
        obs5 = self.observation_5
        instru_range = self.instru_range
        try:
            scope = self.et_items.first().observation.scope

        except:
            scope = None

        try:
            instrument_accessories = self.accessoriesmaster.first().id
        except:
            instrument_accessories = None


        instru_range_unit = self.instru_range_unit
        obs_point_unit = None
        allinstru_list = self.et_items.first().observation.instrument.all()

        try:
            stableity_of_the_source = float(self.stableity_of_the_source)
        except:
            stableity_of_the_source = 0


        abc = etItemUncertainty(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1,
                                obs2,
                                obs3, obs4, obs5, instru_range, instru_range_unit, allinstru_list, instrument_accessories, stableity_of_the_source, scope)

        return abc



    def __str__(self):
        return (str(self.nominal_value) + str(self.type))



class etobservation(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="et_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    temp1 = models.CharField(verbose_name="Temprature Start", blank=True, null=True, max_length=600)
    temp2 = models.CharField(verbose_name="Temprature Middle", blank=True, null=True, max_length=600)
    temp3 = models.CharField(verbose_name="Temprature End", blank=True, null=True, max_length=600)
    temp4 = models.CharField(verbose_name="Temprature Avg", blank=True, null=True, max_length=600)
    rh1 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    rh2 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    rh3 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    etItem = models.ManyToManyField(etItem, related_name="et_items", blank=True)
    uncertainity = models.CharField(verbose_name="Uncertainity in %", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="etcalibrated",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)
    def __str__(self):
        return str(self.observation_number)
    def uncertsinty2(self):
        return "Yes"
    def avgtemp(self):
        try:
            return roundup(float(float(self.temp1)+ float(self.temp2) + float(self.temp3))/3, 2)
        except:
            return "23.3"
    def avgrh(self):
        try:
            return roundup(float(float(self.rh1)+ float(self.rh2) + float(self.rh3))/3, 2)
        except:
            return 51

    def max_vale(self):

        itemN = self.etItem.all().values('type').distinct()
        print('---------------------------------------', itemN)
        pritems = self.etItem.all()
        abd = {}

        for items in itemN:
            abc = {}
            for item in pritems:

                if item.type == items['type']:
                    abc[item.id] = item.get_standard_dev()

            max_pr_un = max(abc, key=abc.get)
            abd[items['type']] = etItem.objects.get(id=max_pr_un)

        print(abd)
        return abd




class dimobservation(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="dim_observations", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    temp1 = models.CharField(verbose_name="Temprature Start", blank=True, null=True, max_length=600)
    temp2 = models.CharField(verbose_name="Temprature Middle", blank=True, null=True, max_length=600)
    temp3 = models.CharField(verbose_name="Temprature End", blank=True, null=True, max_length=600)
    # temp4 = models.CharField(verbose_name="Temprature Avg", blank=True, null=True, max_length=600)
    # rh1 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    # rh2 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    # rh3 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    dimItem = models.ManyToManyField("observation.dimItem", related_name="dim_item", blank=True)
    uncertainity = models.CharField(verbose_name="Uncertainity in %", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="dimcalibrated",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)
    def __str__(self):
        return str(self.observation_number)
    def uncertsinty2(self):
        return "Yes"


class dimItem(models.Model):
    instrument = models.ForeignKey("uuc.UUCMaster",verbose_name="Instrument Under Calibration", related_name="srfInstrumentdim", on_delete=models.CASCADE, null=True, blank=True)
    dimension_category = models.CharField(max_length = 200,blank=True, null=True,choices = dimensioncategory,default = 'External')
    type = models.CharField(verbose_name="Type", blank=True, null=True, max_length=600)
    parameter_range = models.CharField(max_length = 200,blank=True, null=True,default = 'Parameter/Range')
    nominal_value = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=600)
    nomUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=600)
    value_on = models.CharField(max_length = 200,choices = value,default = 'UUC')
    observation_1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    observation_2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    observation_3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    observation_4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    observation_5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)
    obsUnit = models.CharField(verbose_name="Observation Value Unit", blank=True, null=True, max_length=600)
    # observation_6 = models.CharField(verbose_name="Observation Value 6", blank=True, null=True, max_length=600)
    after_conversion = models.CharField(verbose_name="Average After Conversion", blank=True, null=True, max_length=600)
    error = models.CharField(verbose_name="Error", blank=True, null=True, max_length=600)
    least_count = models.CharField(null=True, blank=True, max_length=3)

    method = models.CharField(null=True, blank=True, max_length=3)
    calculation_unit =  models.CharField(null=True, blank=True, max_length=20)
    duc_id = models.IntegerField(null=True, blank=True)

    def average(self):
        itemNeed = (float(self.observation_1) + float(self.observation_2) + float(self.observation_3) + float(
            self.observation_4) + float(self.observation_5))
        itemNeed = roundup(itemNeed, 2)
        return itemNeed / 5

    def method_dimunceratinity(self):
        duc_id = self.duc_id
        lc_duc = self.least_count
        lc_duc_unit_parameter = self.type
        cal_point = self.nominal_value
        cal_point_unit = self.calculation_unit
        # obs_point_unit =
        obs1 = self.observation_1
        obs2 = self.observation_2
        obs3 = self.observation_3
        obs4 = self.observation_4
        obs5 = self.observation_5
        obs_point_unit = None
        rangeP = None
        tempP = None
        temp = None

        least_count = self.least_count

        nomUnit = self.nomUnit
        obsUnit = self.obsUnit

        abc = dimItemUncertainty(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1,
                                 obs2, obs3, obs4, obs5, rangeP, tempP, least_count, temp, nomUnit, obsUnit)
        print('fhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', abc)
        return abc


    def dimItemUncertainty(self):



        duc_id = self.duc_id
        lc_duc = self.least_count
        lc_duc_unit_parameter = self.type
        cal_point = self.nominal_value
        cal_point_unit = self.calculation_unit
        # obs_point_unit =
        obs1 = self.observation_1
        obs2 = self.observation_2
        obs3 = self.observation_3
        obs4= self.observation_4
        obs5= self.observation_5

        duc = UUCMaster.objects.get(id=duc_id)
        if lc_duc:
            pass
        else:
            lc_duc = ''
        obs1 = float(obs1)
        obs2 = float(obs2)
        obs3 = float(obs3)
        obs4 = float(obs4)
        obs5 = float(obs5)
        obs1 = roundup(obs1, 2)
        listobserve = [obs1, obs2, obs3, obs4, obs5]
        ua = stdev(listobserve, ddof=1)
        ua = ua / math.sqrt(5)

        # cal_point_unit='A'

        ub1 = 0
        ub2 = 0
        ub3 = 0
        uc = 0
        veff = 0
        UmV = 0
        Up = 0
        ub4 = 0
        duc_unc = UUCMaster.objects.get(id=duc_id)

        for items in duc_unc.master_uncertainty.uc.all():
            if items.parameters == 'accuracy':
                unc_need = 0
                abc = items.instrument.et_accessory_detail.all()
                # print(abc)
                for itemd in abc:
                    # print(itemd.category)
                    # print("CAL POINT", items.distribution)
                    # print("CAL ", cal_point_unit)
                    if itemd.type == cal_point and itemd.info == cal_point_unit and itemd.category == lc_duc_unit_parameter:
                        abd = itemd.accuracy
                        # print(abd)
                        ub4 = float(abd)
                        # print(ub4)
                        if items.distribution == 'Normal':
                            myV = 2
                        elif items.distribution == 'Rectangular':
                            myV = math.sqrt(3)
                        ub4 = ub4 / myV

                        # ub1 = format(ub1, 6)
                        # ub3 = format(ub3, '.6f')
        # print(ub4)
        # print("THIS")
        for items in duc_unc.master_uncertainty.ub.all():

            if items.parameters == 'uncertainty':
                unc_need = 0
                # print("items-------")
                abc = items.instrument.et_master_detail.all()

                for itemd in abc:
                    # if itemd.type == '1000':
                    #     print("Vasu Is a1 ", itemd.type, cal_point)
                    #     # print("Vasu Is a2 ", itemd.info, cal_point_unit)
                    #     # print("Vasu Is a5 ", itemd.category, lc_duc_unit_parameter)

                    if itemd.type == cal_point and itemd.info == cal_point_unit and itemd.category == lc_duc_unit_parameter:
                        abd = itemd.uncertainty
                        # print("abc", abd)
                        ub1 = float(abd) / 2

                        ub1 = roundup(float(ub1), 6)

            elif items.parameters == 'lc':
                if items.distribution == 'Normal':
                    myV = 2
                elif items.distribution == 'Rectangular':
                    myV = math.sqrt(3)

                # print(lc_duc)
                # print("P")
                lc = float(lc_duc) / 2
                ub2 = lc / myV
                # ub2 = format(ub2,'.6f')



            elif items.parameters == 'accuracy':
                unc_need = 0
                abc = items.instrument.et_master_detail.all()
                for itemd in abc:
                    if itemd.type == cal_point and itemd.info == cal_point_unit and itemd.category == lc_duc_unit_parameter:
                        abd = itemd.accuracy
                        ub3 = float(abd)

                        if items.distribution == 'Normal':
                            myV = 2
                        elif items.distribution == 'Rectangular':
                            myV = math.sqrt(3)
                        # print(myV)
                        ub3 = ub3 / myV


        sumINeed = pow(ua, 2) + pow(ub1, 2) + pow(ub2, 2) + pow(ub3, 2) + pow(ub4, 2)

        # print(sumINeed)
        uc = math.sqrt(sumINeed)
        # print("uc")
        # print(uc)

        veff = pow(uc, 4)
        if ua != 0:
            veff = veff * 4 / pow(ua, 4)
        else:
            veff = 'NA'
        # print("Veff")
        # print(veff)

        UmV = uc * 2
        # print("umv")
        # print(UmV)
        Up = UmV * 100 / float(cal_point)

        # print("uP")
        # print(Up)
        UmV = roundup(UmV, 5)
        totalDict['U']=UmV
        totalDict['Up']=Up
        totalDict['uc']=uc
        totalDict['veff']=veff

        return totalDict
        # return {'U': UmV, 'Up': Up, 'ua': ua, 'ub1': ub1, 'ub2': ub2, 'ub3': ub3, 'uc': uc, 'veff': veff}

        # elif items.parameters=='accuracy':
        #     print("accuracy")
        # elif items.parameters=='accuracy':
        #     print("accuracy")
        # elif items.parameters=='accuracy':
        #     print("accuracy")
        # elif items.parameters=='accuracy':
        #     print("accuracy")
        # elif items.parameters=='accuracy':
        #     print("accuracy")





    def __str__(self):
        return str(self.nominal_value)

from django.db.models import Max

class Pressure(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="pressure_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    least_count = models.CharField(verbose_name="Least Count", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    pressure_item = models.ManyToManyField(pressureItem, related_name="pressure_items", blank=True)
    temp1 = models.CharField(verbose_name="Temprature Start", blank=True, null=True, max_length=600)
    #we are using Temp2
    temp2 = models.CharField(verbose_name="Temprature Middle", blank=True, null=True, max_length=600)
    #alert #alert
    temp3 = models.CharField(verbose_name="Temprature End", blank=True, null=True, max_length=600)
    temp4 = models.CharField(verbose_name="Temprature Avg", blank=True, null=True, max_length=600)
    rh1 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    rh2 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    rh3 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    uncertainity = models.CharField(verbose_name="Uncertainity in %", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="prcalibrated",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)
    def __str__(self):
        return str(self.observation_number)+'ashhu'
    def avgtemp(self):
        try:
            return roundup(float(float(self.starting_temp)+ float(self.ending_temp))/2, 2)
        except:
            return "23.5"
    def avgrh(self):
        try:
            return roundup(float(float(self.rh1) + float(self.rh3))/2, 2)
        except:
            return "55"
    def max_vale(self):
        pritems = self.pressure_item.all()
        abc = {}
        for item in pritems:
            abc[item.id] = item.get_standard_dev()

        max_pr_un = max(abc, key=abc.get)

        return max_pr_un



class PressureMulti(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="pressure_multi_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    least_count = models.CharField(verbose_name="Least Count", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    pressuremulti_item = models.ManyToManyField(pressuremultiItem, related_name="pressure_multi_items", blank=True)
    temp1 = models.CharField(verbose_name="Temprature Start", blank=True, null=True, max_length=600)
    #we are using Temp2
    temp2 = models.CharField(verbose_name="Temprature Middle", blank=True, null=True, max_length=600)
    #alert #alert
    temp3 = models.CharField(verbose_name="Temprature End", blank=True, null=True, max_length=600)
    temp4 = models.CharField(verbose_name="Temprature Avg", blank=True, null=True, max_length=600)
    rh1 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    rh2 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    rh3 = models.CharField(verbose_name="Rh", blank=True, null=True, max_length=600)
    uncertainity = models.CharField(verbose_name="Uncertainity in %", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="pr_multicalibrated",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)
    def __str__(self):
        return str(self.observation_number)+'ashhu'
    def avgtemp(self):
        try:
            return roundup(float(float(self.temp1)+ float(self.temp2) + float(self.temp3))/3, 2)
        except:
            return "23.5"
    def avgrh(self):
        try:
            return roundup(float(float(self.rh1)+ float(self.rh2) + float(self.rh3))/3, 2)
        except:
            return "55"
    def max_vale(self):
        pritems = self.pressure_item.all()
        abc = {}
        for item in pritems:
            abc[item.id] = item.get_standard_dev()

        max_pr_un = max(abc, key=abc.get)

        return max_pr_un


class Volumetric(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="volumetric_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    water_temp = models.CharField(verbose_name="Water Temprature", blank=True, null=True, max_length=600)
    humidity = models.CharField(verbose_name="Humidity", blank=True, null=True, max_length=600)
    volumetric_item = models.ManyToManyField(etItem, related_name="volumetric_items", blank=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="vocalibratedby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)

    def __str__(self):
        return self.observation_number



#
#
# class WeighingBalanceItem(models.Model):
#     instrument = models.ForeignKey("uuc.UUCMaster",verbose_name="Instrument Under Calibration", related_name="srfInstrumentweighing", on_delete=models.CASCADE, null=True, blank=True)
#     nominal_value = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=600)
#     nomUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=60)
#     value_on = models.CharField(max_length = 200,choices = value,default = 'UUC')
#     observation_1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
#     observation_2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
#     observation_3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
#     observation_4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
#     observation_5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)
#     obsUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=60)
#
#     HR1 = models.CharField(verbose_name="HR1", blank=True, null=True, max_length=600)
#     HR2 = models.CharField(verbose_name="HR2", blank=True, null=True, max_length=600)
#     HR3 = models.CharField(verbose_name="HR3", blank=True, null=True, max_length=600)
#     HR4 = models.CharField(verbose_name="HR4", blank=True, null=True, max_length=600)
#     HR5 = models.CharField(verbose_name="HR5", blank=True, null=True, max_length=600)
#     HR6 = models.CharField(verbose_name="HR6", blank=True, null=True, max_length=600)
#     HR7 = models.CharField(verbose_name="HR7", blank=True, null=True, max_length=600)
#     HR8 = models.CharField(verbose_name="HR8", blank=True, null=True, max_length=600)
#     HR9 = models.CharField(verbose_name="HR9", blank=True, null=True, max_length=600)
#     HR10 = models.CharField(verbose_name="HR10", blank=True, null=True, max_length=600)
#
#     FR1 = models.CharField(verbose_name="FR1", blank=True, null=True, max_length=600)
#     FR2 = models.CharField(verbose_name="FR2", blank=True, null=True, max_length=600)
#     FR3 = models.CharField(verbose_name="FR3", blank=True, null=True, max_length=600)
#     FR4 = models.CharField(verbose_name="FR4", blank=True, null=True, max_length=600)
#     FR5 = models.CharField(verbose_name="FR5", blank=True, null=True, max_length=600)
#     FR6 = models.CharField(verbose_name="FR6", blank=True, null=True, max_length=600)
#     FR7 = models.CharField(verbose_name="FR7", blank=True, null=True, max_length=600)
#     FR8 = models.CharField(verbose_name="FR8", blank=True, null=True, max_length=600)
#     FR9 = models.CharField(verbose_name="FR9", blank=True, null=True, max_length=600)
#     FR10 = models.CharField(verbose_name="FR10", blank=True, null=True, max_length=600)
#
#     EA = models.CharField(verbose_name="EA", blank=True, null=True, max_length=600)
#     EB = models.CharField(verbose_name="EB", blank=True, null=True, max_length=600)
#     EC = models.CharField(verbose_name="EC", blank=True, null=True, max_length=600)
#     ED = models.CharField(verbose_name="ED", blank=True, null=True, max_length=600)
#     EO = models.CharField(verbose_name="EO", blank=True, null=True, max_length=600)
#
#
#     # observation_6 = models.CharField(verbose_name="Observation Value 6", blank=True, null=True, max_length=600)
#     after_conversion = models.CharField(verbose_name="Average After Conversion", blank=True, null=True, max_length=600)
#     error = models.CharField(verbose_name="Error", blank=True, null=True, max_length=600)
#     least_count = models.CharField(null=True, blank=True, max_length=3)
#     duc_id = models.IntegerField(null=True, blank=True)
#
#     # def __str__(self):
#         # return self.observation_1
#
#     def average(self):
#         accVal = float(self.observation_1) +float(self.observation_2) + float(self.observation_3)+float(self.observation_4) +float(self.observation_5)
#         needVal = accVal/5
#         return needVal
#
#     def uuc_std(self):
#         nomVal = float(self.nominal_value)
#
#         accVal = float(self.observation_1) + float(self.observation_2) + float(self.observation_3) + float(
#             self.observation_4) + float(self.observation_5)
#
#         avgVal = accVal / 5
#
#         valNeed = abs(nomVal-avgVal)
#         return valNeed
#
#
#
#     def weighinguncertain(self):
#         duc_id =self.duc_id
#         lc_duc = self.least_count
#         cal_point = self.nominal_value
#
#         obs1 = self.observation_1
#         obs2 = self.observation_2
#         obs3 = self.observation_3
#         obs4 = self.observation_4
#         obs5 = self.observation_5
#
#         nomUnit = self.nomUnit
#         obsUnit = self.obsUnit
#
#         temp=1
#
#         HR1 = self.HR1
#         HR2 = self.HR2
#         HR3 = self.HR3
#         HR4 = self.HR4
#         HR5 = self.HR5
#         HR6 = self.HR6
#         HR7 = self.HR7
#         HR8 = self.HR8
#         HR9 = self.HR9
#         HR10 = self.HR10
#         FR1 = self.FR1
#         FR2 = self.FR2
#         FR3 = self.FR3
#         FR4 = self.FR4
#         FR5 = self.FR5
#         FR6 = self.FR6
#         FR7 = self.FR7
#         FR8 = self.FR8
#         FR9 = self.FR9
#         FR10 = self.FR10
#
#         EA = float(self.EA)
#         EB = float(self.EB)
#         EC = float(self.EC)
#         ED = float(self.ED)
#         EO = float(self.EO)
#         list = [EA,EB,EC,ED,EO]
#
#         maxx = max(list)
#         minn = min(list)
#         eccentricity_max_min = str(maxx-minn)
#
#         abc = WeighingItemUncertainty(duc_id,lc_duc, cal_point, obs1, obs2, obs3, obs4, obs5, nomUnit, obsUnit, temp, eccentricity_max_min, HR1, HR2, HR3, HR4, HR5, HR6, HR7, HR8, HR9, HR10, FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9,FR10)
#         return abc

class WeighingBalanceItem(models.Model):
    instrument = models.ForeignKey("uuc.UUCMaster",verbose_name="Instrument Under Calibration", related_name="srfInstrumentweighing", on_delete=models.CASCADE, null=True, blank=True)
    nominal_value = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=600)
    nomUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=60)
    value_on = models.CharField(max_length = 200,choices = value,default = 'UUC')
    observation_1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    observation_2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    observation_3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    observation_4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    obsUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=60)
    master_weight_item = models.ManyToManyField("certificates.WeightCertificate",
                                                verbose_name="Weight Certificate Item")

    halfload_value = models.CharField(verbose_name="Half Load", blank=True, null=True, max_length=600)
    halfloadUnit = models.CharField(verbose_name="Half Unit", blank=True, null=True, max_length=60)

    HR1 = models.CharField(verbose_name="HR1", blank=True, null=True, max_length=600)
    HR2 = models.CharField(verbose_name="HR2", blank=True, null=True, max_length=600)
    HR3 = models.CharField(verbose_name="HR3", blank=True, null=True, max_length=600)
    HR4 = models.CharField(verbose_name="HR4", blank=True, null=True, max_length=600)
    HR5 = models.CharField(verbose_name="HR5", blank=True, null=True, max_length=600)
    HR6 = models.CharField(verbose_name="HR6", blank=True, null=True, max_length=600)
    HR7 = models.CharField(verbose_name="HR7", blank=True, null=True, max_length=600)
    HR8 = models.CharField(verbose_name="HR8", blank=True, null=True, max_length=600)
    HR9 = models.CharField(verbose_name="HR9", blank=True, null=True, max_length=600)
    HR10 = models.CharField(verbose_name="HR10", blank=True, null=True, max_length=600)

    HR11 = models.CharField(verbose_name="HR11", blank=True, null=True, max_length=600)
    HR12 = models.CharField(verbose_name="HR12", blank=True, null=True, max_length=600)
    HR13 = models.CharField(verbose_name="HR13", blank=True, null=True, max_length=600)
    HR14 = models.CharField(verbose_name="HR14", blank=True, null=True, max_length=600)
    HR15 = models.CharField(verbose_name="HR15", blank=True, null=True, max_length=600)
    HR16 = models.CharField(verbose_name="HR16", blank=True, null=True, max_length=600)
    HR17 = models.CharField(verbose_name="HR17", blank=True, null=True, max_length=600)
    HR18 = models.CharField(verbose_name="HR18", blank=True, null=True, max_length=600)
    HR19 = models.CharField(verbose_name="HR19", blank=True, null=True, max_length=600)
    HR20 = models.CharField(verbose_name="HR20", blank=True, null=True, max_length=600)

    fulload_value = models.CharField(verbose_name="Full Load", blank=True, null=True, max_length=600)
    fullloadUnit = models.CharField(verbose_name="Full Load Unit", blank=True, null=True, max_length=60)

    FR1 = models.CharField(verbose_name="FR1", blank=True, null=True, max_length=600)
    FR2 = models.CharField(verbose_name="FR2", blank=True, null=True, max_length=600)
    FR3 = models.CharField(verbose_name="FR3", blank=True, null=True, max_length=600)
    FR4 = models.CharField(verbose_name="FR4", blank=True, null=True, max_length=600)
    FR5 = models.CharField(verbose_name="FR5", blank=True, null=True, max_length=600)
    FR6 = models.CharField(verbose_name="FR6", blank=True, null=True, max_length=600)
    FR7 = models.CharField(verbose_name="FR7", blank=True, null=True, max_length=600)
    FR8 = models.CharField(verbose_name="FR8", blank=True, null=True, max_length=600)
    FR9 = models.CharField(verbose_name="FR9", blank=True, null=True, max_length=600)
    FR10 = models.CharField(verbose_name="FR10", blank=True, null=True, max_length=600)

    FR11 = models.CharField(verbose_name="FR11", blank=True, null=True, max_length=600)
    FR12 = models.CharField(verbose_name="FR12", blank=True, null=True, max_length=600)
    FR13 = models.CharField(verbose_name="FR13", blank=True, null=True, max_length=600)
    FR14 = models.CharField(verbose_name="FR14", blank=True, null=True, max_length=600)
    FR15 = models.CharField(verbose_name="FR15", blank=True, null=True, max_length=600)
    FR16 = models.CharField(verbose_name="FR16", blank=True, null=True, max_length=600)
    FR17 = models.CharField(verbose_name="FR17", blank=True, null=True, max_length=600)
    FR18 = models.CharField(verbose_name="FR18", blank=True, null=True, max_length=600)
    FR19 = models.CharField(verbose_name="FR19", blank=True, null=True, max_length=600)
    FR20 = models.CharField(verbose_name="FR20", blank=True, null=True, max_length=600)

    eccentricity_loading = models.CharField(verbose_name="Eccentricity Loading", blank=True, null=True, max_length=600)
    E1 = models.CharField(verbose_name="EA", blank=True, null=True, max_length=600)
    E2 = models.CharField(verbose_name="EB", blank=True, null=True, max_length=600)
    E3 = models.CharField(verbose_name="EC", blank=True, null=True, max_length=600)
    E4 = models.CharField(verbose_name="ED", blank=True, null=True, max_length=600)
    E5 = models.CharField(verbose_name="EE", blank=True, null=True, max_length=600)
    E6 = models.CharField(verbose_name="EF", blank=True, null=True, max_length=600)
    E7 = models.CharField(verbose_name="EG", blank=True, null=True, max_length=600)
    E8 = models.CharField(verbose_name="EH", blank=True, null=True, max_length=600)
    E9 = models.CharField(verbose_name="EI", blank=True, null=True, max_length=600)
    E10 = models.CharField(verbose_name="EJ", blank=True, null=True, max_length=600)
    E11= models.CharField(verbose_name="EK", blank=True, null=True, max_length=600)
    eccentricityUnit = models.CharField(verbose_name="Eccentricity Unit", blank=True, null=True, max_length=60)


    # observation_6 = models.CharField(verbose_name="Observation Value 6", blank=True, null=True, max_length=600)
    after_conversion = models.CharField(verbose_name="Average After Conversion", blank=True, null=True, max_length=600)
    error = models.CharField(verbose_name="Error", blank=True, null=True, max_length=600)
    least_count = models.CharField(null=True, blank=True, max_length=3)
    duc_id = models.IntegerField(null=True, blank=True)

    
    def mean(self):
        total={}
        e1=float(self.E1) + float(self.E6) + float(self.E11)
        e2=float(self.E2) + float(self.E10)
        e3=float(self.E3) + float(self.E9)
        e4=float(self.E4) + float(self.E8)
        e5=float(self.E5) + float(self.E7)


        Lmen3=e4/2
        Lmen2=e2/2
        Lmen1= e1/3
        Lmen4=e3/2
        Lmen5=e5/2
        h1=Lmen1 - Lmen2
        h2=Lmen1 - Lmen3
        h3=Lmen1 - Lmen4
        h4=Lmen1 - Lmen5

        total['h1']=h1
        total['h2']=h2
        total['h3']=h3
        total['h4']=h4
        
        total['Lmen1']=Lmen1
        total['Lmen2']=Lmen2
        total['Lmen3']=Lmen3
        total['Lmen4']=Lmen4
        total['Lmen5']=Lmen5

        return total


    def DiffHalfLoad(self):
        total={}

        hd1= float(self.HR1) - float(self.HR11)
        total['hd1'] = hd1

        hd2= float(self.HR2) - float(self.HR12)
        total['hd2'] = hd2

        hd3= float(self.HR3) - float(self.HR13)
        total['hd3'] = hd3

        hd4= float(self.HR4) - float(self.HR14)
        total['hd4'] = hd4

        hd5= float(self.HR5) - float(self.HR15)
        total['hd5'] = hd5

        hd6= float(self.HR6) - float(self.HR16)
        total['hd6'] = hd6

        hd7= float(self.HR7) - float(self.HR17)
        total['hd7'] = hd7

        hd8= float(self.HR8) - float(self.HR18)
        total['hd8'] = hd8

        hd9= float(self.HR9) - float(self.HR19)
        total['hd9'] = hd9

        hd10= float(self.HR10) - float(self.HR20)
        total['hd10'] = hd10

     
        
        return total

    def DiffFullLoad(self):
        total={}

        fd1= float(self.FR1) - float(self.FR11)
        total['fd1'] = fd1

        fd2= float(self.FR2) - float(self.FR12)
        total['fd2'] = fd2

        fd3= float(self.FR3) - float(self.FR13)
        total['fd3'] = fd3

        fd4= float(self.FR4) - float(self.FR14)
        total['fd4'] = fd4

        fd5= float(self.FR5) - float(self.FR15)
        total['fd5'] = fd5

        fd6= float(self.FR6) - float(self.FR16)
        total['fd6'] = fd6

        fd7= float(self.FR7) - float(self.FR17)
        total['fd7'] = fd7

        fd8= float(self.FR8) - float(self.FR18)
        total['fd8'] = fd8

        fd9= float(self.FR9) - float(self.FR19)
        total['fd9'] = fd9

        fd10= float(self.FR10) - float(self.FR20)
        total['fd10'] = fd10

     
        
        return total

    def avg(self):
        obs1=float(self.observation_1)
        obs2=float(self.observation_2)
        obs3=float(self.observation_3)
        obs4=float(self.observation_4)
        tot=obs1+obs2+obs3+obs4
        avg=tot/4

        return avg






        







class WeighingBalance(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="weighingbalance_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    humidity = models.CharField(verbose_name="Humidity", blank=True, null=True, max_length=600)
    zero_error = models.CharField(verbose_name="Zero Error", blank=True, null=True, max_length=600)
    weighing_item = models.ManyToManyField(WeighingBalanceItem, related_name="weighing_item", blank=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    zero_error = models.CharField(verbose_name="Zero Error", blank=True, null=True, max_length=600)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="weighingcalibratedby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)

    # def __str__(self):
    #     return self.starting_temp


























class Dimension(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="dimension_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    middle_temp = models.CharField(verbose_name="Middle Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    dimension_item = models.ManyToManyField(etItem, related_name="dimension_items", blank=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="dicalibratedby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)

    def __str__(self):
        return self.observation_number



class MassItem(models.Model):
    instrument = models.ForeignKey("uuc.UUCMaster",verbose_name="Instrument Under Calibration", related_name="srfInstrument13", on_delete=models.CASCADE, null=True, blank=True)
    dimension_category = models.CharField(max_length = 200,blank=True, null=True,choices = dimensioncategory,default = 'External')
    type = models.CharField(verbose_name="Type", blank=True, null=True, max_length=600)
    obs11 = models.CharField(verbose_name="obs11", blank=True, null=True, max_length=600)
    obs12 = models.CharField(verbose_name="obs12", blank=True, null=True, max_length=600)
    obs13 = models.CharField(verbose_name="obs13", blank=True, null=True, max_length=600)
    obs14 = models.CharField(verbose_name="obs14", blank=True, null=True, max_length=600)
    obs15 = models.CharField(verbose_name="obs15", blank=True, null=True, max_length=600)
    obs21 = models.CharField(verbose_name="obs21", blank=True, null=True, max_length=600)
    obs22 = models.CharField(verbose_name="obs22", blank=True, null=True, max_length=600)
    obs23 = models.CharField(verbose_name="obs23", blank=True, null=True, max_length=600)
    obs24 = models.CharField(verbose_name="obs24", blank=True, null=True, max_length=600)
    obs25 = models.CharField(verbose_name="obs25", blank=True, null=True, max_length=600)
    obs31 = models.CharField(verbose_name="obs31", blank=True, null=True, max_length=600)
    obs32 = models.CharField(verbose_name="obs32", blank=True, null=True, max_length=600)
    obs33 = models.CharField(verbose_name="obs33", blank=True, null=True, max_length=600)
    obs34 = models.CharField(verbose_name="obs34", blank=True, null=True, max_length=600)
    obs35 = models.CharField(verbose_name="obs35", blank=True, null=True, max_length=600)
    obs41 = models.CharField(verbose_name="obs41", blank=True, null=True, max_length=600)
    obs42 = models.CharField(verbose_name="obs42", blank=True, null=True, max_length=600)
    obs43 = models.CharField(verbose_name="obs43", blank=True, null=True, max_length=600)
    obs44 = models.CharField(verbose_name="obs44", blank=True, null=True, max_length=600)
    obs45 = models.CharField(verbose_name="obs45", blank=True, null=True, max_length=600)
    obs1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    obs2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    obs3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    obs4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    obs5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)
    obsUnit = models.CharField(verbose_name="Observation Value Unit", blank=True, null=True, max_length=600)
    linearity = models.CharField(verbose_name="Linearity", blank=True, null=True, max_length=600)
    drift = models.CharField(verbose_name="Drift", blank=True, null=True, max_length=600)
    eccentricity = models.CharField(verbose_name="Eccentricity", blank=True, null=True, max_length=600)
    reportZ = models.CharField(verbose_name="reportZ", blank=True, null=True, max_length=600)
    mass_value = models.CharField(verbose_name="Mass Value", blank=True, null=True, max_length=600)
    nominal_value = models.CharField(verbose_name="Nominal Value", blank=True, null=True, max_length=600)
    nomUnit = models.CharField(verbose_name="Nominal Value Unit", blank=True, null=True, max_length=600)
    after_conversion = models.CharField(verbose_name="Average After Conversion", blank=True, null=True, max_length=600)
    error = models.CharField(verbose_name="Error", blank=True, null=True, max_length=600)
    master_weight_item = models.ManyToManyField("certificates.WeightCertificate",verbose_name="Weight Certificate Item")
    least_count = models.CharField(null=True, blank=True, max_length=20)
    vt = models.CharField(verbose_name="Vt", blank=True, null=True, max_length=600)
    vr = models.CharField(verbose_name="Vr", blank=True, null=True, max_length=600)
    va = models.CharField(verbose_name="Va", blank=True, null=True, max_length=600)
    vo = models.CharField(verbose_name="Vo", blank=True, null=True, max_length=600)
    calculation_unit =  models.CharField(null=True, blank=True, max_length=20)
    duc_id = models.IntegerField(null=True, blank=True)

    @property
    def obsx(self):
        least_degits_count = str(self.least_count)
        least_rounding = least_degits_count[::-1].find('.')
        obs1 = float(self.obs1)
        return roundup(obs1, int(least_rounding))


    def massItemUncertainity(self):
        duc_id = self.duc_id
        lc_duc = self.mass_value
        x1 = self.obs1
        x2 = self.obs2
        x3 = self.obs3
        x4 = self.obs4
        x5 = self.obs5
        cal_point = self.nominal_value
        nomUnit = self.nomUnit
        obsUnit = self.obsUnit
        allinstru_list = self.mass_items.first().observation.instrument.all()
        least_count = self.least_count
        vt=self.vt
        vr=self.vr

        try:
            scope = self.mass_items.first().observation.scope

        except:
            scope = None

        allcertitem = []

        try:
            master_cert_Item = self.master_weight_item.all()
            for i in master_cert_Item:
                cer_id = i.id
                allcertitem.append(cer_id)

        except:
            allcertitem = allcertitem

        abc = WeightItemUncertainty(duc_id,cal_point,lc_duc, x1, x2, x3, x4, x5, nomUnit, obsUnit,allinstru_list, least_count,vt, vr, allcertitem, scope)
        return abc

    def mathcalN(self):

        obs_degits_count = str(self.obs21)
        obs_rounding = obs_degits_count[::-1].find('.')
        nom_unit = self.nomUnit

        totalDict = {}
        ba1 = float(self.obs21)-float(self.obs11)
        ba2 = float(self.obs22)-float(self.obs12)
        ba3 = float(self.obs23)-float(self.obs13)
        ba4 = float(self.obs24)-float(self.obs14)
        ba5 = float(self.obs25)-float(self.obs15)

        ba6 = float(self.obs31)-float(self.obs41)
        ba7 = float(self.obs32)-float(self.obs42)
        ba8 = float(self.obs33)-float(self.obs43)
        ba9 = float(self.obs34)-float(self.obs44)
        ba10 = float(self.obs35)-float(self.obs45)

        df1 = (ba1+ba6)/2
        df2 = (ba2+ba7)/2
        df3 = (ba3+ba8)/2
        df4 = (ba4+ba9)/2
        df5 = (ba5+ba10)/2

        mainAvg = (df1+df2+df3+df4+df5)/5

        totalDict['df1'] = roundup(df1, int(obs_rounding)+1)
        totalDict['df1'] = "{:.{}f}".format(totalDict['df1'], int(obs_rounding)+1)

        totalDict['df2'] = roundup(df2, int(obs_rounding)+1)
        totalDict['df2'] = "{:.{}f}".format(totalDict['df2'], int(obs_rounding) + 1)

        totalDict['df3'] = roundup(df3, int(obs_rounding)+1)
        totalDict['df3'] = "{:.{}f}".format(totalDict['df3'], int(obs_rounding) + 1)

        totalDict['df4'] = roundup(df4, int(obs_rounding)+1)
        totalDict['df4'] = "{:.{}f}".format(totalDict['df4'], int(obs_rounding) + 1)

        totalDict['df5'] = roundup(df5, int(obs_rounding)+1)
        totalDict['df5'] = "{:.{}f}".format(totalDict['df5'], int(obs_rounding) + 1)


        totalDict['mainAvg'] = roundup(mainAvg, int(obs_rounding)+1)


        nomValue = self.nominal_value
        nomUnit = self.nomUnit
        obsUnit = self.obsUnit
        vt = self.vt
        vr = self.vr
        va = self.va
        vo = self.vo

        num = float(va)-float(vo)
        dnom = (1/float(vt))-(1/float(vr))
        try:
            air_buoyancy = num / dnom
        except:
            air_buoyancy = 0


        master_used = self.mass_items.first().observation.instrument.first()

        cert = Certificate.objects.get(instrument_cert=master_used)
        certificate = cert.w_instru_cert_item.all()

        weightlist = {}

        consolidated_mass_values = 0
        for x in self.master_weight_item.all():
            consolidated_mass_values = consolidated_mass_values + float(x.mass_value)





        abc = weightlist
        cert_mass_value = consolidated_mass_values
        cert_mass_unit = self.master_weight_item.all().first().mass_value_unit
        newunit = weight_unit_conversion[cert_mass_unit][obsUnit]
        mass_valuleN = float(cert_mass_value) * newunit
        valunN = mass_valuleN*(1+air_buoyancy)
        MvalunN = valunN+mainAvg

        totalDict['MvalunN'] = roundup(MvalunN, int(obs_rounding))

        return totalDict



    def averageobs(self):
        av = (float(self.obs1) + float(self.obs2) + float(self.obs3) + float(self.obs4) + float(self.obs5))/5
        return av







    def __str__(self):
        return str(self.nominal_value)

class Weight(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="weight_obs", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    humidity = models.CharField(verbose_name="Humidity", blank=True, null=True, max_length=600)
    weight_item = models.ManyToManyField(MassItem, related_name="weight_item", blank=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="wetcalibratedby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)

    def __str__(self):
        return self.observation_number



class weightobservation(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="weight_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    humidity = models.CharField(verbose_name="Humidity", blank=True, null=True, max_length=600)
    mass_item = models.ManyToManyField(MassItem, related_name="mass_items", blank=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    lc_duc = models.CharField(verbose_name="lc_duc", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="weightcalibratedby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)



class RPMItem(models.Model):
    value_in = models.CharField(max_length = 200,choices = ranges, default = 'UUC')
    value = models.CharField(max_length = 200,choices = IndicatedValue,default = 'UUC')
    observation_1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    observation_2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    observation_3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    observation_4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    observation_5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)


    def average(self):
        itemNeed = (float(observation_1) + float(observation_2) + float(observation_3) + float(observation_4) + float(observation_5))
        return itemNeed/5


    def __str__(self):
        return self.value_in

class RPM(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="rpm_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    temp = models.CharField(verbose_name="Temprature", blank=True, null=True, max_length=600)
    rh = models.CharField(verbose_name="RH", blank=True, null=True, max_length=600)
    rpm_item = models.ManyToManyField(RPMItem, related_name="rpm_items", blank=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="rpmcalibratedby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)

    def __str__(self):
        return self.observation_number

class TimeEnergy(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="time_energy_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    temp = models.CharField(verbose_name="Temprature", blank=True, null=True, max_length=600)
    rh = models.CharField(verbose_name="RH", blank=True, null=True, max_length=600)
    TimeEnergy_item = models.ManyToManyField(RPMItem, related_name="TimeEnergy_items", blank=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="timecalibratedby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)

    def __str__(self):
        return self.observation_number


class thermalloggingDetails(models.Model):
      set_temp_value = models.CharField(verbose_name="Set Temprature Value", blank=True, null=True, max_length=255)
      logging_date = models.DateTimeField(verbose_name="Logging Date", blank=True, null=True, default=datetime.date.today)
      stating_time = models.CharField(verbose_name="N1", blank=True, null=True, max_length=600)
      end_time = models.CharField(verbose_name="N1", blank=True, null=True, max_length=600)
      uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
      remarks = models.TextField(max_length=600, null=True)
      calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="thercalibratedby",blank=True,null=True)
      is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)

      def __str__(self):
          return self.set_temp_value





class ThermalMPItem(models.Model):
    chamber_size_L1 = models.CharField(verbose_name="Size of chamber for inside L1", blank=True, null=True, max_length=600)
    chamber_size_L2 = models.CharField(verbose_name="Size of chamber for inside L2", blank=True, null=True, max_length=600)
    chamber_size_L3 = models.CharField(verbose_name="Size of chamber for inside L3", blank=True, null=True, max_length=600)
    location = models.CharField(max_length = 200,choices = Location,default = 'SensorCode')
    n1 = models.CharField(verbose_name="N1", blank=True, null=True, max_length=600)
    n2 = models.CharField(verbose_name="N2", blank=True, null=True, max_length=600)
    n3 = models.CharField(verbose_name="N3", blank=True, null=True, max_length=600)
    n4 = models.CharField(verbose_name="N4", blank=True, null=True, max_length=600)
    n5 = models.CharField(verbose_name="N5", blank=True, null=True, max_length=600)
    n6 = models.CharField(verbose_name="N6", blank=True, null=True, max_length=600)
    n7 = models.CharField(verbose_name="N7", blank=True, null=True, max_length=600)
    n8 = models.CharField(verbose_name="N8", blank=True, null=True, max_length=600)
    n9 = models.CharField(verbose_name="N9", blank=True, null=True, max_length=600)
    n10 = models.CharField(verbose_name="N10", blank=True, null=True, max_length=600)
    n11 = models.CharField(verbose_name="N11", blank=True, null=True, max_length=600)
    n12 = models.CharField(verbose_name="N12", blank=True, null=True, max_length=600)
    n13 = models.CharField(verbose_name="N13", blank=True, null=True, max_length=600)
    n14 = models.CharField(verbose_name="N14", blank=True, null=True, max_length=600)
    n15 = models.CharField(verbose_name="N15", blank=True, null=True, max_length=600)
    n16 = models.CharField(verbose_name="N16", blank=True, null=True, max_length=600)



    def __str__(self):
        return self.value_in


class ThermalMP(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="thermalMP_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    starting_temp = models.CharField(verbose_name="Starting Temprature", blank=True, null=True, max_length=600)
    ending_temp = models.CharField(verbose_name="Ending Temprature", blank=True, null=True, max_length=600)
    middle_temp = models.CharField(verbose_name="Middle Temprature", blank=True, null=True, max_length=600)

    starting_humidity = models.CharField(verbose_name="Starting Humidity", blank=True, null=True, max_length=600)
    ending_humidity = models.CharField(verbose_name="Ending Humidity", blank=True, null=True, max_length=600)
    middle_humidity = models.CharField(verbose_name="Middle Humidity", blank=True, null=True, max_length=600)

    # thermal_item = models.ManyToManyField(ThermalMPItem, related_name="thermalMP_items", blank=True)
    # logging_details = models.ManyToManyField(thermalloggingDetails, related_name="thermal_logging_items", blank=True)
    remarks = models.TextField(max_length=600, null=True)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="thermalmpcalibrationdby",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)
    data_log = models.FileField(max_length=800,upload_to="media/data_log/",null=True)
    data_log_record = models.FileField(max_length=800,upload_to="media/data_log_original/",null=True)

    def __str__(self):
        return self.observation_number


class ThermalItem(models.Model):
    indicated_value = models.CharField(max_length = 200,choices = Indicated,default = 'UUC')
    observation_1 = models.CharField(verbose_name="Observation Value 1", blank=True, null=True, max_length=600)
    observation_2 = models.CharField(verbose_name="Observation Value 2", blank=True, null=True, max_length=600)
    observation_3 = models.CharField(verbose_name="Observation Value 3", blank=True, null=True, max_length=600)
    observation_4 = models.CharField(verbose_name="Observation Value 4", blank=True, null=True, max_length=600)
    observation_5 = models.CharField(verbose_name="Observation Value 5", blank=True, null=True, max_length=600)
    sensor_length = models.CharField(verbose_name="Sensor Length", blank=True, null=True, max_length=600)
    sensor_diameter = models.CharField(verbose_name="Sensor Diameter", blank=True, null=True, max_length=600)
    immersion_depth = models.CharField(verbose_name="Immersion Depth", blank=True, null=True, max_length=600)

    def average():
        itemNeed = (float(observation_1) + float(observation_2) + float(observation_3) + float(observation_4) + float(observation_5))
        return itemNeed/5

    def __str__(self):
        return self.indicated_value

class Thermal(models.Model):
    observation = models.ForeignKey("observation.Observation", related_name="thermal_observation", on_delete=models.SET_NULL,blank=True,null=True)
    observation_number =  models.CharField(verbose_name="Observation Number", blank=True, null=True, max_length=255)
    temp = models.CharField(verbose_name="Temprature", blank=True, null=True, max_length=600)
    humidity = models.CharField(verbose_name="Humidity", blank=True, null=True, max_length=600)
    thermal_item = models.ManyToManyField(ThermalItem, related_name="thermal_items", blank=True)
    remarks = models.TextField(max_length=600, null=True)
    uncertain = models.CharField(verbose_name="Uncertain", blank=True, null=True, max_length=600)
    calibratedBy = models.ForeignKey("user.User", on_delete=models.SET_NULL,verbose_name="Calibrated By",related_name="calibration",blank=True,null=True)
    is_approved = models.BooleanField(default=False,verbose_name="Is Approved",blank=True)



    def __str__(self):
        return self.observation_number




class CoItem(models.Model):

    itemName = models.ForeignKey(UUCMaster, verbose_name="UUC Name", blank=True, null=True,on_delete=models.CASCADE)

    unit_price = models.CharField(verbose_name="Price", default=0, blank=True, null=True, max_length=255)
