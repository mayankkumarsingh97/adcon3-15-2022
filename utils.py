import pytz
from datetime import datetime
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import numpy as np
from uuc.models import *
from uncertanity.models import *
from certificates.models import *
import math
from django.db.models import Max
from django.db.models import Q
from django.db import models

from observation.models import *


import math

def roundup(originalvalue, intvalue):
    my_string= str(float(originalvalue))
    int_val= my_string.split('.')[0]
    decimal_val = my_string.split('.')[1]
    if len(decimal_val)>intvalue:
        if int(decimal_val[intvalue]) >= 5:
            valueC = decimal_val[:intvalue]
            adder = int(valueC)+1
            result = int_val+'.'+str(round(adder, intvalue))
            result = float(result)
        else:
            result = round(originalvalue, intvalue)
    else:
        result=float(originalvalue)
    return  result



class Kfactor(models.Model):
    veff = models.CharField(verbose_name="Veff", default=0, blank=True, null=True, max_length=255)
    k_factor = models.CharField(verbose_name="K Factor", default=0, blank=True, null=True, max_length=255)

    def __str__(self):
        return self.veff +' ' +'at' +' ' + self.k_factor

def variance(data, ddof=0):
     n = len(data)
     mean = sum(data) / n
     return sum((x - mean) ** 2 for x in data) / (n - ddof)

def stdev(data, ddof=0):
     return math.sqrt(variance(data, ddof))


def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)


def stdev(data, ddof=0):
    return math.sqrt(variance(data, ddof))

def getkfactor(value):
    kfact1= []
    kfactor_min = []
    kfactor_max = []
    min_dicts={}
    max_dicts = {}
    data_obj = Kfactor.objects.all()
    for u in data_obj:
        if float(u.veff) == float(value):
            kfact1.append(u.k_factor)
        else:
            if float(u.veff) < float(value):
                kfactor_min.append(u)
            else:
                kfactor_max.append(u)


    if kfactor_min:
        for i in kfactor_min:
            minlength = len(kfactor_min)
            for k in range(minlength):
                min_dicts[i] = float(i.veff)

    if kfactor_max:
        for i in kfactor_max:
            minlength = len(kfactor_max)
            for k in range(minlength):
                max_dicts[i] = float(i.veff)


    try:
        m1 = min(max_dicts, key=lambda x: max_dicts[x])
    except:
        pass

    if kfact1:
        k_factor = float(kfact1[0])
    else:
        k_factor = float(m1.k_factor)

    return k_factor






unit_conversion= {"µV":{"µV":1, "mV":0.001, "V":0.000001},
                  "mV":{"µV":1000, "mV":1, "V":0.001},
                  "V":{"µV":1000000, "mV":1000, "V":1},

                  "µA":{"µA":1, "mA":0.001, "A":0.000001},
                  "mA":{"µA":1000, "mA":1, "A":0.001},
                  "A":{"µA":1000000, "mA":1000, "A":1},

                  "Hz":{"Hz":1, "kHz":0.001},
                  "kHz":{"Hz":1000, "kHz":1},

                  "Ω" : {"Ω":1, "KΩ":0.001, "MΩ":0.000001},
                  "KΩ": {"Ω":1000, "KΩ":1, "MΩ":0.001},
                  "MΩ": {"Ω":1000000, "KΩ":1000, "MΩ":1},

                  "pF" : {"pF":1, "nF":0.001, "µF":0.000001, "mF":0.001},
                  "nF": {"pF":1000, "nF":1, "µF":0.001, "mF":0.000001},
                  "µF": {"pF":1000000, "nF":1000, "µF":1, "mF":0.001},
                  "mF": {"pF":1000000000, "nF":1000000, "µF":1000, "mF":1},

                  "Hz":{"Hz":1, "kHz":0.001, "MHz":0.000001, "GHz":0.000000001},
                  "kHz":{"Hz":1000, "kHz":1, "MHz":0.001, "GHz":0.000001},
                  "MHz":{"Hz":1000000, "kHz":0.001, "MHz":1, "GHz":0.001},
                  "GHz":{"Hz":1000000000, "kHz":1000000, "MHz":1000, "GHz":1}

                  }

def etItemUncertainty(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1, obs2,
                      obs3, obs4, obs5, instru_range, instru_range_unit, allinstru_list, instrument_accessories,stableity_of_the_source, scope):


    #print(f'\n \n Dictionary values of util for cal_point- {cal_point} cal_point_unit- {cal_point_unit} obs1- {obs1} obs2- {obs2} obs3- {obs3} obs4- {obs4}  obs5- {obs5}  instru_range- {instru_range} instru_range_unit- {instru_range_unit}  instru_range_unit- {instru_range_unit} allinstru_list- {allinstru_list} instrument_accessories- {instrument_accessories} {stableity_of_the_source}')


    accessories_uncertainity_accuracy=[]
    accual_cal_value = cal_point

    scope_lower_capability = scope.lower_capability
    scope_units = scope.units

    scope_degits_count = str(scope_lower_capability)
    scope_rounding = scope_degits_count[::-1].find('.')

    if instrument_accessories:

        attached_accessories = AccessoriesMaster.objects.get(id=int(instrument_accessories))
        cal_point = float(cal_point)

        if attached_accessories.acc_type == "coil":
            no_of_turns = attached_accessories.no_of_turns
            cal_point = float(cal_point)
            accuracy_of_the_coil = cal_point * 0.0025
            accessories_uncertainity_accuracy.append(accuracy_of_the_coil)

    else:
        pass




    myinstru =[]

    try:
        for i in allinstru_list:
            ids = i['instrument']
            abc = instrumentMaster.objects.get(id=ids)

            myinstru.append(abc)

    except:

        for j in allinstru_list:
            myinstru.append(j)



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
    # obs1 = roundup(obs1)
    listobserve = [obs1, obs2, obs3, obs4, obs5]
    ua = stdev(listobserve, ddof=1)
    uba = ua
    ua = ua / math.sqrt(5)
    ua = roundup(ua, 18)

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

    totalDict = {}

    totalDict['ua'] = ua



    for items in duc_unc.master_uncertainty.first().uc.all():

        if items.parameters == 'accuracy':
            unc_need = 0
            abc = items.instrument.et_accessory_detail.all()
            for itemd in abc:

                if itemd.type == cal_point and itemd.info == cal_point_unit and itemd.category == lc_duc_unit_parameter:
                    abd = itemd.accuracy
                    ub4 = float(abd)
                    if items.distribution == 'Normal':
                        myV = 2
                    elif items.distribution == 'Rectangular':
                        myV = math.sqrt(3)
                    ub4 = ub4 / myV
                    totalDict['ub4'] = ub4


    for items in duc_unc.master_uncertainty.first().ub.all():

        if items.parameters == 'uncertainty':

            instruQ = []

            for j in myinstru:
                for k in items.instrument.i_blueprint.all():
                    if j == k:
                        instruQ.append(j)


            master_used = instruQ[0]

            isInstrument = False

            if items.instrument:
                isInstrument = True
            else:
                isInstrument = False

            quertstd1 = []
            masteruncertitem = []

            if isInstrument:
                v1 = master_used.instrument_certificate.first()
                v2 = v1.instru_cert_item.all()


                quertstd = []


                for i in v2:
                    if i.parameter ==lc_duc_unit_parameter:
                        unit_multiplier = unit_conversion[instru_range_unit][i.range_unit]
                        newinstru_range = float(instru_range)*unit_multiplier

                        if float(i.range) >= float(newinstru_range):
                            if quertstd:
                                updated_val = float(quertstd[0].range)
                                if updated_val >= float(i.range):
                                    # quertstd.clear()
                                    quertstd.append(i)

                                else:
                                    pass
                            else:
                                quertstd.append(i)


            else:
                pass




            correction_factor_list = []

            correction_min_list = []
            correction_max_list = []

            min_dicts = {}
            max_dicts = {}
            error_passed_list = []
            master_uncertainityQ = []

            if instrument_accessories:


                attached_accessories = AccessoriesMaster.objects.get(id=int(instrument_accessories))
                cal_point = float(cal_point)

                if attached_accessories.acc_type == "coil":
                    no_of_turns = attached_accessories.no_of_turns
                    cal_point = float(cal_point)/float(no_of_turns)


            for u in v2:
                if u.parameter == lc_duc_unit_parameter:
                    unit_multiplier1 = unit_conversion[u.value_std_unit][cal_point_unit]
                    new_std = float(u.value_std)*unit_multiplier1
                    x1 = u.value_std
                    x1_unit_conv = unit_conversion[u.value_std_unit][cal_point_unit]
                    x2 = u.value_uuc
                    x2_unit_conv = unit_conversion[u.value_uuc_unit][cal_point_unit]
                    if new_std == float(cal_point):
                        x1N = float(x1) * x1_unit_conv
                        x2N = float(x2) * x2_unit_conv
                        error_passed = x1N-x2N
                        error_passed_list.append(error_passed)
                        master_uncertainityQ.append(u)
                    else:
                        if new_std< float(cal_point):
                            correction_min_list.append(u)
                        else:
                            correction_max_list.append(u)



            if correction_min_list:
                for i in correction_min_list:
                    unit_multiplier = unit_conversion[i.value_std_unit][cal_point_unit]
                    minlength = len(correction_min_list)
                    for k in range(minlength):
                        min_dicts[i] = float(i.value_std) * unit_multiplier


            if correction_max_list:
                for i in correction_max_list:
                    unit_multiplier = unit_conversion[i.value_std_unit][cal_point_unit]
                    minlength = len(correction_max_list)
                    for k in range(minlength):
                        max_dicts[i] = float(i.value_std) * unit_multiplier





            try:

                max_cert_item = min(max_dicts, key=lambda x: max_dicts[x])
                masteruncertitem_minQ = min(max_dicts, key=lambda x: max_dicts[x])
                min_cert_item = max(min_dicts, key=lambda x: min_dicts[x])

                x1_value_std = float(max_cert_item.value_std)
                x1_std_unit_conv = unit_conversion[max_cert_item.value_std_unit][cal_point_unit]
                x1_value_stdN = x1_value_std * x1_std_unit_conv

                x1_value_uuc = float(max_cert_item.value_uuc)
                x1_uuc_unit_conv = unit_conversion[max_cert_item.value_uuc_unit][cal_point_unit]
                x1_value_uucN = x1_value_uuc * x1_uuc_unit_conv

                x2_value_std = float(min_cert_item.value_std)
                x2_std_unit_conv = unit_conversion[min_cert_item.value_std_unit][cal_point_unit]
                x2_value_stdN = x2_value_std * x2_std_unit_conv

                x2_value_uuc = float(min_cert_item.value_uuc)
                x2_uuc_unit_conv = unit_conversion[min_cert_item.value_uuc_unit][cal_point_unit]
                x2_value_uucN = x2_value_uuc * x2_uuc_unit_conv




                e1 = x1_value_uucN - x1_value_stdN
                e2 = x2_value_uucN - x2_value_stdN

                num = e1-e2
                denom = x1_value_stdN - x2_value_stdN
                x_value =num/denom
                ityN = float(max_cert_item.value_std) * x1_std_unit_conv

                errorx = (float(cal_point) - float(ityN)) * x_value + float(e1)


            except:
                error = error_passed_list[0]

            if error_passed_list:
                error = error_passed_list[0]
            else:
                error= errorx

            if master_uncertainityQ:
                master_uncert = master_uncertainityQ[0]
            else:
                master_uncert = masteruncertitem_minQ

            error = error * -1


            std_after_correction = float(cal_point)+error





            master_uncert_percent = master_uncert.uncertain
            std_value = master_uncert.value_std
            std_value_unit = master_uncert.value_std_unit
            converted_std_value_unit = unit_conversion[std_value_unit][cal_point_unit]
            converted_std_value = float(std_value)*converted_std_value_unit
            valN = float(master_uncert_percent)*converted_std_value
            master_uncertainity = valN/100

            master_uncertainity = roundup(master_uncertainity, 15)

            combined_uncertainity = float(master_uncertainity)



            ub1 = float(combined_uncertainity) / 2



            totalDict[items.name] = ub1



        elif items.parameters == 'lc':
            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)

            lc = float(lc_duc) / 2
            ub2 = lc / myV
            # ub2 = format(ub2,'.6f')

            totalDict[items.name] = ub2



        elif items.parameters == 'accuracy':

            for j in myinstru:
                for k in items.instrument.i_blueprint.all():
                    if j == k:
                        instruQ.append(j)


            master_used = instruQ[0]
            std_equipment = etAccessorySpecification.objects.filter(parameters=lc_duc_unit_parameter , instrument=master_used)
            quertstd = []

            for specN in std_equipment:

                unit_conv = unit_conversion[specN.range_unit][cal_point_unit]
                new_range_from = float(specN.from_range) * unit_conv
                new_range_to = float(specN.to_range) * unit_conv


                if float(cal_point) >= new_range_from and float(cal_point) <= new_range_to:
                    if quertstd:
                        u_conv = unit_conversion[quertstd[0].range_unit][cal_point_unit]
                        updated_val = float(quertstd[0].to_range) * u_conv
                        if updated_val >= new_range_to:
                            quertstd.clear()
                            quertstd.append(specN)
                        else:
                            pass
                    else:
                        quertstd.append(specN)

            valueNN = float(cal_point)
            accuracyQ = quertstd[0]



            accuracyN = quertstd[0].retunvalue(valueNN, cal_point_unit, instru_range, instru_range_unit)

            accuracyN = roundup(accuracyN, 12)
            accuracydict = accuracyN


            if accessories_uncertainity_accuracy:
                coil_accuracy_list = accessories_uncertainity_accuracy[0]
                totalDict['coil_accuracy']=coil_accuracy_list
            else:
                coil_accuracy_list = 0




            if lc_duc_unit_parameter == "DC Current":

                ub3 = float(accuracyN)+float(coil_accuracy_list)
                if items.distribution == 'Normal':
                    myV = 2
                    ub3 = ub3 / myV

                    totalDict[items.name] = ub3

                elif items.distribution == 'Rectangular':
                    myV = math.sqrt(3)
                    ub3 = ub3 / myV

                    totalDict[items.name] = ub3


            if lc_duc_unit_parameter == "AC-Current":

                ub3 = float(accuracyN)+float(coil_accuracy_list)
                if items.distribution == 'Normal':
                    myV = 2
                    ub3 = ub3 / myV

                    totalDict[items.name] = ub3

                elif items.distribution == 'Rectangular':
                    myV = math.sqrt(3)
                    ub3 = ub3 / myV

                    totalDict[items.name] = ub3
            else:
                if items.distribution == 'Normal':
                    myV = 2
                    ub3 = ub3 / myV
                    ub3 = roundup(ub3, 10)

                    totalDict[items.name] = ub3

                elif items.distribution == 'Rectangular':
                    myV = math.sqrt(3)
                    accN = float(accuracyN) / myV
                    ub3 = accN
                    ub3 = roundup(ub3, 10)
                    totalDict[items.name] = ub3


        elif items.parameters == 'stableity_of_the_source':

            try:
                stableity_of_the_source = float(stableity_of_the_source)
            except:
                stableity_of_the_source = 0

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)

            stableity_of_the_source = stableity_of_the_source
            ub4 = stableity_of_the_source / myV
            totalDict[items.name] = ub4



    sumINeed = pow(ua, 2) + pow(ub1, 2) + pow(ub2, 2) + pow(ub3, 2) + pow(ub4, 2)


    uc = math.sqrt(sumINeed)

    totalDict['uc'] = roundup(uc, 6)


    veff = pow(uc, 4)
    if ua != 0:
        veff = veff * 4 / pow(ua, 4)
        try:
            K = getkfactor(veff)
        except:
            K=2
    else:
        veff = 'Infinity'
        K=2



    try:
        totalDict['veff'] = roundup(veff, 6)
    except:
        totalDict['veff'] = 'Infinity'
    totalDict['ua'] = roundup(ua, 6)
    totalDict['std'] = roundup(uba, 6)

    totalDict['ub1'] = roundup(ub1, 6)
    totalDict['ub2'] = roundup(ub2, 6)
    totalDict['ub3'] = roundup(ub3, 6)
    totalDict['ub4'] = roundup(ub4, 6)


    UmV = uc * K

    nominal_val = str(accual_cal_value)
    nom_rounding = nominal_val[::-1].find('.')

    totalDict['U'] = roundup(UmV, int(scope_rounding))

    Up = UmV * 100 / float(accual_cal_value)
    Ue = uc * 2

    totalDict['Ue'] = roundup(Ue, int(scope_rounding))

    least_count_count_ = str(lc_duc)
    rounding = accual_cal_value[::-1].find('.')
    error1 = roundup(error, int(rounding))
    totalDict['error'] = error1

    scope_lower_capability = scope.lower_capability

   #apply nabl scope for % only, if need then extended

    if scope_units == '%':
        if Up<= float(scope_lower_capability):
            Up = float(scope_lower_capability)
        else:
            Up=Up
    else:
        Up=Up

    totalDict['Up'] = roundup(Up, int(scope_rounding))
    totalDict['accuracydict'] = accuracydict
    totalDict['accuracyQ'] = accuracyQ.id

    totalDict['master_uncertainQ'] = masteruncertitem_minQ.id


    totalDict['master_uncertainity'] = master_uncertainity
    totalDict['nonrounded_error'] = error
    totalDict['std_after_correction'] = roundup(std_after_correction, int(nom_rounding))
    totalDict['accual_cal_value'] = instru_range + ' ' +instru_range_unit
    totalDict['least_count']=lc_duc


    #print(f'\n \n Dictionary values of util for {cal_point} {cal_point_unit} is :- {totalDict}')
    return totalDict
dimensions_unit_conversion = {
    "mm": {"mm":1,"µm":1000},
    "µm": {"mm":0.001,"µm":1}
}

def dimItemUncertainty(duc_id,lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1, obs2, obs3, obs4, obs5, rangeP,tempP,least_count, temp, nomUnit, obsUnit):
    duc = UUCMaster.objects.get(id=duc_id)

    multiplyer = dimensions_unit_conversion[nomUnit][obsUnit]
    #print(multiplyer, ">>>>>")

    temp2 = temp

    if lc_duc:
        pass
    else:
        lc_duc=''
    obs1 = float(obs1) * multiplyer
    obs2 = float(obs2) * multiplyer
    obs3 = float(obs3) * multiplyer
    obs4 = float(obs4) * multiplyer
    obs5 = float(obs5) * multiplyer

    obsSum = obs1+obs2+obs3+obs4+obs5/5
    cal_point = float(cal_point)

    std_uuc_dff = abs(obsSum-cal_point)

    #print(std_uuc_dff, "////////////////////......")

    listobserve=[obs1, obs2, obs3, obs4, obs5]
    uaa = stdev(listobserve, ddof=1)
    std = uaa
    uaaa=uaa/math.sqrt(5)


    ub1 = 0
    # temp1 = float(temp1)
    ub2=0
    ub3=0
    uc = 0
    veff = 0
    UmV = 0
    Up = 0
    ub4=0
    duc_unc = UUCMaster.objects.get(id=duc_id)

    unc_need = 0

    totalDict = {}

    for items in duc_unc.master_uncertainty.first().uc.all():

        if items.parameters=='uncertainty':

            a1 = float(items.uuc.coefficient_of_temp.linear_coeff)
            a2 = float(items.instrument_master.coefficient_i.linear_coeff)
            a3 = abs(a1+a2)
            divh = a3/2
            rangeP = items.uuc.size
            if items.distribution=='Normal':
                uncert_temp = float(items.instrument.uncertainty_access)

                ub4 = float(rangeP)*divh*uncert_temp
                ub4 = ub4/2000

            elif items.distribution=='Rectangular':
                uncert_temp = float(items.instrument.uncertainty_access)
                myV= math.sqrt(3)

                numt = rangeP*divh
                new_val = numt*uncert_temp
                ub4 = new_val/2000

            uncert_temp = uncert_temp

            totalDict[items.name] = ub4

        elif items.parameters=='accuracy':

            a1 = float(items.uuc.coefficient_of_temp.linear_coeff)
            a2 = float(items.instrument_master.coefficient_i.linear_coeff)
            a3 = abs(a1+a2)

            divh = a3/2
            # a4 = a2+a1
            rangeP = float(items.uuc.size)


            myVal = divh*rangeP


            if items.distribution=='Normal':
                uncert_temp = float(items.instrument.uncertainty_access)

                ub8 = float(rangeP)*divh*uncert_temp
                ub8 = ub4/2000

            elif items.distribution=='Rectangular':

                accuracy_temp = float(items.instrument.accuracy)
                newVal= myVal*accuracy_temp
                myV= math.sqrt(3)
                ub8 = newVal/myV/1000
                ub8 = ub8/1000

                accuracy_temp_recoreder = accuracy_temp


            totalDict[items.name] = ub8

    for items in duc_unc.master_uncertainty.first().ub.all():
        if items.parameters=='uncertainty':

            dimMasterCerti = dialGuageTester.objects.all()


            uncertainty = items.instrument.uncertainty
            itemd_unit = items.instrument.uncertainty_unit
            uncert_multi = dimensions_unit_conversion[itemd_unit][obsUnit]
            itemd = float(uncertainty) * uncert_multi

            ub1 = itemd/2
            totalDict[items.name] = ub1

        elif items.parameters=='lc':
            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)
            if items.uuc is not None:
                lc = float(least_count)/2
            else:
                lc = float(items.instrument.lc_resolution)
            ub2=lc/myV

            totalDict[items.name] = ub2



        elif items.parameters=='change_in_room_temp':

            a1 = float(items.uuc.coefficient_of_temp.linear_coeff)
            a2 = float(items.instrument.coefficient_i.linear_coeff)
            a3 = abs(a2-a1)
            a4 = a2+a1
            abd = items.uuc.size

            ub3 = float(abd)
            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)
            ub3 = ub3/myV
            ub3 = float(abd)*a3/myV
            totalDict[items.name] = ub3

        elif items.parameters=='difference_in_temp':
            a1 = float(items.uuc.coefficient_of_temp.linear_coeff)
            a2 = float(items.instrument.coefficient_i.linear_coeff)

            a3 = abs(a1+a2)
            divh = a3/2
            rangeP = float(items.uuc.size)
            val= divh*rangeP

            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)

            temp=1
            new_val =val*temp/myV
            ub5 = new_val/1000
            totalDict[items.name] = ub5

        elif items.parameters=='change_in_linear_thermal_coefficient':

            a1 = float(items.uuc.coefficient_of_temp.linear_coeff)
            a2 = float(items.instrument.coefficient_i.linear_coeff)
            a3 = abs(a2+a1)
            devh =a3/2
            temp=1


            rangeP = float(items.uuc.size)
            valh = divh*rangeP*0.1*temp

            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)

                newVal = valh/1000
                ub6 = newVal/myV
                totalDict[items.name] = ub6


        elif items.parameters=='accuracy':

            accuracy_master = items.instrument.accuracy

            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)
                newVal = float(accuracy_master)
                ub7 = newVal/myV
                totalDict[items.name] = ub7



    testDict = totalDict

    myList = totalDict.keys()
    for item in myList:
        if 'ub' not in item:
            testDict.pop(item)

    sumINeed=0

    ua_to_add = pow(float(uaaa), 2)

    for item,value in testDict.items():
        sumINeed += pow(float(value), 2)


    uc = math.sqrt(sumINeed + ua_to_add)
    veff = pow(uc,4)
    if uaaa!=0:
        veff = veff*4/pow(uaaa,4)
    else:
        veff='NA'
    UmV = uc*2
    Up = UmV*100/float(cal_point)

    totalDict['U']=UmV
    totalDict['Up']=Up
    totalDict['ua'] = uaaa
    totalDict['uc']=uc
    totalDict['veff']=veff
    totalDict['std'] = std
    totalDict['uncertainty'] = uncertainty
    totalDict['std_uuc_dff'] = std_uuc_dff
    totalDict['accuracy_master'] = accuracy_master
    totalDict['uncert_temp'] = uncert_temp


    totalDict['avg_after_conver'] = obsSum
    totalDict['accuracy_temp_recoreder'] = accuracy_temp_recoreder



    return totalDict

weighing_unit_conversion = {
    "g": {"mg":1, "g":1000, "kg":1000},
    "mg": {"mg":1, "g":1000, "kg":1000},
    "kg": {"mg":0.001, "g":1, "kg":1000}
}


def WeighingItemUncertainty(duc_id,lc_duc, cal_point, obs1, obs2, obs3, obs4, obs5, nomUnit, obsUnit, temp, eccentricity_max_min, HR1, HR2, HR3, HR4, HR5, HR6, HR7, HR8, HR9, HR10, FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9,FR10):
    duc = UUCMaster.objects.get(id=duc_id)

    multiplyer = weighing_unit_conversion[nomUnit][obsUnit]
    eccentricity_max_min=float(eccentricity_max_min)
    temp2 = temp

    if lc_duc:
        pass
    else:
        lc_duc=''

    obs1 = float(obs1) * multiplyer
    obs2 = float(obs2) * multiplyer
    obs3 = float(obs3) * multiplyer
    obs4 = float(obs4) * multiplyer
    obs5 = float(obs5) * multiplyer

    listobserve=[obs1, obs2, obs3, obs4, obs5]
    uaa = stdev(listobserve, ddof=1)


    if HR6 != '':
        listHR = [float(HR1), float(HR2), float(HR3), float(HR4), float(HR5), float(HR6), float(HR7), float(HR8), float(HR9), float(HR10)]
        listFR = [float(FR1), float(FR2), float(FR3), float(FR4), float(FR5), float(FR6), float(FR7), float(FR8), float(FR9), float(FR10)]

    else:
        listHR = [float(HR1), float(HR2), float(HR3), float(HR4), float(HR5)]
        listFR = [float(FR1), float(FR2), float(FR3), float(FR4), float(FR5)]

    stdHR = stdev(listHR, ddof=1)
    stdFR = stdev(listFR, ddof=1)

    std_list = [uaa, stdHR, stdFR]
    maximum_std_dev = max(std_list)



    ua=uaa/math.sqrt(9)

    ub1 = 0
    # temp1 = float(temp1)
    ub2=0
    ub3=0
    uc = 0
    veff = 0
    UmV = 0
    Up = 0
    ub4=0

    duc_unc = UUCMaster.objects.get(id=duc_id)

    totalDict = {}

    for items in duc_unc.master_uncertainty.first().ub.all():



        if items.parameters=='uncertainty':
            uuc_need=0


            if items.instrument:
                isInstrument = True
            else:
                isInstrument = False

            quertstd = []

            if isInstrument:
                v1 = items.instrument.instrument_certificate.first()
                v2 = v1.wb_instru_cert_item.all()


                for i in v2:
                    mass_value = float(i.mass_value)
                    mass_value_unit = i.mass_value_unit
                    multi = weighing_unit_conversion[mass_value_unit]['g']
                    mass_value_after = mass_value * multi
                    nominal_val = float(cal_point)
                    nominal_val_unit = nomUnit
                    nom_multi = weighing_unit_conversion[nominal_val_unit]['g']
                    nominal_val_after = nominal_val*nom_multi

                    if mass_value_after >= nominal_val_after:


                        if quertstd:

                            if float(quertstd[0].mass_value) >= float(i.mass_value):
                                quertstd.clear()
                                quertstd.append(i)
                            else:
                                pass

                        else:
                            quertstd.append(i)



            if items.distribution == 'Normal':
                uncertainty = quertstd[0].uncertainity
                #print(uncertainty, "uncertainty uncertainty")
                uncertainty_unit = quertstd[0].uncertainity_unit

                uncert_multi = weighing_unit_conversion[uncertainty_unit][obsUnit]
                itemd = float(uncertainty) * uncert_multi
                myV = 2
                ub1 = float(itemd)/myV
                totalDict[items.name] = ub1


        elif items.parameters=='lc':

            if items.distribution=='Normal':
                myV = 2

            elif items.distribution=='Rectangular':
                itemd = items.uuc.size
                nVal = float(itemd)/2
                myV= math.sqrt(3)
                ub2 = nVal/myV
            totalDict[items.name] = ub2



        elif items.parameters=='drift_of_the_master':

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                itemd = items.instrument.drift_of_the_master
                nVal = float(itemd)*0.1
                myV = math.sqrt(3)
                ub3 =nVal / myV
            totalDict[items.name] = ub3


        elif items.parameters=='ecentricity':
            a1 = eccentricity_max_min

            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)
            my = myV*2
            ub4 = a1/myV

            totalDict[items.name] = ub4

        elif items.parameters=='linerity':
            a1 = float(items.uuc.linerity)

            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)
                ub5 = a1/myV

            totalDict[items.name] = ub5



    testDict = totalDict

    myList = totalDict.keys()

    for item in myList:
        if 'ub' not in item:
            testDict.pop(item)
    sumINeed=0

    for item,value in testDict.items():
        sumINeed += pow(float(value), 2)

    uc = math.sqrt(sumINeed)
    veff = pow(uc,4)
    if ua!=0:
        veff = veff*4/pow(ua,4)
    else:
        veff='NA'
    UmV = uc*2
    Up = UmV*100/float(cal_point)
    totalDict['U']=UmV
    totalDict['Up']=Up
    totalDict['uc']=uc
    totalDict['veff']=veff


    return totalDict


weight_unit_conversion = {
    "g": {"mg":1000, "g":1, "kg":0.001},
    "mg": {"mg":1, "g":1000, "kg":1000000},
    "kg": {"mg":0.000001, "g":0.001, "kg":1}
}

def WeightItemUncertainty(duc_id,cal_point,lc_duc, x1, x2, x3, x4, x5, nomUnit, obsUnit,allinstru_list, least_count,vt, vr, allcertitem, scope):
    weight_cert_item = []

    scope_lower_capability = scope.lower_capability
    scope_units = scope.units
    scope_result = scope.result_type

    scope_degits_count = str(scope_lower_capability)
    scope_rounding = scope_degits_count[::-1].find('.')

    least_degits_count = str(least_count)
    least_rounding = least_degits_count[::-1].find('.')


    try:
        for mx in allcertitem:
            c = mx['certitem']
            weight_cert_item.append(c)
    except:
        weight_cert_item = allcertitem

    myinstru = []

    try:
        for i in allinstru_list:
            ids = i['instrument']
            abc = instrumentMaster.objects.get(id=ids)
            myinstru.append(abc)
    except:
        for j in allinstru_list:
            myinstru.append(j)


    duc = UUCMaster.objects.get(id=duc_id)
    cal_point = float(cal_point)

    multiplyer = weight_unit_conversion[nomUnit][obsUnit]



    cal_point = float(cal_point)

    if lc_duc:
        pass
    else:
        lc_duc=''

    x1 = roundup(float(x1), int(least_rounding))
    x2 = roundup(float(x2), int(least_rounding))
    x3 = roundup(float(x3), int(least_rounding))
    x4 = roundup(float(x4), int(least_rounding))
    x5 = roundup(float(x5), int(least_rounding))
    cal_point = float(cal_point)*multiplyer

    listobserve=[x1, x2, x3, x4, x5]
    obs_sum = x1 + x2 + x3 + x4 + x5
    new_avg = obs_sum / 5
    erro_std_uuc = float(cal_point) - new_avg

    ua = stdev(listobserve, ddof=1)

    standard_dev = ua
    ua=ua/math.sqrt(5)

    ub1 = 0
    # temp1 = float(temp1)
    ub2=0
    ub3=0
    uc = 0
    veff = 0
    UmV = 0
    Up = 0
    ub4=0
    duc_unc = UUCMaster.objects.get(id=duc_id)

    unc_need = 0

    totalDict = {}

    quertstd = []


    for items in duc_unc.master_uncertainty.first().ub.all():


        if items.parameters=='uncertainty':

            if items.instrument:
                isInstrument = True
            else:
                isInstrument = False

            instruQ = []
            for j in myinstru:

                for k in items.instrument.i_blueprint.all():
                    #print(j)
                    if j == k:
                        instruQ.append(j)

            master_used = instruQ[0]



            #quertstd = []
            uncertain_all = []


            v1 = master_used.instrument_certificate.first()

            for i in weight_cert_item:
                vm = v1.w_instru_cert_item.all()

                for j in vm:
                    if j.id == int(i):
                        unit_conversion = weight_unit_conversion[j.uncertainity_unit][obsUnit]
                        uncertainity = float(j.uncertainity)
                        uncertainityN = uncertainity*unit_conversion
                        uncertain_all.append(uncertainityN)

            consolidated_uncertainity = 0
            for x in uncertain_all:
                consolidated_uncertainity = consolidated_uncertainity+float(x)

            master_uncertainity = consolidated_uncertainity

            #print(weight_cert_item, v1, "jjjjjjjjjjjjjjjjj ttttttttttttttttttttt")

            if items.distribution == 'Normal':
                myV = 2
                ub1 = float(master_uncertainity)
                ub1 = ub1 / myV
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)
                ub1 = float(master_uncertainity) / myV

            totalDict[items.name] = ub1




        elif items.parameters=='drift_of_the_master':
            instruQ = []
            for j in myinstru:
                for k in items.instrument.i_blueprint.all():
                    if j == k:
                        instruQ.append(j)

            master_used = instruQ[0]

            drift_all = []

            v1 = master_used.instrument_certificate.first()

            for i in weight_cert_item:
                vm = v1.w_instru_cert_item.all()

                for j in vm:
                    if j.id == int(i):
                        unit_conversion = weight_unit_conversion[j.drift_unit][obsUnit]
                        drift_of_the_master = float(j.drift)
                        drift_of_the_masterN = drift_of_the_master * unit_conversion
                        drift_all.append(drift_of_the_masterN)

            consolidated_drift = 0
            for x in drift_all:
                consolidated_drift = consolidated_drift + float(x)

            drift_of_the_master = consolidated_drift
            if items.distribution=='Normal':
                myVN = 2
            elif items.distribution=='Rectangular':
                myVN= math.sqrt(3)

            ub2 = abs(float(drift_of_the_master)/myVN)
            #print(drift_all, ub2, "8888888888888 555555555555555555 333333333333333v222222222 444444444")
            totalDict[items.name] = ub2

        elif items.parameters=='lc':
            least_count = float(least_count)

            if items.distribution=='Normal':
                myC = 2
            elif items.distribution=='Rectangular':
                myC= math.sqrt(6)

            ub3 = float(least_count)/myC
            totalDict[items.name] = ub3


        elif items.parameters=='buogancy_correction':

            instruQ = []
            for j in myinstru:
                #print('=============================================== ')
                for k in items.instrument.i_blueprint.all():
                    if j == k:
                        instruQ.append(j)

            master_used = instruQ[0]

            massvalues_all = []

            v1 = master_used.instrument_certificate.first()

            for i in weight_cert_item:
                vm = v1.w_instru_cert_item.all()

                for j in vm:
                    if j.id == int(i):
                        unit_conversion = weight_unit_conversion[j.mass_value_unit][obsUnit]
                        mass_values = float(j.mass_value)
                        mass_valuesN = mass_values * unit_conversion
                        massvalues_all.append(mass_valuesN)

            consolidated_mass_values = 0
            for x in massvalues_all:
                consolidated_mass_values = consolidated_mass_values + float(x)

            consolidated_mass_values = consolidated_mass_values

            itemvt = float(vt)
            itemvr = float(vr)
            f1 = 0.12/math.sqrt(3)
            f2 = itemvr - itemvt
            f3 = itemvt *itemvr
            f12 = f1*f2
            f12NN = f12*consolidated_mass_values
            valN_n = f12NN/f3
            ub4 = valN_n

            totalDict[items.name] = ub4

    testDict = totalDict

    myList = totalDict.keys()
    for item in myList:
        if 'ub' not in item:
            testDict.pop(item)


    ua_sqN = pow(ua, 2)
    sumINeed=0
    for item,value in testDict.items():
        sumINeed += pow(float(value), 2)


    uc = math.sqrt(sumINeed+ua_sqN)


    veff = pow(uc,4)

    if ua!=0:
        veff = veff*4/pow(ua,4)
        try:
            K = getkfactor(veff)
        except:
            K=2
    else:
        veff='infinity'
        K = 2

    UmV = uc * K

    # apply nabl scope for % only, if need then extended

    #print(scope_units, obsUnit, "pppppppppppppppppppppppppppppppppppppppppppp gggggggggggggggggggggggg eeeeeeeeeeee")

    if scope_result == 'unit':
        unit_conversion = weight_unit_conversion[scope_units][obsUnit]
        xn = float(scope_lower_capability) * unit_conversion
        if UmV <= xn:
            UmV = xn
        else:
            UmV = UmV
    else:
        if Up <= float(scope_lower_capability):
            Up = float(scope_lower_capability)
        else:
            Up = Up



    Up = UmV*100/0.001

    totalDict['U']=UmV
    totalDict['Up']=Up
    totalDict['uc']=uc
    totalDict['veff']=veff
    totalDict['erro_std_uuc'] = erro_std_uuc
    totalDict['ua'] = ua
    totalDict['buogancy'] = valN_n
    master_uncertainity = master_uncertainity
    totalDict['drift_of_the_master'] = drift_of_the_master

    totalDict['master_uncertainity'] = master_uncertainity
    totalDict['standard_dev'] = standard_dev



    return totalDict

#
# pressure_unit_conversion = {"Pascal":{"Pascal":1, "bar":0.00001, "psi":0.0001450377},
#                             "bar" :{"Pascal":100000, "bar":1, "psi":14.503773773},
#                             "psi" :{"Pascal":6894.7572932, "bar":0.0689475729, "psi":1}
#                             }


pressure_unit_conversion =  {"Pascal":{"Pascal":1, "bar":0.00001, "psi":0.000145038,  "kg/cm2": 0.0000101972, "mmH2o": 0.10, "mmHg": 0.00750062, "inHg":0.0002953, "mbar": 0.01, "mpa": 0.000001, "kpa": 0.001, "inH2o": 0.00401865, "cmH2o": 0.0101972, "hpa": 0.01 },
                            "bar" :{"Pascal":100000, "bar":1, "psi":14.503773773, "kg/cm2": 1.01972, "mmH2o": 10197.16, "mmHg": 750.062, "inHg":29.53,"mbar": 1000, "mpa": 0.1, "kpa": 100, "inH2o": 401.865, "cmH2o": 1019.72, "hpa": 1000 },
                            "psi" :{"Pascal": 6894.76, "bar":0.0689476, "psi":1, "kg/cm2": 0.070307, "mmH2o": 703.07, "mmHg": 51.7149, "inHg":2.03602, "mbar": 68.9476, "mpa": 0.00689476, "kpa": 6.89476, "inH2o": 27.7076, "cmH2o": 70.307, "hpa": 68.94757293},
                             "kg/cm2" :{"Pascal":98066.5, "bar":0.980665, "psi":14.2233, "kg/cm2": 1, "mmH2o": 0.0001, "mmHg": 735.559, "inHg":28.959, "mbar": 980.665, "mpa": 0.0980665, "kpa": 98.0665, "inH2o": 394.095, "cmH2o": 1000, "hpa": 0.00102 },
                             "mmH2o" :{"Pascal":9.80665, "bar":10197.162129, "psi":703.069578, "kg/cm2": 10000, "mmH2o": 1, "mmHg": 0.07, "inHg":345.31554268, "mbar": 10.197162129779, "mpa":  0.00000980665, "kpa": 101.97162129779, "inH2o": 25.399999830047, "cmH2o": 0.1, "hpa": 0.098063},
                             "mmHg" :{"Pascal":133.322, "bar":0.00133322, "psi":0.0193368, "kg/cm2": 0.00135951, "mmH2o": 13.60, "mmHg": 1, "inHg":0.0393701, "mbar": 1.33322, "mpa": 0.000133322, "kpa": 0.133322, "inH2o": 0.535776, "cmH2o": 1.35951, "hpa": 0.75006156130624},
                             "inHg" :{"Pascal":3386.39, "bar":0.0338639, "psi":0.491154, "kg/cm2": 0.0345316, "mmH2o": 345.32, "mmHg": 25.4, "inHg":1, "mbar": 33.8639, "mpa": 0.00338639, "kpa": 3.38639, "inH2o": 13.6087, "cmH2o": 34.5316, "hpa": 33.863},
                             "mbar" :{"Pascal": 100, "bar":0.001, "psi":0.0145038, "kg/cm2": 0.00101972, "mmH2o": 10.20, "mmHg": 0.750062, "inHg":0.02953,"mbar": 1, "mpa": 0.0001, "kpa": 0.1, "inH2o": 0.401865, "cmH2o": 1.01972, "hpa": 1 },
                             "mpa" :{"Pascal":1000000, "bar":10, "psi":145.038, "kg/cm2": 10.1972, "mmH2o": 101974.428892, "mmHg": 7500.62, "inHg": 295.3,"mbar": 10000, "mpa": 1, "kpa": 1000, "inH2o": 4018.65, "cmH2o": 10197.2, "hpa": 10000 },
                             "kpa" :{"Pascal": 1000, "bar":0.01, "psi":0.145038, "kg/cm2": 0.0101972, "mmH2o": 101.97162, "mmHg": 7.50062, "inHg" :0.2953,"mbar": 10, "mpa": 0.001, "kpa": 1, "inH2o": 4.01865, "cmH2o": 10.1974, "hpa": 10 },
                             "inH2o" :{"Pascal":248.84, "bar":0.0024884, "psi":0.0360912, "kg/cm2":0.00253746, "mmH2o": 25.4, "mmHg": 1.86645, "inHg" :0.0734824,"mbar":2.4884, "mpa": 0.00024884, "kpa": 0.24884, "inH2o": 1, "cmH2o": 2.53746, "hpa": 0.4014630},
                             "cmH2o" :{"Pascal":98.0665, "bar":0.000980665, "psi":0.0142233, "kg/cm2": 0.001, "mmH2o": 10.00027, "mmHg": 0.735559, "inHg": 0.028959,"mbar": 0.980665, "mpa": 0.0000980665, "kpa": 0.0980665, "inH2o":0.394095, "cmH2o":1, "hpa": 0.980638},
                             "hpa" :{"Pascal": 100, "bar":0.001, "psi":0.0145037, "kg/cm2": 0.00102, "mmH2o": 10.20, "mmHg": 0.75006157, "inHg": 0.0295299,"mbar": 1, "mpa": 0.0001, "kpa": 0.1, "inH2o": 0.4015, "cmH2o": 1.019744, "hpa": 1},}





def pr_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit, diff, allinstru_list, temp_var, scope, calibration_location):



    myinstru = []
    nom_N = cal_point

    scope_lower_capability = scope.lower_capability
    scope_units = scope.units
    scope_result = scope.result_type

    #print(scope_lower_capability, "ggggggg sggggggggg eyyyyyyyyyyy hhhhhhhhhhh")

    scope_degits_count = str(float(scope_lower_capability))
    scope_rounding = scope_degits_count[::-1].find('.')
    unit_conversion_scoping = pressure_unit_conversion[obsUnit][scope_units]

    lc_duc_count = str(float(least_count))
    lc_duc_count_digit = lc_duc_count[::-1].find('.')
    # try:
    #     lc_duc_count = str(least_count)
    #     lc_duc_count_digit = lc_duc_count[::-1].find('.')
    #     if int(obs_count_digit) < 0:
    #         print(lc_duc_count_digit, cal_point, "ppppdjudhfuhd fudhdufhdufhud hfudhfudh")
    #         lc_duc_count = str(float(least_count))
    #         lc_duc_count_digit = lc_duc_count[::-1].find('.')
    # except:
    #     pass





    obs_count = str(float(obs2))
    obs_count_digit = obs_count[::-1].find('.')
    try:
        obs_count = str(obs2)
        obs_count_digit = obs_count[::-1].find('.')
        if int(obs_count_digit) < 0:
            obs_count = str(float(obs2))
            obs_count_digit = obs_count[::-1].find('.')
    except:
        pass




    try:
        for i in allinstru_list:
            ids = i['instrument']
            abc = instrumentMaster.objects.get(id=ids)

            myinstru.append(abc)

    except:

        for j in allinstru_list:
            myinstru.append(j)

    multiplyer = pressure_unit_conversion[nomUnit][obsUnit]

    if obs3 == None or obs3 == "":
        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)

        dof = 2
        list = [f1, f2]

        maxf = max(list)
        minf = min(list)

        hystersis = maxf - minf
        zeroOffset = maxf - minf

        avgpr = (f1 + f2) / 2

        list_obsn = [float(f1), float(f2)]
        obs_sum = f1 + f2
        new_avg = obs_sum / 2
        avg_after_conver = avgpr -nom_val
        dvdr = 2
        cklem = 1

    elif obs4 == None or obs4 == "":

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)

        dof = 3

        list = [f1, f2, f3]

        maxf = max(list)
        minf = min(list)

        hystersis = maxf - minf
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3) / 2 + f2) / 2

        list_obsn = [float(f1), float(f2), float(f3)]
        obs_sum = f1 + f2 + f3
        new_avg = obs_sum / 3
        avg_after_conver = avgpr -nom_val
        dvdr = 3
        cklem =2



    elif obs5 == None or obs5 == "":

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)
        f4 = float(obs4)

        dof = 4

        val1 = f2-f1
        val2 = f4-f3
        valf =abs(val1)+abs(val2)

        list = [f1, f2, f3, f4]

        maxf = max(list)
        minf = min(list)

        hystersis = valf/2
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3) / 2 + (f2 + f4) / 2) / 2

        list_obsn = [float(f1), float(f2), float(f3), float(f4)]
        obs_sum = f1 + f2 + f3 + f4
        new_avg = obs_sum / 4
        avg_after_conver = avgpr -nom_val
        dvdr = 4
        cklem = 3

    elif obs6 == None or obs6 == "":

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)
        f4 = float(obs4)
        f5 = float(obs5)

        dof = 5

        list = [f1, f2, f3, f4, f5]

        maxf = max(list)
        minf = min(list)

        hystersis = maxf - minf
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4) / 2) / 2

        list_obsn = [float(f1), float(f2), float(f3), float(f4), float(f5)]
        obs_sum = f1 + f2 + f3 + f4 + f5
        new_avg = obs_sum / 5
        avg_after_conver = avgpr -nom_val
        dvdr = 5
        cklem = 4

    else:

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)
        f4 = float(obs4)
        f5 = float(obs5)
        f6 = float(obs6)

        dof = 6

        list = [f1, f2, f3, f4, f5, f6]

        maxf = max(list)
        minf = min(list)

        val1 = f2-f1
        val2 = f4-f3
        val3 = f6-f5
        valf =abs(val1)+abs(val2)+abs(val3)

        hystersis = valf/3
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4 + f6) / 3) / 2
        list_obsn = [float(f1), float(f2), float(f3), float(f4), float(f5), float(f6)]
        obs_sum = f1 + f2 + f3 + f4 + f5 + f6
        new_avg = obs_sum / 6
        avg_after_conver = avgpr -nom_val
        dvdr = 6
        cklem = 5

    erro_std_uuc = float(cal_point) - new_avg
    new_std = stdev(list_obsn, ddof=1)

    std_dev = new_std
    ua = std_dev / math.sqrt(dvdr)

    ub1 = 0
    ub2 = 0
    ub3 = 0
    uc = 0
    veff = 0
    UmV = 0
    Up = 0
    ub4 = 0

    totalDict = {}
    errorx=[]



    totalDict['ua'] = ua

    duc_unc = UUCMaster.objects.get(id=duc_id)

    print(duc_unc.id, "lllllllllllllllllllllllllllllllx djjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")

    try:
        if duc_unc.uuc_unit == 'obsUnit':
            least_countn= float(least_count)
        # else:
        #     least_count= float(least_count)*pressure_unit_conversion[nomUnit][obsUnit]
    except:
        least_countn= float(least_count)*pressure_unit_conversion[nomUnit][obsUnit]

    #print(least_countn, "least_count least_count v least_count least_count vv least_count least_count v")




    for items in duc_unc.master_uncertainty.first().ub.all():

        if items.parameters == 'uncertainty':

            instruQ = []
            for j in myinstru:
                print(j, "ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                for k in items.instrument.i_blueprint.all():
                    print(k, "loooooooooooooooojjjjjjjjjjjjjjjjjjjjjjjjjjhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                    if j == k:
                        instruQ.append(j)

            master_used = instruQ[0]

            #recheck again for optimization

            cert = Certificate.objects.get(instrument_cert = master_used)

            pressure_certificate = cert.pr_instru_cert_item.all()

            correction_min_list = []
            correction_max_list = []

            min_dicts = {}
            max_dicts = {}

            for certitm in pressure_certificate:
                avg_obs_c = float(avgpr)*pressure_unit_conversion[obsUnit][certitm.uuc_unit]
                uucValue = float(certitm.uuc)


                if float(uucValue) <= float(avg_obs_c):
                    l = certitm
                    correction_min_list.append(l)

                elif float(uucValue) > float(avg_obs_c):
                    m = certitm
                    correction_max_list.append(m)


            for i in correction_min_list:
                minlength = len(correction_min_list)
                for k in range(minlength):
                    min_dicts[i] = float(i.uuc)

            for i in correction_max_list:
                minlength = len(correction_max_list)
                for k in range(minlength):
                    max_dicts[i] = float(i.uuc)

            min_cert_item = max(min_dicts, key=lambda x: min_dicts[x])
            max_cert_item = min(max_dicts, key= lambda x: max_dicts[x])




            error_nom = float(min_cert_item.error)-float(max_cert_item.error)
            erro_dom = float(max_cert_item.uuc) - float(min_cert_item.uuc)
            error = error_nom/erro_dom

            # print("/n /n", error, cal_point)
            errorx.append(error)

            print(avgpr, obs_count_digit, roundup(avgpr, int(obs_count_digit)), "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")

            abcdef = roundup(avg_obs_c, int(obs_count_digit))
            avgpr = roundup(avgpr, int(obs_count_digit))
            print(cal_point, avgpr, "999999999999999999999999999999999999999999999999999999999999999999999999999999999")

            multicerti = pressure_unit_conversion[max_cert_item.uuc_unit][nomUnit]
            f23 =float(max_cert_item.meanvalue)
            correction_val1 = float(abcdef)-f23
            correction_val2= correction_val1*error
            correction_val3 = float(max_cert_item.error)
            correction = (correction_val2 - correction_val3)

            after_correction = (float(avg_obs_c)+correction)*pressure_unit_conversion[max_cert_item.uuc_unit][obsUnit]
            expended_uncertainity = float(max_cert_item.uncertainity)
            expended_uncertainity_unitN = expended_uncertainity*pressure_unit_conversion[max_cert_item.uuc_unit][obsUnit]



            itemd = items.instrument
            # abd = itemd.uncertainty
            abd = expended_uncertainity_unitN
            mainUn =abd

            ub1 = float(abd) / 2
            totalDict[items.name] = ub1


        elif items.parameters == 'lc':
            abd = float(least_countn)

            if items.distribution == 'Normal':

                myV = 2
                ub2 = float(abd)/myV
            elif items.distribution == 'Rectangular':
                least_count_new_values = abd/2
                valneed_inbudget = least_count_new_values
                myV = math.sqrt(3)

                ub2 = least_count_new_values/myV
            totalDict[items.name] = ub2


        elif items.parameters == 'zero_offset':
            zeroOffset = float(diff)

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)
            valN = zeroOffset/2


            ub3 = valN/myV
            totalDict[items.name] = ub3

        elif items.parameters == 'head_correction':
            instruQ = []
            for j in myinstru:
                for k in items.instrument.i_blueprint.all():
                    if j == k:
                        instruQ.append(j)

            master_used = instruQ[0]
            head_correction = float(master_used.head_correction)
            head_correction_unit = master_used.head_correction_unit
            unit_conx = pressure_unit_conversion[head_correction_unit][obsUnit]
            head_correctionN = head_correction*unit_conx

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)

            ub4 = head_correctionN/myV
            totalDict[items.name] = ub4


        elif items.parameters == 'temp_variation':

            if calibration_location == 'Site':
                temp_limit = 5
            else:
                temp_limit = 2


            cal_point = float(cal_point)
            val1 = cal_point*0.000023*pressure_unit_conversion[nomUnit][obsUnit]
            temp_varient = val1*temp_limit

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)

            ub5 = temp_varient/myV
            totalDict[items.name] = ub5


        elif items.parameters == 'hysterisis':
            hystersis = hystersis

            if items.distribution == 'Normal':

                myV = 2
            elif items.distribution == 'Rectangular':

                myV = math.sqrt(3)

            ub6 = hystersis/myV
            totalDict[items.name] = ub6


    testDict = totalDict


    myList = totalDict.keys()




    sumINeed = 0
    for item, value in testDict.items():
        sumINeed += pow(float(value), 2)

    uc = math.sqrt(sumINeed)

    veff = pow(uc, 4)


    if ua != 0:
        veff = veff * cklem / pow(ua, 4)
        try:
            K = getkfactor(veff)
        except:
            K=2
    else:
        veff = 'Infinity'
        K = 2

    UmV = uc * K
    UmV_budget = UmV

    try:
        Up = UmV * dof / float(cal_point)
        totalDict['Up'] = Up
    except:
        totalDict['Up'] = 'Infinity'

    # apply nabl scope for % only, if need then extended

    if scope_result == 'unit':
        unit_conversion = pressure_unit_conversion[scope_units][nomUnit]
        xn = float(scope_lower_capability)*unit_conversion
        if UmV <= xn:
            UmV = xn
        else:
            UmV=UmV
    else:
        if Up <= float(scope_lower_capability):
            Up = float(scope_lower_capability)
        else:
            Up = Up

    lc_duc_count_digit_int = int(lc_duc_count_digit) + 1
    totalDict['Up'] = roundup(Up, int(lc_duc_count_digit)+1)
    #print(scope_rounding)
    #print(totalDict['Up'])
    totalDict['Up'] = "{:.{}f}".format(totalDict['Up'], int(lc_duc_count_digit)+1)

    UmvN = UmV*unit_conversion_scoping
    if float(scope_lower_capability)>UmvN:
        UmvNN = float(scope_lower_capability)
    else:
        UmvNN = UmvN


    totalDict['uc'] =  roundup(uc, 6 )
    totalDict['uc'] = "{:.{}f}".format(totalDict['uc'], 6)

    totalDict['cal_point'] = cal_point
    totalDict['veff'] = veff
    totalDict['valneed_inbudget'] = valneed_inbudget
    totalDict['std_dev'] = std_dev
    totalDict['erro_std_uuc'] = erro_std_uuc
    totalDict['scope_units'] = scope_units
    scope_rounding_int = int(scope_rounding)



    abcd = avgpr

    m2 = int(obs_count_digit)+ 2
    abcd = roundup(abcd, int(obs_count_digit)+ 2)


    abcd = roundup(abcd, (int(obs_count_digit)+ 1))
    print(f'\n \n \n \n \n Correction factor: - {correction} , Cal Point: {cal_point}, ABCD(AVGPR): - {abcd}, {avgpr}')
    # avgpr2 = abcd
    aftercorr = float(abcd)+float(correction)
    print(f'After Correction :- {aftercorr}')
    totalDict['avg_after_conver'] = \
    roundup((nom_val-aftercorr), int(obs_count_digit))
    totalDict['avg_after_conver'] = "{:.{}f}".format(totalDict['avg_after_conver'], int(obs_count_digit))



    scope_degits_count = str(round(float(obs1), int(obs_count_digit)))
    scope_rounding = scope_degits_count[::-1].find('.')

    totalDict['avgpr'] = roundup(avgpr,int(obs_count_digit))

    totalDict['avgpr'] = "{:.{}f}".format(totalDict['avgpr'], int(obs_count_digit))


    totalDict['master_uncertainity'] = mainUn
    totalDict['zeroOffset'] = roundup(zeroOffset, int(obs_count_digit))
    totalDict['zeroOffset'] = "{:.{}f}".format(totalDict['zeroOffset'], int(obs_count_digit))

    totalDict['error_uuc_std'] = roundup(float(cal_point)-(float(avgpr)*pressure_unit_conversion[obsUnit][nomUnit]), int(obs_count_digit))
    totalDict['error_uuc_std'] = "{:.{}f}".format(totalDict['error_uuc_std'], int(obs_count_digit))
    aftercorrx=aftercorr

    totalDict['aftercorr'] =  roundup(aftercorr, int(obs_count_digit))
    totalDict['aftercorr'] = "{:.{}f}".format(totalDict['aftercorr'], int(obs_count_digit))





    totalDict['after_correction'] = after_correction
    totalDict['correction_mutiplyer'] = error

    totalDict['error'] = correction
    newvar = float(aftercorr) - float(cal_point)
    totalDict['newvar'] = roundup(newvar, int(scope_rounding))


    totalDict['U']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], int(scope_rounding))
    totalDict['U'] = "{:.{}f}".format(totalDict['U'], int(scope_rounding))

    totalDict['U_extract']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], 6)
    totalDict['U_extract'] = "{:.{}f}".format(totalDict['U_extract'], 6)

    totalDict['UmV_budget'] = roundup(UmV_budget * pressure_unit_conversion[obsUnit][nomUnit], 6)
    totalDict['UmV_budget'] = "{:.{}f}".format(totalDict['UmV_budget'], 6)



    totalDict['U_cert']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], int(obs_count_digit))
    totalDict['U_cert'] = "{:.{}f}".format(totalDict['U_cert'], int(obs_count_digit))

    totalDict['U_extract_sheet']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], int(lc_duc_count_digit)+1)
    totalDict['U_extract_sheet'] = "{:.{}f}".format(totalDict['U_extract_sheet'], int(lc_duc_count_digit)+1)


    totalDict['newvar'] = "{:.{}f}".format(totalDict['newvar'], int(scope_rounding))
    totalDict['hystersis'] = roundup(hystersis, 6)
    totalDict['hystersis'] = "{:.{}f}".format(totalDict['hystersis'], 6)
    totalDict['std_val_after_conv'] = roundup(aftercorrx*pressure_unit_conversion[obsUnit][nomUnit], int(obs_count_digit))
    totalDict['std_val_after_conv'] = "{:.{}f}".format(totalDict['std_val_after_conv'], int(obs_count_digit))

    obs_count_digit = int(obs_count_digit)
    #print(obs_count_digit)
    try:
        totalDict['error'] = roundup(float(totalDict['error']), 4)
        totalDict['error'] = "{:.{}f}".format(totalDict['error'], 4)
    except:
        pass
    try:
        totalDict['veff'] = roundup(float(veff),6)
        totalDict['veff'] = "{:.{}f}".format(totalDict['veff'], 6)
    except:
        totalDict['veff'] = "Infinity"
    totalDict['ua'] = roundup(ua, 8)
    totalDict['ua'] = "{:.{}f}".format(totalDict['ua'], 8)
    totalDict['std'] = roundup(std_dev, int(obs_count_digit)+2)
    totalDict['std'] = "{:.{}f}".format(totalDict['std'], int(obs_count_digit)+2)
    scope_rounding_int = scope_rounding_int + 3


    totalDict['ub1'] = roundup(totalDict['ub1'], 8 )
    totalDict['ub1'] = "{:.{}f}".format(totalDict['ub1'], 8)
    totalDict['ub2'] = roundup(totalDict['ub2'], 8)
    totalDict['ub2'] = "{:.{}f}".format(totalDict['ub2'], 8)
    totalDict['ub3'] = roundup(totalDict['ub3'], 8)
    totalDict['ub3'] = "{:.{}f}".format(totalDict['ub3'], 8)
    totalDict['ub4'] = roundup(totalDict['ub4'], 8)
    totalDict['ub4'] = "{:.{}f}".format(totalDict['ub4'], 8)
    try:
        totalDict['ub5'] = roundup(totalDict['ub5'], 8)
        totalDict['ub5'] = "{:.{}f}".format(totalDict['ub5'], 8)
    except:
        pass

    try:
        totalDict['ub6'] = roundup(totalDict['ub6'], 8)
        totalDict['ub6'] = "{:.{}f}".format(totalDict['ub6'], 8)
    except:
        pass

    totalDict['cal_point']=cal_point

    new_correction = float(totalDict['std_val_after_conv'])-float(nom_N)

    totalDict['new_correction'] = roundup(new_correction, int(obs_count_digit) )
    totalDict['new_correction'] = "{:.{}f}".format(totalDict['new_correction'], int(obs_count_digit))

    totalDict['K']=K


    return totalDict


def prMulti_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit, diff, allinstru_list, temp_var, scope, calibration_location):



    myinstru = []
    nom_N = cal_point

    scope_lower_capability = scope.lower_capability
    scope_units = scope.units
    scope_result = scope.result_type

    #print(scope_lower_capability, "ggggggg sggggggggg eyyyyyyyyyyy hhhhhhhhhhh")

    scope_degits_count = str(float(scope_lower_capability))
    scope_rounding = scope_degits_count[::-1].find('.')
    unit_conversion_scoping = pressure_unit_conversion[obsUnit][scope_units]

    lc_duc_count = str(float(least_count))
    lc_duc_count_digit = lc_duc_count[::-1].find('.')
    # try:
    #     lc_duc_count = str(least_count)
    #     lc_duc_count_digit = lc_duc_count[::-1].find('.')
    #     if int(obs_count_digit) < 0:
    #         print(lc_duc_count_digit, cal_point, "ppppdjudhfuhd fudhdufhdufhud hfudhfudh")
    #         lc_duc_count = str(float(least_count))
    #         lc_duc_count_digit = lc_duc_count[::-1].find('.')
    # except:
    #     pass





    obs_count = str(float(obs2))
    obs_count_digit = obs_count[::-1].find('.')
    try:
        obs_count = str(obs2)
        obs_count_digit = obs_count[::-1].find('.')
        if int(obs_count_digit) < 0:
            obs_count = str(float(obs2))
            obs_count_digit = obs_count[::-1].find('.')
    except:
        pass




    try:
        for i in allinstru_list:
            ids = i['instrument']
            abc = instrumentMaster.objects.get(id=ids)

            myinstru.append(abc)

    except:

        for j in allinstru_list:
            myinstru.append(j)

    multiplyer = pressure_unit_conversion[nomUnit][obsUnit]

    if obs3 == None or obs3 == "":
        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)

        dof = 2
        list = [f1, f2]

        maxf = max(list)
        minf = min(list)

        hystersis = maxf - minf
        zeroOffset = maxf - minf

        avgpr = (f1 + f2) / 2

        list_obsn = [float(f1), float(f2)]
        obs_sum = f1 + f2
        new_avg = obs_sum / 2
        avg_after_conver = avgpr -nom_val
        dvdr = 2
        cklem = 1

    elif obs4 == None or obs4 == "":

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)

        dof = 3

        list = [f1, f2, f3]

        maxf = max(list)
        minf = min(list)

        hystersis = maxf - minf
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3) / 2 + f2) / 2

        list_obsn = [float(f1), float(f2), float(f3)]
        obs_sum = f1 + f2 + f3
        new_avg = obs_sum / 3
        avg_after_conver = avgpr -nom_val
        dvdr = 3
        cklem =2



    elif obs5 == None or obs5 == "":

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)
        f4 = float(obs4)

        dof = 4

        val1 = f2-f1
        val2 = f4-f3
        valf =abs(val1)+abs(val2)

        list = [f1, f2, f3, f4]

        maxf = max(list)
        minf = min(list)

        hystersis = valf/2
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3) / 2 + (f2 + f4) / 2) / 2

        list_obsn = [float(f1), float(f2), float(f3), float(f4)]
        obs_sum = f1 + f2 + f3 + f4
        new_avg = obs_sum / 4
        avg_after_conver = avgpr -nom_val
        dvdr = 4
        cklem = 3

    elif obs6 == None or obs6 == "":

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)
        f4 = float(obs4)
        f5 = float(obs5)

        dof = 5

        list = [f1, f2, f3, f4, f5]

        maxf = max(list)
        minf = min(list)

        hystersis = maxf - minf
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4) / 2) / 2

        list_obsn = [float(f1), float(f2), float(f3), float(f4), float(f5)]
        obs_sum = f1 + f2 + f3 + f4 + f5
        new_avg = obs_sum / 5
        avg_after_conver = avgpr -nom_val
        dvdr = 5
        cklem = 4

    else:

        nom_val = float(cal_point) * multiplyer
        f1 = float(obs1)
        f2 = float(obs2)
        f3 = float(obs3)
        f4 = float(obs4)
        f5 = float(obs5)
        f6 = float(obs6)

        dof = 6

        list = [f1, f2, f3, f4, f5, f6]

        maxf = max(list)
        minf = min(list)

        val1 = f2-f1
        val2 = f4-f3
        val3 = f6-f5
        valf =abs(val1)+abs(val2)+abs(val3)

        hystersis = valf/3
        zeroOffset = maxf - minf

        avgpr = ((f1 + f3 + f5) / 3 + (f2 + f4 + f6) / 3) / 2
        list_obsn = [float(f1), float(f2), float(f3), float(f4), float(f5), float(f6)]
        obs_sum = f1 + f2 + f3 + f4 + f5 + f6
        new_avg = obs_sum / 6
        avg_after_conver = avgpr -nom_val
        dvdr = 6
        cklem = 5

    erro_std_uuc = float(cal_point) - new_avg
    new_std = stdev(list_obsn, ddof=1)

    std_dev = new_std
    ua = std_dev / math.sqrt(dvdr)

    ub1 = 0
    ub2 = 0
    ub3 = 0
    uc = 0
    veff = 0
    UmV = 0
    Up = 0
    ub4 = 0

    totalDict = {}
    errorx=[]



    totalDict['ua'] = ua

    duc_unc = UUCMaster.objects.get(id=duc_id)


    try:
        if duc_unc.uuc_unit == 'obsUnit':
            least_countn= float(least_count)
        # else:
        #     least_count= float(least_count)*pressure_unit_conversion[nomUnit][obsUnit]
    except:
        least_countn= float(least_count)*pressure_unit_conversion[nomUnit][obsUnit]

    #print(least_countn, "least_count least_count v least_count least_count vv least_count least_count v")




    for items in duc_unc.master_uncertainty.first().ub.all():

        if items.parameters == 'uncertainty':

            instruQ = []
            for j in myinstru:
               instruQ.append(j)

            master_used = instruQ[0]

            #recheck again for optimization

            cert = Certificate.objects.get(instrument_cert = master_used)

            pressure_certificate = cert.pr_instru_cert_item.all()

            correction_min_list = []
            correction_max_list = []

            min_dicts = {}
            max_dicts = {}

            for certitm in pressure_certificate:
                avg_obs_c = float(avgpr)*pressure_unit_conversion[obsUnit][certitm.uuc_unit]
                uucValue = float(certitm.uuc)


                if float(uucValue) <= float(avg_obs_c):
                    l = certitm
                    correction_min_list.append(l)

                elif float(uucValue) > float(avg_obs_c):
                    m = certitm
                    correction_max_list.append(m)


            for i in correction_min_list:
                minlength = len(correction_min_list)
                for k in range(minlength):
                    min_dicts[i] = float(i.uuc)

            for i in correction_max_list:
                minlength = len(correction_max_list)
                for k in range(minlength):
                    max_dicts[i] = float(i.uuc)

            min_cert_item = max(min_dicts, key=lambda x: min_dicts[x])
            max_cert_item = min(max_dicts, key= lambda x: max_dicts[x])




            error_nom = float(min_cert_item.error)-float(max_cert_item.error)
            erro_dom = float(max_cert_item.uuc) - float(min_cert_item.uuc)
            error = error_nom/erro_dom

            # print("/n /n", error, cal_point)
            errorx.append(error)

            print(avgpr, obs_count_digit, roundup(avgpr, int(obs_count_digit)), "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")

            abcdef = roundup(avg_obs_c, int(obs_count_digit))
            avgpr = roundup(avgpr, int(obs_count_digit))
            print(cal_point, avgpr, "999999999999999999999999999999999999999999999999999999999999999999999999999999999")

            multicerti = pressure_unit_conversion[max_cert_item.uuc_unit][nomUnit]
            f23 =float(max_cert_item.meanvalue)
            correction_val1 = float(abcdef)-f23
            correction_val2= correction_val1*error
            correction_val3 = float(max_cert_item.error)
            correction = (correction_val2 - correction_val3)

            after_correction = (float(avg_obs_c)+correction)*pressure_unit_conversion[max_cert_item.uuc_unit][obsUnit]
            expended_uncertainity = float(max_cert_item.uncertainity)
            expended_uncertainity_unitN = expended_uncertainity*pressure_unit_conversion[max_cert_item.uuc_unit][obsUnit]



            itemd = items.instrument
            # abd = itemd.uncertainty
            abd = expended_uncertainity_unitN
            mainUn =abd

            ub1 = float(abd) / 2
            totalDict[items.name] = ub1


        elif items.parameters == 'lc':
            abd = float(least_countn)

            if items.distribution == 'Normal':

                myV = 2
                ub2 = float(abd)/myV
            elif items.distribution == 'Rectangular':
                least_count_new_values = abd/2
                valneed_inbudget = least_count_new_values
                myV = math.sqrt(3)

                ub2 = least_count_new_values/myV
            totalDict[items.name] = ub2


        elif items.parameters == 'zero_offset':
            zeroOffset = float(diff)

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)
            valN = zeroOffset/2


            ub3 = valN/myV
            totalDict[items.name] = ub3

        elif items.parameters == 'head_correction':
            instruQ = []
            for j in myinstru:
                for k in items.instrument.i_blueprint.all():
                    if j == k:
                        instruQ.append(j)

            master_used = instruQ[0]
            head_correction = float(master_used.head_correction)
            head_correction_unit = master_used.head_correction_unit
            unit_conx = pressure_unit_conversion[head_correction_unit][obsUnit]
            head_correctionN = head_correction*unit_conx

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)

            ub4 = head_correctionN/myV
            totalDict[items.name] = ub4


        elif items.parameters == 'temp_variation':

            if calibration_location == 'Site':
                temp_limit = 5
            else:
                temp_limit = 2


            cal_point = float(cal_point)
            val1 = cal_point*0.000023*pressure_unit_conversion[nomUnit][obsUnit]
            temp_varient = val1*temp_limit

            if items.distribution == 'Normal':
                myV = 2
            elif items.distribution == 'Rectangular':
                myV = math.sqrt(3)

            ub5 = temp_varient/myV
            totalDict[items.name] = ub5


        elif items.parameters == 'hysterisis':
            hystersis = hystersis

            if items.distribution == 'Normal':

                myV = 2
            elif items.distribution == 'Rectangular':

                myV = math.sqrt(3)

            ub6 = hystersis/myV
            totalDict[items.name] = ub6


    testDict = totalDict


    myList = totalDict.keys()




    sumINeed = 0
    for item, value in testDict.items():
        sumINeed += pow(float(value), 2)

    uc = math.sqrt(sumINeed)

    veff = pow(uc, 4)


    if ua != 0:
        veff = veff * cklem / pow(ua, 4)
        try:
            K = getkfactor(veff)
        except:
            K=2
    else:
        veff = 'Infinity'
        K = 2

    UmV = uc * K
    UmV_budget = UmV

    try:
        Up = UmV * dof / float(cal_point)
        totalDict['Up'] = Up
    except:
        totalDict['Up'] = 'Infinity'

    # apply nabl scope for % only, if need then extended

    if scope_result == 'unit':
        unit_conversion = pressure_unit_conversion[scope_units][nomUnit]
        xn = float(scope_lower_capability)*unit_conversion
        if UmV <= xn:
            UmV = xn
        else:
            UmV=UmV
    else:
        if Up <= float(scope_lower_capability):
            Up = float(scope_lower_capability)
        else:
            Up = Up

    lc_duc_count_digit_int = int(lc_duc_count_digit) + 1
    totalDict['Up'] = roundup(Up, int(lc_duc_count_digit)+1)
    #print(scope_rounding)
    #print(totalDict['Up'])
    totalDict['Up'] = "{:.{}f}".format(totalDict['Up'], int(lc_duc_count_digit)+1)

    UmvN = UmV*unit_conversion_scoping
    if float(scope_lower_capability)>UmvN:
        UmvNN = float(scope_lower_capability)
    else:
        UmvNN = UmvN


    totalDict['uc'] =  roundup(uc, 6 )
    totalDict['uc'] = "{:.{}f}".format(totalDict['uc'], 6)

    totalDict['cal_point'] = cal_point
    totalDict['veff'] = veff
    totalDict['valneed_inbudget'] = valneed_inbudget
    totalDict['std_dev'] = std_dev
    totalDict['erro_std_uuc'] = erro_std_uuc
    totalDict['scope_units'] = scope_units
    scope_rounding_int = int(scope_rounding)



    abcd = avgpr

    m2 = int(obs_count_digit)+ 2
    abcd = roundup(abcd, int(obs_count_digit)+ 2)


    abcd = roundup(abcd, (int(obs_count_digit)+ 1))
    print(f'\n \n \n \n \n Correction factor: - {correction} , Cal Point: {cal_point}, ABCD(AVGPR): - {abcd}, {avgpr}')
    # avgpr2 = abcd
    aftercorr = float(abcd)+float(correction)
    print(f'After Correction :- {aftercorr}')
    totalDict['avg_after_conver'] = \
    roundup((nom_val-aftercorr), int(obs_count_digit))
    totalDict['avg_after_conver'] = "{:.{}f}".format(totalDict['avg_after_conver'], int(obs_count_digit))



    scope_degits_count = str(round(float(obs1), int(obs_count_digit)))
    scope_rounding = scope_degits_count[::-1].find('.')

    totalDict['avgpr'] = roundup(avgpr,int(obs_count_digit))

    totalDict['avgpr'] = "{:.{}f}".format(totalDict['avgpr'], int(obs_count_digit))


    totalDict['master_uncertainity'] = mainUn
    totalDict['zeroOffset'] = roundup(zeroOffset, int(obs_count_digit))
    totalDict['zeroOffset'] = "{:.{}f}".format(totalDict['zeroOffset'], int(obs_count_digit))

    totalDict['error_uuc_std'] = roundup(float(cal_point)-(float(avgpr)*pressure_unit_conversion[obsUnit][nomUnit]), int(obs_count_digit))
    totalDict['error_uuc_std'] = "{:.{}f}".format(totalDict['error_uuc_std'], int(obs_count_digit))
    aftercorrx=aftercorr

    totalDict['aftercorr'] =  roundup(aftercorr, int(obs_count_digit))
    totalDict['aftercorr'] = "{:.{}f}".format(totalDict['aftercorr'], int(obs_count_digit))





    totalDict['after_correction'] = after_correction
    totalDict['correction_mutiplyer'] = error

    totalDict['error'] = correction
    newvar = float(aftercorr) - float(cal_point)
    totalDict['newvar'] = roundup(newvar, int(scope_rounding))


    totalDict['U']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], int(scope_rounding))
    totalDict['U'] = "{:.{}f}".format(totalDict['U'], int(scope_rounding))

    totalDict['U_extract']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], 6)
    totalDict['U_extract'] = "{:.{}f}".format(totalDict['U_extract'], 6)

    totalDict['UmV_budget'] = roundup(UmV_budget * pressure_unit_conversion[obsUnit][nomUnit], 6)
    totalDict['UmV_budget'] = "{:.{}f}".format(totalDict['UmV_budget'], 6)



    totalDict['U_cert']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], int(obs_count_digit))
    totalDict['U_cert'] = "{:.{}f}".format(totalDict['U_cert'], int(obs_count_digit))

    totalDict['U_extract_sheet']= roundup(UmV*pressure_unit_conversion[obsUnit][nomUnit], int(lc_duc_count_digit)+1)
    totalDict['U_extract_sheet'] = "{:.{}f}".format(totalDict['U_extract_sheet'], int(lc_duc_count_digit)+1)


    totalDict['newvar'] = "{:.{}f}".format(totalDict['newvar'], int(scope_rounding))
    totalDict['hystersis'] = roundup(hystersis, 6)
    totalDict['hystersis'] = "{:.{}f}".format(totalDict['hystersis'], 6)
    totalDict['std_val_after_conv'] = roundup(aftercorrx*pressure_unit_conversion[obsUnit][nomUnit], int(obs_count_digit))
    totalDict['std_val_after_conv'] = "{:.{}f}".format(totalDict['std_val_after_conv'], int(obs_count_digit))

    obs_count_digit = int(obs_count_digit)
    #print(obs_count_digit)
    try:
        totalDict['error'] = roundup(float(totalDict['error']), 4)
        totalDict['error'] = "{:.{}f}".format(totalDict['error'], 4)
    except:
        pass
    try:
        totalDict['veff'] = roundup(float(veff),6)
        totalDict['veff'] = "{:.{}f}".format(totalDict['veff'], 6)
    except:
        totalDict['veff'] = "Infinity"
    totalDict['ua'] = roundup(ua, 8)
    totalDict['ua'] = "{:.{}f}".format(totalDict['ua'], 8)
    totalDict['std'] = roundup(std_dev, int(obs_count_digit)+2)
    totalDict['std'] = "{:.{}f}".format(totalDict['std'], int(obs_count_digit)+2)
    scope_rounding_int = scope_rounding_int + 3


    totalDict['ub1'] = roundup(totalDict['ub1'], 8 )
    totalDict['ub1'] = "{:.{}f}".format(totalDict['ub1'], 8)
    totalDict['ub2'] = roundup(totalDict['ub2'], 8)
    totalDict['ub2'] = "{:.{}f}".format(totalDict['ub2'], 8)
    totalDict['ub3'] = roundup(totalDict['ub3'], 8)
    totalDict['ub3'] = "{:.{}f}".format(totalDict['ub3'], 8)
    totalDict['ub4'] = roundup(totalDict['ub4'], 8)
    totalDict['ub4'] = "{:.{}f}".format(totalDict['ub4'], 8)
    try:
        totalDict['ub5'] = roundup(totalDict['ub5'], 8)
        totalDict['ub5'] = "{:.{}f}".format(totalDict['ub5'], 8)
    except:
        pass

    try:
        totalDict['ub6'] = roundup(totalDict['ub6'], 8)
        totalDict['ub6'] = "{:.{}f}".format(totalDict['ub6'], 8)
    except:
        pass

    totalDict['cal_point']=cal_point

    new_correction = float(totalDict['std_val_after_conv'])-float(nom_N)

    totalDict['new_correction'] = roundup(new_correction, int(obs_count_digit) )
    totalDict['new_correction'] = "{:.{}f}".format(totalDict['new_correction'], int(obs_count_digit))

    totalDict['K']=K


    return totalDict




def MassItemUncertainty(duc_id,lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1, obs2, obs3, linearity,least_count):
    duc = UUCMaster.objects.get(id=duc_id)
    if lc_duc:
        pass
    else:
        lc_duc=''
    obs1 = float(obs1)
    obs2 = float(obs2)
    obs3 = float(obs3)

    linearity = float(linearity)
    obs1 = roundup(obs1, 2)
    listobserve=[obs1, obs2, obs3,linearity]
    ua = stdev(listobserve, ddof=1)
    ua=ua/math.sqrt(10)

    # rangeP = float(rangeP)
    # cal_point_unit='A'

    ub1 = 0
    ub2=0
    ub3=0
    uc = 0
    veff = 0
    UmV = 0
    Up = 0
    ub4=0
    duc_unc = UUCMaster.objects.get(id=duc_id)
    unc_need = 0
    temp1=20
    # temp2 = abs((temp1)-float(temp))




    totalDict = {}
    for items in duc_unc.master_uncertainty.first().ub.all():


        if items.parameters=='drift':
            itemd = items.instrument
            myV= math.sqrt(3)

            abd=itemd.drift

            m= float(abd)/2
            ub1=m/myV
            totalDict[items.name]=ub1
            #print(ub1,"satish")





        elif items.parameters=='uncertainty':
            itemd = items.instrument



            abd=itemd.uncertainty

            ub2=float(abd)/2
            totalDict[items.name]=ub2
            #print(ub2,"rahul")

        elif items.parameters=='lc':
            itemd = items.instrument
            abd=itemd.lc_resolution

            myV= math.sqrt(6)

            ub3=float(abd)/myV
            totalDict[items.name]=ub3


        elif items.parameters=='linearity':
            itemd = items.instrument
            abd=itemd.linearity



            ub4=float(abd)*0.577
            #print(ub4, "goku")
            totalDict[items.name]=ub4


        elif items.parameters=='eccentricity':
            itemd = items.instrument
            abd=itemd.eccentricity



            ub5=float(abd)/2
            myV= math.sqrt(3)
            ub5 = ub5/myV
            #print(ub5, "nehit")
            totalDict[items.name]=ub5






            # unc_need = 0
            # # #print("items-------")
            # abc = items.instrument.Mass_master_detail.all()
            #
            # for itemd in abc:
            #     if itemd.type=='1000':
            #         # #print("Vasu Is a1 ", itemd.type, cal_point)
            #         # #print("Vasu Is a2 ", itemd.info,cal_point_unit)
            #         # #print("Vasu Is a5 ", itemd.category, lc_duc_unit_parameter)
            #
            #      if itemd.type==cal_point and itemd.info==cal_point_unit and itemd.category==lc_duc_unit_parameter:
            #
            #         abd = itemd.uncertainty
            #         #print("abc", abdasfasffafafgaag)
            #         ub1 = float(abd)/2
            #         #print("abcd", ub1)
            #         # ub1 = format(ub1, 6)
            #         # ub1 = format(ub1, '.6f')
            #         ub1 = roundup(float(ub1), 6)
            #         # #print(format(0.00001357, '.8f'))
            #         #print("abcde", ub1)
        elif items.parameters=='lc':
            if items.distribution=='Normal':
                myV = 2
            elif items.distribution=='Rectangular':
                myV= math.sqrt(3)

            #print(lc_duc)
            #print("P")
            lc = float(lc_duc)/2
            ub2=lc/myV
            # ub2 = format(ub2,'.6f')



        elif items.parameters=='accuracy':
            unc_need = 0
            abc = items.instrument.et_master_detail.all()
            for itemd in abc:
                if itemd.type==cal_point and itemd.info==cal_point_unit and itemd.category==lc_duc_unit_parameter:
                    abd = itemd.accuracy
                    #print(abd)
                    ub3 = float(abd)
                    #print(ub3)
                    if items.distribution=='Normal':
                        myV = 2
                    elif items.distribution=='Rectangular':
                        myV= math.sqrt(3)
                    #print(myV)
                    ub3 = ub3/myV
                    #print("|||||||||||||||")
                    #print(ub3)
                    # ub1 = format(ub1, 6)
                    # ub3 = format(ub3, '.6f')




    #print("-----")
    # ub1 = float(ub1)
    # ub1 = roundup(float(ub1), 6)

    #print("ua")
    #print(ua)
    #print("ub1")
    #print(ub1)
    #print("ub2")
    #print(ub2)
    #print("ub3")

    #print("ub4", ub4)




    sumINeed= pow(ua, 2) + pow(ub1, 2) + pow(ub2, 2) + pow(ub3, 2) + pow(ub4, 2)

    # #print(sumINeed)
    uc = math.sqrt(sumINeed)
    #print("uc")
    #print(uc)

    veff = pow(uc,4)
    if ua!=0:
        veff = veff*4/pow(ua,4)
    else:
        veff='NA'
    #print("Veff")
    #print(veff)


    UmV = uc*2
    #print("umv")
    #print(UmV)
    Up = UmV*100/float(cal_point)


    #print("uP")
    #print(Up)

    return {'U':UmV, 'Up':Up, 'ua': ua, 'ub1': ub1, 'ub2': ub2, 'ub3':ub3, 'uc': uc, 'veff': veff }
