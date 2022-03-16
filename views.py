from django.shortcuts import render
from home.models import *
from master.models import *
from certificates.models import *
from certificates.forms import *
# Create your views here.
from django.contrib.auth.decorators import login_required
import django.utils.timezone as timezone
from django.db.models import Q
from .forms import *
from workorder.models import *
from srf.models import ServiceRequirement, SRFItem
from uuc.models import *
import datetime, time
from .models import Observation, etItem,dimobservation
from django.shortcuts import redirect
from django.http import HttpResponse
from .utils import etItemUncertainty, pr_ItemUncertainty,dimItemUncertainty, WeightItemUncertainty, WeighingItemUncertainty, prMulti_ItemUncertainty
# from xhtml2pdf import pisa
import os
from observation.global_constants import SOAKING_REQUIREMENT
monthN = timezone.now().month
yearN = timezone.now().year
todayN = timezone.now().day
dayN = timezone.now().day


from django.http import HttpResponse
from django.template.loader import get_template

monthN = timezone.now().month
yearN = timezone.now().year
todayN = timezone.now().day
dayN = timezone.now().day


choice_i_need = (
    ('mm', 'mm'),
    ('C', 'C'),
    ('Ω', 'Ω'),
    ('mΩ', 'mΩ'),
    ('KΩ', 'KΩ'),
    ('MΩ', 'MΩ'),
    ('A', 'A'),
    ('mA', 'mA'),
    ('µA', 'µA'),
    ('µV', 'µV'),
    ('kgcm3', 'kgcm3'),
    ('V', 'V'),
    ('mV', 'mV'),
    ('Hz', 'Hz'),
    ('KHz', 'Khz'),
    ('µm', 'µm')
)

pressure_unit = (
    ('Pascal', 'Pascal'),
    ('bar', 'bar'),
    ('psi', 'psi'),
    ('kg/cm2', 'kg/cm2'),
    ('mmH2o', 'mmH2o'),
    ('mmHg', 'mmHg'),
    ('inHg', 'inHg'),
    ('mbar', 'mbar'),
    ('mpa', 'mpa'),
    ('kpa', 'kpa'),
    ('inH2o', 'inH2o'),
    ('cmH2o', 'cmH2o'),
    ('hpa', 'hpa'),
)

dimensions_unit = (
    ('mm', 'mm'),
    ('µm', 'µm')
)

weighing_unit = (
    ('g', 'g'),
    ('kg', 'kg'),
    ('mg', 'mg')
)

weight_unit = (
    ('g', 'g'),
    ('kg', 'kg'),
    ('mg', 'mg')
)


type_clarification = (
    ('DC Voltage', 'DC Voltage'),
    ('AC-Voltage', 'AC-Voltage'),
    ('Resistance', 'Resistance'),
    ('DC Current', 'DC Current'),
    ('AC-Current', 'AC-Current'),
    ('Frequency', 'frequency'),
    ('Time', 'Time'),
    ('Power', 'Power'),
    ('Power_Factor', 'Power_Factor'),
    ('Capacitance', 'Capacitance'),
    # ('Weight', 'Weight'),
    # ('Weighing_Balance', 'Weighing_Balance'),

)


@login_required
def newObservation(request, id):
    srfN = SRFItem.objects.get(id=id)
    srfNoN = srfN.job_no
    unt = choice_i_need
   # locN = srfN.srfIt.first().location
    calN = srfNoN + '/' + str(srfN.id)
    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    parameterNN = uucForCalibration.material_type
    accessoriesmaster = AccessoriesMaster.objects.filter(units=parameterNN)
    scope_get = Scope.objects.filter(parameter=parameterNN)


    instruList = uucForCalibration.procedure_master.master_equipment.all()




    check_source_measure = uucForCalibration.source

    if check_source_measure == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "UUC"
        secondry_intru = "Std"

    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp

    data = {'cal_observation_number': calN, 'calibration_performed_at': 'Lab', 'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN}
    form = ObservationForm(initial=data)
    cycles = srfN.instrument.procedure_master.cycles
    chamber = srfN.instrument.chamber_postions



    if cycles:
        pass
    else:
        cycles = 5

    pressD = PressureForm()
    observIt = etItemForm()
    observIti = ThermalItemForm()
    Dimension1 = DimensionForm()
    Weighing1 = WeighingForm()
    Weight1 = WeightForm()
    Volumetric1 = VolumetricForm()
    Thermal1 = ThermalForm()
    electrothermal = ETForm()
    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles
    soaks = SOAKING_REQUIREMENT
    context = {
        'form': form,
        'scope_get':scope_get,
        'pressD': pressD,
        'observIt': observIt,
        'chamber':chamber,
        'idn': id,
        'srfN': srfN,
        'Dimension1': Dimension1,
        'Weighing1': Weighing1,
        'Weight1' : Weight1,
        'Volumetric1': Volumetric1,
        'Thermal1': Thermal1,
        'electrothermal': electrothermal,
        'tempVar': tempVar,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'pressure_unit' :pressure_unit,
        'dimensions_unit':dimensions_unit,
        'check_source_measure' :check_source_measure,
        'weighing_unit' : weighing_unit,
        'weight_unit' : weight_unit,
        'primary_intru' :primary_intru,
        'secondry_intru' : secondry_intru,
        'instruList' :instruList,
        'accessoriesmaster':accessoriesmaster,
        'SOAKING_REQUIREMENT': soaks
    }

    return render(request, "observation/addobservation.html", context)


@login_required
def updateobs(request, id):
    srfN = Observation.objects.get(id=id)
    #print(srfN)
    #print(srfN.uucForCalibration.material_type)
    uucForCalibration = srfN.uucForCalibration
    form = ObservationForm(instance=srfN)
    context = {
        'form': form,
        # 'pressD': pressD,

        'idn': id,
        'srfN': srfN,
        # 'idn': id
    }
    if srfN.uucForCalibration.material_type == 'dialgauge':
        Dimension1 = DimensionForm()
        context = {
            'form': form,
            'pressD': pressD,
            'Dimension1': Dimension1,
            'idn': id,
            'srfN': srfN,
            # 'idn': id
        }
    elif srfN.uucForCalibration.material_type == 'pressuregauge':
        observIt = pressureForm()
        context = {
            'form': form,
            'pressD': pressD,
            'observIt': observIt,
            'idn': id,
            'srfN': srfN,
            # 'idn': id
        }
    elif srfN.uucForCalibration.material_type == 'Thermal':
        observIti = ThermalItemForm()
        context = {
            'form': form,
            'pressD': pressD,
            'observIti': observIti,
            'idn': id,
            'srfN': srfN,
            # 'idn': id
        }
    elif srfN.uucForCalibration.material_type == 'Dimension':
        Dimension1 = DimensionForm()
        #print("Hi")
        context = {
            'form': form,
            'pressD': pressD,
            'Dimension1': Dimension1,
            'idn': id,
            'srfN': srfN,
            'uucForCalibration': uucForCalibration
            # 'idn': id
        }
    elif srfN.uucForCalibration.material_type == 'Weighing_Balance':
        Weighing1 = WeighingForm()
        context = {
            'form': form,
            # 'pressD': pressD,
            'Weighing1': Weighing1,
            'idn': id,
            'srfN': srfN,
            'uucForCalibration': uucForCalibration
            # 'idn': id
        }
    elif srfN.uucForCalibration.material_type == 'Volumertric':
        Volumetric1 = VolumetricForm()
        context = {
            'form': form,
            'pressD': pressD,
            'Volumetric1': Volumetric1,
            'idn': id,
            'srfN': srfN,
            # 'idn': id
        }

    else:
        # elif srfN.uucForCalibration.material_type=='Electro_Techinical':
        electrothermal = ETForm()
        context = {
            'form': form,
            'pressD': pressD,
            'electrothermal': electrothermal,
            'idn': id,
            'srfN': srfN,
            # 'idn': id
        }

    return render(request, "updateobs.html", context)



def approveobs(request, id):
    abc = Observation.objects.get(id=id)
    abc.checked_by = request.user
    abc.save()
    Certificate.objects.create(draft=abc)
    return redirect('home:dashboard')


def prgaugelab(request):
    certi = Certificate.objects.get(id=1)
    context = {
        'certi': certi,
    }
    return render(request, "prgaugelab.html", context)


def pressurecerti(request, id):
    certi = Certificate.objects.get(id=id)
    context = {

        'certi': certi,
    }
    return render(request, "prgaugesite.html", context)


# def prgaugesite(request):
#
#     context={
#
#     }
#     return render(request,"prgaugesite.html",context)


def bevelprotractor(request):
    context = {
    }
    return render(request, "bevelprotractor.html", context)


def burette(request):
    context = {
    }
    return render(request, "burette.html", context)


def dialgauge(request, id):
    certi = Certificate.objects.get(id=id)
    #print("certi--===----", certi)
    context = {
        'certi': certi,
    }
    return render(request, "dialgauge.html", context)


def digitalcaliper(request):
    context = {
    }
    return render(request, "digitalcaliper.html", context)


def digitalmultimeter(request):
    context = {
    }
    return render(request, "digitalmultimeter.html", context)


def digitaltimer(request):
    context = {
    }
    return render(request, "digitaltimer.html", context)


def digitalmicrometer(request):
    context = {
    }
    return render(request, "digitalmicrometer.html", context)


def mappingresults(request):
    context = {
    }
    return render(request, "mappingresults.html", context)


def mapping(request):
    context = {
    }
    return render(request, "mapping.html", context)


def micropipette(request):
    context = {
    }
    return render(request, "micropipette.html", context)


def ppgaugeSGDG(request):
    context = {
    }
    return render(request, "ppgaugeSGDG.html", context)


def ppgauge(request):
    context = {
    }
    return render(request, "ppgauge.html", context)


def poweranalyzer(request):
    context = {
    }
    return render(request, "poweranalyzer.html", context)


def rtw(request):
    context = {
    }
    return render(request, "rtw.html", context)


def stopwatchcalibrator(request):
    context = {
    }
    return render(request, "stopwatchcalibrator.html", context)


def stopwatchmedichem(request):
    context = {
    }
    return render(request, "stopwatchmedichem.html", context)


def testreport(request):
    context = {
    }
    return render(request, "testreport.html", context)


def veeblock(request):
    context = {
    }
    return render(request, "veeblock.html", context)


@login_required
def pushtoobservation(request, id):
    srf = ServiceRequirement.objects.get(id=id)
    srf.status = "Pending"

    srf.save()
    for item in srf.instrument.all():
        srfitem = SRFItem.objects.get(id=item.id)
        observation = Observation.objects.create()
        observation.cal_observation_number = 'PMM/' + str(srfitem.job_no)
        observation.uucForCalibration = srfitem.instrument
        # observation.parent_srf=srf
        observation.parent_srf = srfitem
        # observation.job =
    srf.adderess = str(working.account.billing_address_line) + " " + str(working.account.billing_street) + " " + str(
        working.account.billing_city) + " " + str(working.account.billing_state) + " " + str(
        working.account.billing_postcode) + " " + str(working.account.billing_country)
    srf.status = "New"
    srf.save()
    for item in working.quotation.quotationItem.all():
        for i in range(0, int(item.qty)):
            jb_no = i + 1
            srfitem = SRFItem.objects.create(job_no=jb_no)
            srfitem.instrument.add(item.itemName)
            # #print(srf)
            srf.instrument.add(srfitem)
            srf.save()
    # confirmationmail(request)
    # team = Teams.objects.get(name="Manager")
    # if workingorder.objects.get(company_name=opportunity.name,qoutation_app=True,assigned_to = team,quotation=quotation):
    #     pass
    # else:
    #     working = workingorder.objects.create(company_name=opportunity.name,qoutation_app=True,assigned_to = team,quotation=quotation)
    return redirect('srf:updateSRF', srf.id)


@login_required
def allocationview(request, id):
    working = ServiceRequirement.objects.get(id=id)
    empView = User.objects.all()
    myArr = []

    for item in empView:
        newdDict = {}
        newdDict['first_name'] = item.first_name
        newdDict['last_name'] = item.last_name
        newdDict['id'] = item.id
        newdDict['bool'] = False

        arrayNeed = []
        countT = 0
        for items in item.work_assigned_to.all():
            arrayNeed.append(items)
            newdDict['bool'] = True
            countT += items.wo_item.count()

        newdDict['countH'] = countT
        newdDict['works'] = arrayNeed
        myArr.append(newdDict)

    #print(myArr)
    if request.method == "POST":
        assignee = request.POST.getlist('arrayOI')
        allvalue = request.POST.getlist('arrayOI[]')
        working.assigned_to.clear()
        for item in allvalue:
            kook = User.objects.get(id=int(item))

            working.assigned_to.add(kook)
            working.save()
    context = {
        "working": working,
        'empView': empView,
        'myArr': myArr
    }
    return render(request, "allocation/allocationview.html", context)


@login_required
def allocation(request):
    working = workingorder.objects.filter(location='On Site', assigned_to__isnull=True)
    work = workingorder.objects.filter(location='Lab', assigned_to__isnull=True)

    service = ServiceRequirement.objects.filter(assigned_to=None)
    to_be_deleted = []
    to_be_deleted2 = []
    for items in working:
        try:
            if items.job.srf.is_observed() == False:
                to_be_deleted.append(items.id)
        except:
            pass

    working.filter(id__in=to_be_deleted).delete()

    for item in work:
        try:
            if items.job.srf.is_observed() == False:
                to_be_deleted2.append(items.id)
        except:
            pass

    work.filter(id__in=to_be_deleted2).delete()

    context = {
        'working': working,
        'work': work,
        'service': service,

    }
    return render(request, "allocation/allocation.html", context)


def observationDashboard(request):

    newtest = Observation.objects.all().order_by('-id')
    #print(">>>>>>>>>>>", newtest)
    srfItemN = SRFItem.objects.filter(srfIt__created_on__month=monthN, is_observed=False)
    to_be_deleted = []
    for item in srfItemN:
        if item.srfIt.first().srfno == None:
            to_be_deleted.append(item.id)
    # srfItemN.filter(id__in=to_be_deleted).delete()
    # products = product.objects.all().order_by('-id')[:6]
    srfItemS = SRFItem.objects.filter(is_observed=False).order_by('id')[:6]
    uuc_data = UUCMaster.objects.all().values()
    inst_type = InstrumentType.objects.all()

    # #print("ghgghghg",uuc_data)
    yest = timezone.now().day - 1
    srfYest = SRFItem.objects.filter(srfIt__created_on__day=yest, is_observed=False)
    srfTod = SRFItem.objects.filter(srfIt__created_on__day=dayN, is_observed=False)
    srfTodC = srfTod.count()
    srfYestC = srfYest.count()

    srfItemNC = srfItemN.count()

    context = {
        'srfItemN': srfItemN,
        'srfItemS': srfItemS,
        'srfItemNC': srfItemNC,
        'srfYest': srfYest,
        'srfYestC': srfYestC,
        'srfTod': srfTod,
        'srfTodC': srfTodC,
        'newtest': newtest,
        'uuc_data':uuc_data,
        'inst_type':inst_type
        # 'form': form
    }

    return render(request, 'observation/observationdashboard.html', context)


import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def etUncertainView(request):

    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        lc_duc = request.POST.get('lc_duc')
        lc_duc_unit = request.POST.get('lc_duc_unit')
        lc_duc_unit_parameter = request.POST.get('lc_duc_unit_parameter')
        cal_point = request.POST.get('cal_point')
        cal_point_unit = request.POST.get('cal_point_unit')
        obs_point_unit = request.POST.get('obs_point_unit')
        instru_range = request.POST.get('instru_range')
        instru_range_unit = request.POST.get('instru_range_unit')
        instrument_accessories = request.POST.get('instrument_accessories')
        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')
        scopes = request.POST.get('scopes')
        scope =  Scope.objects.get(id = int(scopes))


        stableity_of_the_source = request.POST.get('stablity_of_source')
        try:
            stableity_of_the_source = stableity_of_the_source
        except:
            stableity_of_the_source = None

        allinstru = request.POST.getlist('arrayIN[]')
        allinstru_list = json.loads(allinstru[0])



        abc = None
        if obs1 != '':
            abc = etItemUncertainty(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit,
                                    obs1, obs2, obs3, obs4, obs5, instru_range, instru_range_unit, allinstru_list, instrument_accessories, stableity_of_the_source, scope)

    #print(abc)
    return HttpResponse(json.dumps(abc))


@csrf_exempt
def etitemsave(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        lc_duc = request.POST.get('lc_duc')
        lc_duc_unit = request.POST.get('lc_duc_unit')
        lc_duc_unit_parameter = request.POST.get('lc_duc_unit_parameter')
        cal_point = request.POST.get('cal_point')
        cal_point_unit = request.POST.get('cal_point_unit')
        obs_point_unit = request.POST.get('obs_point_unit')
        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')

        abc = None
        if obs1 != '':
            abc = etItem(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1, obs2,
                         obs3, obs4, obs5)

    #print(json.dumps(abc))
    return HttpResponse(json.dumps(abc))



# import os
#
# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# from django.conf import settings
# from dashboard.models import *
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML
# from django.templatetags.static import static
# import base64

@csrf_exempt
def etitemtestView(request):
    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        scopes = request.POST.get('scopes')
        scop_obj = Scope.objects.get(id = int(scopes))


        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')
        temp1 = request.POST.get('temp1')
        temp3 = request.POST.get('temp3')
        rh1 = request.POST.get('rh1')
        rh3 = request.POST.get('rh3')
        check_source_measure = request.POST.get('check_source_measure')

        allvalue = request.POST.getlist('arrayOID[]')
        allinstru = request.POST.getlist('arrayIN[]')

        allinstru_list = json.loads(allinstru[0])



        allvalue = json.loads(allvalue[0])


        srfItN = SRFItem.objects.get(id=sfn_id)
        obsIt = Observation.objects.create(parent_srf=srfItN, cal_observation_number=cal_observation_no, calibration_performed_at=id_calibration_performed_at, location=id_calibration_performed_at, calibrated_by=request.user)

        for instrus in allinstru_list:

            if instrus.get('instrument'):
                ids = instrus['instrument']


                abc = instrumentMaster.objects.get(id=ids)
                obsIt.instrument.add(abc)
            obsIt.save()

        obsIt.scope = scop_obj
        obsIt.mode = check_source_measure
        obsIt.uucForCalibration = srfItN.instrument


        etObsIt = etobservation.objects.create(observation=obsIt, calibratedBy=request.user, remarks = remarks)
        etObsIt.temp1 = temp1
        etObsIt.temp3 = temp3
        etObsIt.rh1 = rh1
        etObsIt.rh3 = rh3


        for item in allvalue:

            # fullNo = int(item['itemName'])
            instr = etItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item['sn']

            if item.get('cal_point'):
                #print(item['cal_point'])
                instr.nominal_value = item['cal_point']

            if item.get('value_on'):
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']

            if item.get('nom_1'):
                instr.nom_1 = item['nom_1']
            if item.get('nom_2'):
                instr.nom_2 = item['nom_2']
            if item.get('nom_3'):
                instr.nom_3 = item['nom_3']
            if item.get('nom_4'):
                instr.nom_4 = item['nom_4']
            if item.get('nom_5'):
                instr.nom_5 = item['nom_5']


            if item.get('lead_resistance'):
                instr.lead_resistance = item['lead_resistance']
            if item.get('current_num'):
                instr.current_value = item['current_num']
            if item.get('current_denom'):
                instr.current_ratio = item['current_denom']

            if item.get('lc_duc'):
                instr.least_count = item['lc_duc']
            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']

            if item.get('stablity_of_source'):
                instr.stableity_of_the_source = item['stablity_of_source']


            if item.get('instrument_accessories'):
                try:
                    abc_id = item['instrument_accessories']
                    abc = AccessoriesMaster.objects.get(id=abc_id)
                    instr.accessoriesmaster.add(abc)
                except:
                    pass


            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('instru_range'):
                instr.instru_range = item['instru_range']
            if item.get('instru_range_unit'):
                instr.instru_range_unit = item['instru_range_unit']



            instr.save()
            etObsIt.etItem.add(instr)
            etObsIt.save()

        etObsIt.save()



        myLC = etObsIt.etItem.all().values('least_count').distinct()
        abc = myLC.count()
        lc_val = None
        if abc == 1:
            lc_val = myLC.first()
            lc_val = lc_val['least_count']

        else:
            lc_val = 'Multiple'

        rh1 = etObsIt.rh1
        rh3 = etObsIt.rh3

        if rh1 != None:
            itemNeed = (float(rh1) +  float(rh3))
            itemNeed = round(itemNeed, 2)
            avgRh = itemNeed / 2
        else:
            avgRh = " "


        # context2 = {
        #     'newtest': obsIt,
        #     'newtest2': etObsIt.etItem.all(),
        #     'lc_val': lc_val,
        #     'avgTemp': etObsIt.temp4,
        #     'avgRh': avgRh,
        # }
        #
        # image1 = os.path.join(BASE_DIR, 'static') +'img/quotation/main_logo.png'
        # html_string = render_to_string('observation/test.html', context2)
        #
        #
        #
        # html = HTML(string=html_string, base_url=request.build_absolute_uri())
        # abc1 = static('css/css.css')
        # loc = settings.MEDIA_ROOT
        # n = random.randint(1,9999999999)
        #
        # loc2 = loc + '/observation/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc2,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #
        #
        #
        #
        # m = etObsIt.etItem.all().values('type').distinct()
        # parameters = []
        # for a in m:
        #     parameter = a['type']
        #     parameters.append(parameter)
        #
        #
        #
        #
        # context3 = {
        # 'newtest': obsIt,
        # 'parameters' : parameters,
        # }
        #
        #
        #
        # html_string2 = render_to_string('observation/uncertainitybudgeting.html', context3)
        # html = HTML(string=html_string2, base_url=request.build_absolute_uri())
        # n = random.randint(1,9999999999)
        # loc23 = loc + '/observation/uncertaintybudgeting/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc23,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #
        #
        # calibratedBy = etObsIt.calibratedBy
        # context4 = {
        # 'newtest': obsIt,
        # 'lc_val': lc_val,
        # 'my_parameter_list': parameters,
        # 'etitemslist' : etObsIt.etItem.all(),
        # 'calibratedBy' : calibratedBy.username,
        # }
        #
        #
        # html_string3 = render_to_string('observation/etDraft.html', context4)
        # html = HTML(string=html_string3, base_url=request.build_absolute_uri())
        # n = random.randint(1,9999999999)
        # loc234 = loc + '/observation/draft/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc234,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #
        #
        #
        #
        #
        # obsIt.certificate=loc2
        # obsIt.observation_bugdet=loc23
        # obsIt.observation_details = loc234

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()

        return HttpResponse("done")


        # image1 = os.path.join(BASE_DIR, 'static') + 'img/quotation/main_logo.png'
        # html_string = render_to_string('testmul.html', { })

        # return redirect('observation:moretest', id)
        # pass













@csrf_exempt
def thermalUncertainView(request):

    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        lc_duc = request.POST.get('lc_duc')
        lc_duc_unit = request.POST.get('lc_duc_unit')
        lc_duc_unit_parameter = request.POST.get('lc_duc_unit_parameter')
        cal_point = request.POST.get('cal_point')
        cal_point_unit = request.POST.get('cal_point_unit')
        obs_point_unit = request.POST.get('obs_point_unit')
        instru_range = request.POST.get('instru_range')
        instru_range_unit = request.POST.get('instru_range_unit')
        instrument_accessories = request.POST.get('instrument_accessories')
        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')

        allinstru = request.POST.getlist('arrayIN[]')
        allinstru_list = json.loads(allinstru[0])



        abc = None
        if obs1 != '':
            abc = etItemUncertainty(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit,
                                    obs1, obs2, obs3, obs4, obs5, instru_range, instru_range_unit, allinstru_list, instrument_accessories)

    #print(abc)
    return HttpResponse(json.dumps(abc))


@csrf_exempt
def thermalitemsave(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        lc_duc = request.POST.get('lc_duc')
        lc_duc_unit = request.POST.get('lc_duc_unit')
        lc_duc_unit_parameter = request.POST.get('lc_duc_unit_parameter')
        cal_point = request.POST.get('cal_point')
        cal_point_unit = request.POST.get('cal_point_unit')
        obs_point_unit = request.POST.get('obs_point_unit')
        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')

        abc = None
        if obs1 != '':
            abc = etItem(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1, obs2,
                         obs3, obs4, obs5)

    #print(json.dumps(abc))
    return HttpResponse(json.dumps(abc))



# import os
#
# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# from django.conf import settings
# from dashboard.models import *
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML
# from django.templatetags.static import static
# import base64

@csrf_exempt
def thermalitemtestView(request):
    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')


        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')
        temp1 = request.POST.get('temp1')
        temp3 = request.POST.get('temp3')
        rh1 = request.POST.get('rh1')
        rh3 = request.POST.get('rh3')
        check_source_measure = request.POST.get('check_source_measure')

        allvalue = request.POST.getlist('arrayOID[]')
        allinstru = request.POST.getlist('arrayIN[]')

        allinstru_list = json.loads(allinstru[0])



        allvalue = json.loads(allvalue[0])
        #print(allvalue, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


        srfItN = SRFItem.objects.get(id=sfn_id)
        obsIt = Observation.objects.create(parent_srf=srfItN, cal_observation_number=cal_observation_no, calibration_performed_at=id_calibration_performed_at, location=id_calibration_performed_at, calibrated_by=request.user)

        for instrus in allinstru_list:

            if instrus.get('instrument'):
                ids = instrus['instrument']


                abc = instrumentMaster.objects.get(id=ids)
                obsIt.instrument.add(abc)
            obsIt.save()



        obsIt.mode = check_source_measure
        obsIt.uucForCalibration = srfItN.instrument


        etObsIt = etobservation.objects.create(observation=obsIt, calibratedBy=request.user, remarks = remarks)
        etObsIt.temp1 = temp1
        etObsIt.temp3 = temp3
        etObsIt.rh1 = rh1
        etObsIt.rh3 = rh3


        for item in allvalue:

            # fullNo = int(item['itemName'])
            instr = etItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item['sn']

            if item.get('cal_point'):
                #print(item['cal_point'])
                instr.nominal_value = item['cal_point']

            if item.get('value_on'):
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']

            if item.get('nom_1'):
                instr.nom_1 = item['nom_1']
            if item.get('nom_2'):
                instr.nom_2 = item['nom_2']
            if item.get('nom_3'):
                instr.nom_3 = item['nom_3']
            if item.get('nom_4'):
                instr.nom_4 = item['nom_4']
            if item.get('nom_5'):
                instr.nom_5 = item['nom_5']

            if item.get('lc_duc'):
                instr.least_count = item['lc_duc']
            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']


            if item.get('instrument_accessories'):
                try:
                    abc_id = item['instrument_accessories']
                    abc = AccessoriesMaster.objects.get(id=abc_id)
                    instr.accessoriesmaster.add(abc)
                except:
                    pass


            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('instru_range'):
                instr.instru_range = item['instru_range']
            if item.get('instru_range_unit'):
                instr.instru_range_unit = item['instru_range_unit']



            instr.save()
            etObsIt.etItem.add(instr)
            etObsIt.save()

        etObsIt.save()



        myLC = etObsIt.etItem.all().values('least_count').distinct()
        abc = myLC.count()
        lc_val = None
        if abc == 1:
            lc_val = myLC.first()
            lc_val = lc_val['least_count']

        else:
            lc_val = 'Multiple'

        rh1 = etObsIt.rh1
        rh3 = etObsIt.rh3

        if rh1 != None:
            itemNeed = (float(rh1) +  float(rh3))
            itemNeed = round(itemNeed, 2)
            avgRh = itemNeed / 2
        else:
            avgRh = " "


        # context2 = {
        #     'newtest': obsIt,
        #     'newtest2': etObsIt.etItem.all(),
        #     'lc_val': lc_val,
        #     'avgTemp': etObsIt.temp4,
        #     'avgRh': avgRh,
        # }
        #
        # image1 = os.path.join(BASE_DIR, 'static') +'img/quotation/main_logo.png'
        # html_string = render_to_string('observation/test.html', context2)
        #
        #
        #
        # html = HTML(string=html_string, base_url=request.build_absolute_uri())
        # abc1 = static('css/css.css')
        # loc = settings.MEDIA_ROOT
        # n = random.randint(1,9999999999)
        #
        # loc2 = loc + '/observation/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc2,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #
        #
        #
        #
        # m = etObsIt.etItem.all().values('type').distinct()
        # parameters = []
        # for a in m:
        #     parameter = a['type']
        #     parameters.append(parameter)
        #
        #
        #
        #
        # context3 = {
        # 'newtest': obsIt,
        # 'parameters' : parameters,
        # }
        #
        #
        #
        # html_string2 = render_to_string('observation/uncertainitybudgeting.html', context3)
        # html = HTML(string=html_string2, base_url=request.build_absolute_uri())
        # n = random.randint(1,9999999999)
        # loc23 = loc + '/observation/uncertaintybudgeting/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc23,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #
        #
        # calibratedBy = etObsIt.calibratedBy
        # context4 = {
        # 'newtest': obsIt,
        # 'lc_val': lc_val,
        # 'my_parameter_list': parameters,
        # 'etitemslist' : etObsIt.etItem.all(),
        # 'calibratedBy' : calibratedBy.username,
        # }
        #
        #
        # html_string3 = render_to_string('observation/etDraft.html', context4)
        # html = HTML(string=html_string3, base_url=request.build_absolute_uri())
        # n = random.randint(1,9999999999)
        # loc234 = loc + '/observation/draft/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc234,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #
        #
        #
        #
        #
        # obsIt.certificate=loc2
        # obsIt.observation_bugdet=loc23
        # obsIt.observation_details = loc234

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()

        return render(request, 'observation/test.html')


        # image1 = os.path.join(BASE_DIR, 'static') + 'img/quotation/main_logo.png'
        # html_string = render_to_string('testmul.html', { })

        # return redirect('observation:moretest', id)
        # pass






# import random
# @csrf_exempt
#
# @csrf_exempt
# def moretest(request,id):
#     newtest = Observation.objects.get(id=id)
#     newtest2 = etItem.objects.all()
#     # new_val = etobservation.objects.filter(observation=newtest).temp4.values()
#     avgTemp = newtest.et_observation.first().temp4
#
#     rh1 = newtest.et_observation.first().rh1
#     rh2 = newtest.et_observation.first().rh2
#     rh3 = newtest.et_observation.first().rh3
#
#     if rh1 != None:
#         itemNeed = (float(rh1) + float(rh2) + float(rh3))
#         itemNeed = round(itemNeed, 2)
#         avgRh = itemNeed / 3
#     else:
#         avgRh = " "
#
#     myLC = newtest.et_observation.first().etItem.all().values('least_count').distinct()
#     abc = myLC.count()
#     lc_val = None
#     if abc == 1:
#         lc_val = myLC.first()
#         lc_val = lc_val['least_count']
#
#     else:
#         lc_val = 'Multiple'
#     #print("Hello ",myLC)
#
#
#
#     context = {
#         'newtest':newtest,
#         'newtest2': newtest2,
#         'lc_val': lc_val,
#         'avgTemp' : avgTemp,
#         'avgRh' : avgRh,
#     }
#
#     return render(request, 'observation/test.html', context)

def uncertinitybudgeting(request, id):
    newtest = Observation.objects.get(id=id)
    newtest2 = etItem.objects.all()

    m = newtest.et_observation.first().etItem.all().values('type').distinct()
    parameters = []
    for a in m:
        parameter = a['type']
        parameters.append(parameter)


    #print(parameters)


    context = {
        'newtest': newtest,
        'parameters' : parameters,


    }

    return render(request, 'observation/uncertainitybudgeting.html', context)


def digitalmultimeter_certificate(request, id):
    newtest = Observation.objects.get(id=id)

    myLC = newtest.et_observation.first().etItem.all().values('least_count').distinct()


    abc = myLC.count()
    lc_val = None
    if abc == 1:
        lc_val = myLC.first()
        lc_val = lc_val['least_count']

    else:
        lc_val = 'Multiple'

    r = newtest.et_observation.first().etItem.all().values()
    etitemslist = newtest.et_observation.first().etItem.all()

    m= newtest.et_observation.first().etItem.all().values('type').distinct()

    calibratedBy = newtest.et_observation.first().calibratedBy


    my_parameter_list = []
    for a in m:
        parameter = a['type']
        my_parameter_list.append(parameter)




    context = {
        'newtest': newtest,
        'lc_val': lc_val,
        'my_parameter_list': my_parameter_list,
        'etitemslist' : etitemslist,
        'calibratedBy' : calibratedBy.username,

    }
    # return render(request, 'observation/digitalmultimeter.html', context)
    return render(request, 'observation/testmul.html', context)


@csrf_exempt
def pressureView(request):
    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        calibration_performed_at = request.POST.get('calibration_performed_at')
        least_count = request.POST.get('least_count')
        diff = request.POST.get('diff')
        middle_temp = request.POST.get('middle_temp')
        scopes = request.POST.get('scopes')
        calibration_location = request.POST.get('calibration_location')
        scop_obj = Scope.objects.get(id=int(scopes))


        id_starting_humadity=request.POST.get('id_starting_humadity')
        id_middle_humadity =request.POST.get('id_middle_humadity')
        id_ending_humadity= request.POST.get('id_ending_humadity')


        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        starting_temp = request.POST.get('start_temp')
        ending_temp = request.POST.get('end_temp')
        duc_id = request.POST.get('duc_id')

        button_clicked = request.POST.get('button_clicked')
        check_source_measure = request.POST.get('check_source_measure')


        allvalue = request.POST.getlist('arrayOID[]')
        allinstru = request.POST.getlist('arrayIN[]')
        allinstru_list = json.loads(allinstru[0])


        allvalue = json.loads(allvalue[0])


        srfItN = SRFItem.objects.get(id=sfn_id)

        obsIt = Observation.objects.create( cal_observation_number=cal_observation_no, calibration_performed_at= calibration_location, location=calibration_performed_at, calibrated_by=request.user)
        for instrus in allinstru_list:
            if instrus.get('instrument'):
                ids = instrus['instrument']
                abc = instrumentMaster.objects.get(id=ids)
                obsIt.instrument.add(abc)
            obsIt.save()

        obsIt.scope = scop_obj
        obsIt.mode = check_source_measure
        obsIt.uucForCalibration = srfItN.instrument
        obsIt.parent_srf=srfItN
        #print(obsIt)

        prObsIt = Pressure.objects.create(observation=obsIt, calibratedBy=request.user, remarks=remarks,ending_temp=ending_temp,starting_temp=starting_temp, least_count=least_count)
        prObsIt.rh1 = id_starting_humadity
        prObsIt.rh2 = id_middle_humadity
        prObsIt.rh3 = id_ending_humadity
        prObsIt.temp2 = middle_temp
        uucForCalibration=str(srfItN.instrument)

        for item in allvalue:

            instr = pressureItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item['sn']

            instr.startingTemp= starting_temp
            instr.endingTemp = ending_temp
            instr.duc_id = duc_id
            instr.zero_deviation = diff
            instr.middle_temp = middle_temp

            if item.get('uuc'):
                instr.nominal_value = item['uuc']

            if item.get('x1'):
                instr.observation1 = item['x1']
            if item.get('x2'):
                instr.observation2 = item['x2']
            if item.get('x3'):
                instr.observation3 = item['x3']
            if item.get('x4'):
                instr.observation4 = item['x4']
            if item.get('x5'):
                instr.observation5 = item['x5']
            if item.get('x6'):
                instr.observation6 = item['x6']

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']

            instr.least_count = least_count


            instr.save()
            prObsIt.pressure_item.add(instr)
            prObsIt.save()

        prObsIt.save()
        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False
        obsIt.save()


        # context3 = {
        # 'newtest': obsIt,
        # 'uucForCalibration' : uucForCalibration,
        # }


        # loc = settings.MEDIA_ROOT
        # html_string2 = render_to_string('observation/pressuregauge.html', context3)
        # html = HTML(string=html_string2, base_url=request.build_absolute_uri())
        # n = random.randint(1,9999999999)
        # loc2 = loc + '/observation/draft/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc2,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);


        # m = etObsIt.etItem.all().values('type').distinct()
        # parameters = []
        # for a in m:
        #     parameter = a['type']
        #     parameters.append(parameter)




        # context1 = {
        # 'newtest': obsIt,
        # # 'parameters' : parameters,
        # }



        # html_string2 = render_to_string('observation/pguncertanitybudgeting.html', context1)
        # html = HTML(string=html_string2, base_url=request.build_absolute_uri())
        # n = random.randint(1,9999999999)
        # loc23 = loc + '/observation/uncertaintybudgeting/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc23,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #

        # calibratedBy = prObsIt.calibratedBy
        # context4 = {
        # 'newtest': obsIt,
        # # 'lc_val': lc_val,
        # # 'my_parameter_list': parameters,
        # 'etitemslist' : prObsIt.pressure_item.all(),
        # 'calibratedBy' : calibratedBy.username,
        # }

        #
        # html_string3 = render_to_string('observation/pressureguagelab.html', context4)
        # html = HTML(string=html_string3, base_url=request.build_absolute_uri())
        # n = random.randint(1,9999999999)
        # loc234 = loc + '/observation/draft/' + str(n)  + '.pdf'
        # html.write_pdf(target=loc234,stylesheets=['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700', 'http://127.0.0.1:8000/static/css/css.css']);
        #
        #



        # obsIt.observation_details = loc2
        #
        # obsIt.observation_bugdet = loc23
        # obsIt.certificate = loc234
        # obsIt.save()





        # image1 = os.path.join(BASE_DIR, 'static') + 'img/quotation/main_logo.png'
        # html_string = render_to_string('testmul.html', { })


        return HttpResponse("done")


@csrf_exempt
def pressureMultiView(request):
    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        calibration_performed_at = request.POST.get('calibration_performed_at')
        middle_temp = request.POST.get('middle_temp')
        scopes = request.POST.get('scopes')
        calibration_location = request.POST.get('calibration_location')
        #scop_obj = Scope.objects.get(id=int(scopes))


        id_starting_humadity=request.POST.get('id_starting_humadity')
        id_middle_humadity =request.POST.get('id_middle_humadity')
        id_ending_humadity= request.POST.get('id_ending_humadity')


        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        starting_temp = request.POST.get('start_temp')
        ending_temp = request.POST.get('end_temp')
        duc_id = request.POST.get('duc_id')

        button_clicked = request.POST.get('button_clicked')
        check_source_measure = request.POST.get('check_source_measure')


        allvalue = request.POST.getlist('arrayOID[]')



        allvalue = json.loads(allvalue[0])


        srfItN = SRFItem.objects.get(id=sfn_id)

        obsIt = Observation.objects.create( cal_observation_number=cal_observation_no, calibration_performed_at= calibration_location, location=calibration_performed_at, calibrated_by=request.user)


        obsIt.mode = check_source_measure
        obsIt.uucForCalibration = srfItN.instrument
        obsIt.parent_srf=srfItN

        prObsIt = PressureMulti.objects.create(observation=obsIt, calibratedBy=request.user, remarks=remarks,ending_temp=ending_temp,starting_temp=starting_temp)
        prObsIt.rh1 = id_starting_humadity
        prObsIt.rh2 = id_middle_humadity
        prObsIt.rh3 = id_ending_humadity
        prObsIt.temp2 = middle_temp
        uucForCalibration=str(srfItN.instrument)

        for item in allvalue:

            instr = pressuremultiItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item['sn']

            instr.startingTemp= starting_temp
            instr.endingTemp = ending_temp
            instr.duc_id = duc_id
            instr.middle_temp = middle_temp

            if item.get('diff'):
                instr.zero_deviation = item['diff']

            if item.get('scopes'):
                instr.scope = Scope.objects.get(id=int(item['scopes']))

            if item.get('uuc'):
                instr.nominal_value = item['uuc']

            if item.get('x1'):
                instr.observation1 = item['x1']
            if item.get('x2'):
                instr.observation2 = item['x2']
            if item.get('x3'):
                instr.observation3 = item['x3']
            if item.get('x4'):
                instr.observation4 = item['x4']
            if item.get('x5'):
                instr.observation5 = item['x5']
            if item.get('x6'):
                instr.observation6 = item['x6']

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']

            if item.get('least_count'):
                instr.least_count = item['least_count']

            if item.get('arrayInstru'):
                for i in item['arrayInstru']:
                    ids = i['instrument']
                    abc = instrumentMaster.objects.get(id=ids)
                    instr.m_instrument.add(abc)




            instr.save()
            prObsIt.pressure_item.add(instr)
            prObsIt.save()

        prObsIt.save()
        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False
        obsIt.save()







def presureuncertaintest(request, id):
    pres_inst = pressureItem.objects.get(id=id)


    #print(pres_inst, "ahsadfhsadbfjsdh")




@csrf_exempt
def PrUncertainView(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        least_count = request.POST.get('least_count')
        cal_point = request.POST.get('cal_point')

        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')
        obs6 = request.POST.get('obs6')
        diff = request.POST.get('diff')
        temp_var = request.POST.get('temp_var')
        scopes = request.POST.get('scopes')
        calibration_location = request.POST.get('calibration_location')

        allinstru = request.POST.getlist('arrayIN[]')
        allinstru_list = json.loads(allinstru[0])

        nomUnit = request.POST.get('nomUnit')
        obsUnit = request.POST.get('obsUnit')
        scope = Scope.objects.get(id=int(scopes))


        abc = None
        if obs1 != '':
            abc = pr_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit, diff, allinstru_list, temp_var, scope, calibration_location)

    #print(json.dumps(abc))
    return HttpResponse(json.dumps(abc))



@csrf_exempt
def PrMultiUncertainView(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        least_count = request.POST.get('least_count')
        cal_point = request.POST.get('cal_point')

        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')
        obs6 = request.POST.get('obs6')
        diff = request.POST.get('diff')
        temp_var = request.POST.get('temp_var')
        scopes = request.POST.get('scopes')
        calibration_location = request.POST.get('calibration_location')

        allinstru = request.POST.getlist('arrayIN[]')
        allinstru_list = json.loads(allinstru[0])

        nomUnit = request.POST.get('nomUnit')
        obsUnit = request.POST.get('obsUnit')
        scope = Scope.objects.get(id=int(scopes))


        abc = None
        if obs1 != '':
            abc = prMulti_ItemUncertainty(duc_id, obs1, obs2, obs3, obs4, obs5, obs6, cal_point, least_count, nomUnit, obsUnit, diff, allinstru_list, temp_var, scope, calibration_location)

    #print(json.dumps(abc))
    return HttpResponse(json.dumps(abc))

@csrf_exempt
def dimUncertainView(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        lc_duc = request.POST.get('lc_duc')
        rangeP =  request.POST.get('range')
        lc_duc_unit = request.POST.get('lc_duc_unit')
        lc_duc_unit_parameter = request.POST.get('lc_duc_unit_parameter')
        cal_point = request.POST.get('cal_point')
        cal_point_unit = request.POST.get('cal_point_unit')
        obs_point_unit = request.POST.get('obs_point_unit')
        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')
        tempP = request.POST.get('tempP')
        nomUnit = request.POST.get('nomUnit')
        obsUnit = request.POST.get('obsUnit')

        #print(nomUnit)
        #print(obsUnit)

        # temp = request.POST.get('temp')
        temp1 = request.POST.get('temp1')

        starting_temp = request.POST.get('starting_temp')
        ending_temp = request.POST.get('ending_temp')

        least_count = request.POST.get('least_count')

        temp = float(ending_temp)-float(starting_temp)



        abc = None
        if obs1 != '':
            abc = dimItemUncertainty(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit,
                                    obs1, obs2, obs3, obs4, obs5,rangeP, tempP,least_count, temp, nomUnit, obsUnit)

    return HttpResponse(json.dumps(abc))






@csrf_exempt
def dimitemsave(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        lc_duc = request.POST.get('lc_duc')
        rangeP =  request.POST.get('range')
        lc_duc_unit = request.POST.get('lc_duc_unit')
        lc_duc_unit_parameter = request.POST.get('lc_duc_unit_parameter')
        cal_point = request.POST.get('cal_point')
        cal_point_unit = request.POST.get('cal_point_unit')
        obs_point_unit = request.POST.get('obs_point_unit')
        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')
        tempP = request.POST.get('tempP')
        least_count = request.POST.get('least_count')

        abc = None
        if obs1 != '':
            abc = etItem(duc_id, lc_duc, lc_duc_unit_parameter, cal_point, cal_point_unit, obs_point_unit, obs1, obs2,
                         obs3, obs4, obs5,rangeP, tempP,least_count)

    #print(json.dumps(abc))
    return HttpResponse(json.dumps(abc))


@csrf_exempt
def dimitemtestView(request):
    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')

        start_temp = request.POST.get('start_temp')
        end_temp = request.POST.get('end_temp')
        check_source_measure = request.POST.get('check_source_measure')
        least_count = request.POST.get('least_count')


        ref_temp = request.POST.get('ref_temp')

        allvalue = request.POST.getlist('arrayOID[]')
        allvalue = json.loads(allvalue[0])

        srfItN = SRFItem.objects.get(id=sfn_id)
        obsIt = Observation.objects.create(parent_srf=srfItN, cal_observation_number=cal_observation_no)
        obsIt.mode = check_source_measure
        obsIt.uucForCalibration = srfItN.instrument





        etObsIt = dimobservation.objects.create(observation=obsIt, calibratedBy=request.user, remarks = remarks,temp1=start_temp,temp3=end_temp, temp2=ref_temp)


        for item in allvalue:

            instr = dimItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item['sn']

            instr.least_count = least_count

            if item.get('cal_point'):
                instr.nominal_value = item['cal_point']

            if item.get('value_on'):
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']




            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']
            if item.get('rangeP'):
                instr.type = item['rangeP']

            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']


            if item.get('method'):
                instr.method = item['method']

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']

            instr.save()
            etObsIt.dimItem.add(instr)
            etObsIt.save()

        etObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()




        return redirect('observation:observationDashboard')






@csrf_exempt
def weightUncertainView(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        mass = request.POST.get('mass')
        least_count = request.POST.get('least_count')
        nomUnit = request.POST.get('nomUnit')
        obsUnit = request.POST.get('obsUnit')
        cal_point = request.POST.get('cal_point')
        vt = request.POST.get('vt')
        vr = request.POST.get('vr')
        x1 = request.POST.get('x1')
        x2 = request.POST.get('x2')
        x3 = request.POST.get('x3')
        x4 = request.POST.get('x4')
        x5 = request.POST.get('x5')
        lc_duc = mass
        scopes = request.POST.get('scopes')
        allinstru = request.POST.getlist('arrayIN[]')
        allinstru_list = json.loads(allinstru[0])
        scope = Scope.objects.get(id=int(scopes))

        allcertitem = request.POST.getlist('arrayCIT[]')
        allcertitem = json.loads(allcertitem[0])
        #print(f'-------------------------------------------------------- {allinstru_list}')
        abc = None
        if x1 != '':
            abc = WeightItemUncertainty(duc_id,cal_point,lc_duc, x1, x2, x3, x4, x5, nomUnit, obsUnit, allinstru_list, least_count, vt, vr, allcertitem, scope)


    #print(json.dumps(abc))
    return HttpResponse(json.dumps(abc))







weight_unit_conversion = {
    "g": {"mg":1000, "g":1, "kg":0.001},
    "mg": {"mg":1, "g":1000, "kg":1000000},
    "kg": {"mg":0.000001, "g":0.001, "kg":1}
}
@csrf_exempt
def weightcertificatemassvalue(request):
    if request.method == "POST":
        nomValue = request.POST.get('nom_val')
        nomUnit = request.POST.get('nomUnit')
        obsUnit = request.POST.get('obsUnit')
        vt = request.POST.get('vt')
        vr = request.POST.get('vr')
        va = request.POST.get('va')
        vo = request.POST.get('vo')
        num = float(va)-float(vo)
        dnom = (1/float(vt))-(1/float(vr))
        air_buoyancy = num*dnom

        allcertu = request.POST.getlist('arrayIN[]')
        allcertu_list = json.loads(allcertu[0])

        weight_cert_item = []
        mass_value_list = []
        try:
            for mx in allcertu_list:
                c = mx['certitem']
                weight_cert_item.append(c)
        except:
            weight_cert_item = allcertu_list

        #print(weight_cert_item, "sss")


        consolidated_mass_value = 0
        for x in weight_cert_item:
            certItm = WeightCertificate.objects.get(id=int(x))
            mass_valueN = certItm.mass_value
            mass_value_unit= certItm.mass_value_unit
            unit_converter = weight_unit_conversion[mass_value_unit][obsUnit]
            #print(unit_converter, mass_value_unit, nomUnit)
            mass_valueNN = float(mass_valueN)*unit_converter

            consolidated_mass_value = consolidated_mass_value + mass_valueNN

        mass_value = consolidated_mass_value

        #print(mass_value, "kkkkkk")



        weightlist = {}


        valunN = mass_value*(1+air_buoyancy)

        weightlist['valunN']=valunN

    #print(json.dumps(weightlist))
    return HttpResponse(json.dumps(weightlist))

@csrf_exempt
def weightitemtestView(request):
    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        button_clicked = request.POST.get('button_clicked')
        scopes = request.POST.get('scopes')
        scop_obj = Scope.objects.get(id=int(scopes))


        lc_duc = request.POST.get('lc_duc')
        duc_id = request.POST.get('duc_id')
        check_source_measure = request.POST.get('check_source_measure')

        allvalue = request.POST.getlist('arrayOID[]')
        allvalue = json.loads(allvalue[0])
        instru_array = request.POST.getlist('arrayIN[]')
        instru_list = json.loads(instru_array[0])



        srfItN = SRFItem.objects.get(id=sfn_id)
        obsIt = Observation.objects.create(parent_srf=srfItN, cal_observation_number=cal_observation_no)
        obsIt.mode = check_source_measure
        obsIt.uucForCalibration = srfItN.instrument
        for instrus in instru_list:
            if instrus.get('instrument'):
                ids = instrus['instrument']
                abc = instrumentMaster.objects.get(id=ids)
                obsIt.instrument.add(abc)
            obsIt.save()
        obsIt.scope = scop_obj

        weightObsIt = weightobservation.objects.create(observation=obsIt, calibratedBy=request.user, lc_duc=lc_duc)

        for item in allvalue:

            instr = MassItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))


            if item.get('x1'):
                instr.obs1 = item['x1']
            if item.get('x2'):
                instr.obs2 = item['x2']
            if item.get('x3'):
                instr.obs3 = item['x3']
            if item.get('x4'):
                instr.obs4 = item['x4']
            if item.get('x5'):
                instr.obs5 = item['x5']

            if item.get('x11'):
                instr.obs11 = item['x11']
            if item.get('x12'):
                instr.obs12 = item['x12']
            if item.get('x13'):
                instr.obs13 = item['x13']
            if item.get('x14'):
                instr.obs14 = item['x14']
            if item.get('x15'):
                instr.obs15 = item['x15']


            if item.get('x21'):
                instr.obs21 = item['x21']
            if item.get('x22'):
                instr.obs22 = item['x22']
            if item.get('x23'):
                instr.obs23 = item['x23']
            if item.get('x24'):
                instr.obs24 = item['x24']
            if item.get('x25'):
                instr.obs25 = item['x25']


            if item.get('x31'):
                instr.obs31 = item['x31']
            if item.get('x32'):
                instr.obs32 = item['x32']
            if item.get('x33'):
                instr.obs33 = item['x33']
            if item.get('x34'):
                instr.obs34 = item['x34']
            if item.get('x35'):
                instr.obs35 = item['x35']


            if item.get('x41'):
                instr.obs41 = item['x41']
            if item.get('x42'):
                instr.obs42 = item['x42']
            if item.get('x43'):
                instr.obs43 = item['x43']
            if item.get('x44'):
                instr.obs44 = item['x44']
            if item.get('x45'):
                instr.obs45 = item['x45']

            if item.get('vt'):
                instr.vt = item['vt']
            if item.get('vr'):
                instr.vr = item['vr']
            if item.get('va'):
                instr.va = item['va']
            if item.get('vo'):
                instr.vo = item['vo']

            if item.get('least_count'):
                instr.least_count = item['least_count']

            if item.get('arraycert'):
                try:
                    for i in item['arraycert']:
                        ids = int(i)
                        cert_obj = WeightCertificate.objects.get(id=ids)
                        instr.master_weight_item.add(cert_obj)

                except:
                    pass



            if item.get('range'):
                instr.nominal_value = item['range']
            if item.get('mass'):
                instr.mass_value = item['mass']

            instr.duc_id = duc_id


            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']
            if item.get('nom_val'):
                instr.nominal_value = item['nom_val']


            instr.save()
            weightObsIt.mass_item.add(instr)
            weightObsIt.save()

        weightObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False



        obsIt.save()

        return redirect('observation:observationDashboard')


def instrumentfolder(request,material_type):
    #print("url test", material_type)
    uuc_id = UUCMaster.objects.filter(material_type=material_type)
    obs = Observation.objects.all().filter(submit=True)
    #print(">>>>>>>>>>:::", obs)
    # obs = Observation.objects.all()
    srf = SRFItem.objects.all().count()
    pending_obs= SRFItem.objects.filter(is_observed=True).count()

    observationN = Observation.objects.filter(uucForCalibration__material_type=material_type)
    #print(observationN,"1222222222222222222222222222222222222222222222222222")
    # #print("uuc data ", SRFItem.objects.filter(UUCMaster.objects.get(instrument_name="Calibrator"))
    srfitem = []

    srfitem = SRFItem.objects.filter(instrument__material_type=material_type,obs_service__isnull=True )
    #print(srfitem)
    # for item in srfitem:
    #     if srfitem.parent_srf.first() is None:
    #         sr
    # for item in uuc_id:
    #      #print("sfsfedafskldsgkhldsgshlk",item)
    #      data = SRFItem.objects.filter(instrument=item)
    #      srfitem.append(data)



    #     # data = SRFItem.objects.filter(instrument=UUCMaster.objects.get(instrument_nameitem))
         # srfitem.append(SRFItem.objects.filter(data=uuc_id))
    #
    # #print("test all id", srfitem)
    # #print(obs_data,"data inside data")

    context = {
        "srfitem":srfitem,
        'srf':srf,
        'observationN':observationN
        # 'obs':obs



    }

    return render(request, 'observation/startobservation.html', context)

def technicaldashboard(request):
    certi = Observation.objects.all()
    correct_obs = Observation.objects.filter(submit=True, approved=False)
    total_cert = Observation.objects.filter(submit=True).count()
    today_cert = Observation.objects.filter(submit=True, calibrated_on__month=monthN).count()
    recject_cert = Observation.objects.filter(rejected=True).count()
    context={
        "correct_obs":correct_obs,
        'total_cert':total_cert,
        'recject_cert':recject_cert,
        'today_cert':today_cert,
        'certi':certi

    }
    return render(request, 'observation/technicaldashboard.html', context)


def updateet(request):
    srfN = SRFItem.objects.all()
    # ref_standardN = srfN.instrument.procedure_master.ref_standard
    electrothermal = ETForm()

    context={
    'electrothermal':electrothermal

    }
    return render(request, 'cert_obs/update_et.html', context)


def rejected(request, id):
    obs= Observation.objects.get(id= id)
    obs.rejected = True
    obs.rejected_by = request.user
    obs.save()
    redirect('observation:observationDashboard')


def approved(request, id):
    obs= Observation.objects.get(id= id)
    obs.approved = True

    obs.save()
    redirect('observation:certificate-Dashboard')

    # context={
    # 'obs':obs
    #
    # }
    # return render(request, 'cert_obs/update_et.html', context)


def updateObservation(request, id):
    ordered_obser = Observation.objects.get(id=id)


    if ordered_obser.uucForCalibration.material_type == 'Electro_Technical':
        return redirect('observation:updateET', id)

    elif ordered_obser.uucForCalibration.material_type == 'Dimension':
        return redirect('observation:updatedim', id)
    elif ordered_obser.uucForCalibration.material_type == 'Pressure':
        return redirect('observation:updatepre', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weighing_Balance':
        return redirect('observation:updateWB', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weight':
        return redirect('observation:updateweight', id)
    elif ordered_obser.uucForCalibration.material_type == 'Thermal':
        return redirect('observation:updateThermal', id)



    else:
        return redirect('observation:observationDashboard')




def viewobservation(request, id):
    ordered_obser = Observation.objects.get(id=id)





    if ordered_obser.uucForCalibration.material_type == 'Electro_Technical':
        return redirect('observation:viewET', id)

    elif ordered_obser.uucForCalibration.material_type == 'Dimension':
        return redirect('observation:viewDIM', id)
    elif ordered_obser.uucForCalibration.material_type == 'Pressure':
        return redirect('observation:viewPr', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weighing_Balance':
        return redirect('observation:viewWB', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weight':
        return redirect('observation:viewWeight', id)

    else:
        return redirect('observation:observationDashboard')




weighing_unit = (
    ('g', 'g'),
    ('kg', 'kg'),
    ('mg', 'mg')
)

def viewWeight(request, id):
    ordered_obser = Observation.objects.get(id=id)

    newtest=ordered_obser
    srf_id = ordered_obser.parent_srf.id

    srfN = SRFItem.objects.get(id=srf_id)
    srfNoN = srfN.srfIt.first().srfno

    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)


    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)

    m = weightobservation.objects.filter(observation=ordered_obser).first()
    weight_item = m.mass_item.all()

    idR = m.id

    dataR = weightobservation.objects.get(id=idR)
    anyItem = dataR.mass_item.first()
    vt = anyItem.vt
    vr = anyItem.vr
    vo = anyItem.vo
    va = anyItem.va

    mass_item = dataR.mass_item.values()


    mass_itemNN = mass_item[0]
    massValN =mass_itemNN['mass_value']

    mass_item_obsunit = mass_itemNN['obsUnit']
    mass_item_nomunit = mass_itemNN['nominal_value']

    form1 = WeightForm(instance=dataR)



    context = {
        'ordered_obser': ordered_obser,
        'form': form,
        'uucForCalibration': uucForCalibration,
        'dataR':dataR,
        'massValN':massValN,
        'form1':form1,
        'weight_unit':weight_unit,
        'primary_intru':primary_intru,
        'secondry_intru':secondry_intru,
        'mass_item_nomunit':mass_item_nomunit,
        'mass_item_obsunit':mass_item_obsunit,
        'weight_item':weight_item,
        'vt': vt,
        'vr': vr,
        'va': va,
        'vo': vo,
        'weighing_unit':weight_unit



    }

    return render(request, "view_obs/viewobservation.html", context)



weight_unit = (
    ('g', 'g'),
    ('kg', 'kg'),
    ('mg', 'mg')
)

weighing_unit = (
    ('g', 'g'),
    ('kg', 'kg'),
    ('mg', 'mg')
)


def updateweight(request, id):
    ordered_obser = Observation.objects.get(id=id)

    newtest = ordered_obser
    srf_id = ordered_obser.parent_srf.id
    srfN = SRFItem.objects.get(id=srf_id)
    srfNoN = srfN.srfIt.first().srfno

    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)

    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)

    m = weightobservation.objects.filter(observation=ordered_obser).first()
    weight_item = m.mass_item.all()

    idR = m.id

    dataR = weightobservation.objects.get(id=idR)
    anyItem = dataR.mass_item.first()
    print(anyItem, "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
    vt = anyItem.vt
    vr = anyItem.vr
    vo = anyItem.vo
    va = anyItem.va

    mass_item = dataR.mass_item.values()

    mass_itemNN = mass_item[0]
    massValN = mass_itemNN['mass_value']

    mass_item_obsunit = mass_itemNN['obsUnit']
    mass_item_nomunit = mass_itemNN['nominal_value']

    form1 = WeightForm(instance=dataR)

    if request.method == "POST":

        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        button_clicked = request.POST.get('button_clicked')
        vt = request.POST.get('vt')
        vr = request.POST.get('vr')
        va = request.POST.get('va')
        vo = request.POST.get('vo')

        lc_duc = request.POST.get('lc_duc')
        duc_id = request.POST.get('duc_id')

        allvalue = request.POST.getlist('arrayOID[]')
        allvalue = json.loads(allvalue[0])
        print(allvalue, 'ye hai asli cheejjjjjjjjjjjjjjjjjjjjjjj')

        instru_array = request.POST.getlist('arrayIN[]')

        instru_list = json.loads(instru_array[0])

        srfItN = SRFItem.objects.get(id=sfn_id)
        obsIt = ordered_obser

        weightObsIt = weightobservation.objects.filter(observation=ordered_obser).first()
        obsIt.weight_observation.first().mass_item.all().delete()

        for item in allvalue:
            instr = MassItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            if item.get('x1'):
                instr.obs1 = item['x1']
            if item.get('x2'):
                instr.obs2 = item['x2']
            if item.get('x3'):
                instr.obs3 = item['x3']
            if item.get('x4'):
                instr.obs4 = item['x4']
            if item.get('x5'):
                instr.obs5 = item['x5']

            if item.get('x11'):
                instr.obs11 = item['x11']
            if item.get('x12'):
                instr.obs12 = item['x12']
            if item.get('x13'):
                instr.obs13 = item['x13']
            if item.get('x14'):
                instr.obs14 = item['x14']
            if item.get('x15'):
                instr.obs15 = item['x15']

            if item.get('x21'):
                instr.obs21 = item['x21']
            if item.get('x22'):
                instr.obs22 = item['x22']
            if item.get('x23'):
                instr.obs23 = item['x23']
            if item.get('x24'):
                instr.obs24 = item['x24']
            if item.get('x25'):
                instr.obs25 = item['x25']

            if item.get('x31'):
                instr.obs31 = item['x31']
            if item.get('x32'):
                instr.obs32 = item['x32']
            if item.get('x33'):
                instr.obs33 = item['x33']
            if item.get('x34'):
                instr.obs34 = item['x34']
            if item.get('x35'):
                instr.obs35 = item['x35']

            if item.get('x41'):
                instr.obs41 = item['x41']
            if item.get('x42'):
                instr.obs42 = item['x42']
            if item.get('x43'):
                instr.obs43 = item['x43']
            if item.get('x44'):
                instr.obs44 = item['x44']
            if item.get('x45'):
                instr.obs45 = item['x45']

            if item.get('least_count'):
                instr.least_count = item['least_count']

            if item.get('arraycert'):
                try:
                    for i in item['arraycert']:
                        ids = int(i['instrument'])
                        cert_obj = WeightCertificate.objects.get(id=ids)
                        instr.master_weight_item.add(cert_obj)
                        instr.save()

                except:
                    pass

            if item.get('range'):
                instr.nominal_value = item['range']
            if item.get('mass'):
                instr.mass_value = item['mass']

            instr.duc_id = duc_id
            instr.vt = vt
            instr.vr = vr
            instr.va = va
            instr.vo = vo

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']
            if item.get('nom_val'):
                instr.nominal_value = item['nom_val']

            instr.save()
            weightObsIt.mass_item.add(instr)

        weightObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()

    context = {
        'ordered_obser': ordered_obser,
        'form': form,
        'srfN': srfN,
        'uucForCalibration': uucForCalibration,
        'dataR': dataR,
        'massValN': massValN,
        'form1': form1,
        'weight_unit': weight_unit,
        'primary_intru': primary_intru,
        'secondry_intru': secondry_intru,
        'mass_item_nomunit': mass_item_nomunit,
        'mass_item_obsunit': mass_item_obsunit,
        'weight_item': weight_item,
        'vt': vt,
        'vr': vr,
        'va': va,
        'vo': vo,
        'weighing_unit': weighing_unit,
    }

    return render(request, "update_obs/updateobservation.html", context)


def etdrafts(request, id):
    newtest = Observation.objects.get(id=id)
    #print(newtest.scope, "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    mymode = newtest.uucForCalibration.source
    m = newtest.et_observation.first().etItem.all().values('type').distinct()
    parameters = []
    for a in m:
        parameter = a['type']
        parameters.append(parameter)

    newtest2 = etItem.objects.all()
    # new_val = etobservation.objects.filter(observation=newtest).temp4.values()
    avgTemp = newtest.et_observation.first().temp4


    #trial

    get_master = newtest.instrument.all()

    # Sales.objects.all().values_list('user_id', flat=True).distinct()
    new_quer = newtest.et_observation.first().etItem.all()
    mylist = []

    for item in new_quer:
        if item.accessoriesmaster.all():
            for items in item.accessoriesmaster.all():
                mylist.append(items)

    newset = set(mylist)
    mylist = list(newset)
    # new_quer = zip(get_master,get_accessory)
    #print(\

    rh1 = newtest.et_observation.first().rh1
    rh2 = newtest.et_observation.first().rh2
    rh3 = newtest.et_observation.first().rh3

    if rh1 != None:
        # itemNeed = (float(rh1) + float(rh2) + float(rh3))
        # itemNeed = round(itemNeed, 2)
        avgRh = 5 / 3
    else:
        avgRh = " "

    myLC = newtest.et_observation.first().etItem.all().values('least_count').distinct()
    abc = myLC.count()
    lc_val = None
    if abc == 1:
        lc_val = myLC.first()
        lc_val = lc_val['least_count']

    else:
        lc_val = 'Multiple'

    context = {
        'newtest':newtest,
        'newtest2': newtest2,
        'lc_val': lc_val,
        'avgTemp' : avgTemp,
        'avgRh' : avgRh,
        'parameters': parameters,
        'mymode': mymode,
        'new_quer': mylist
    }

    return render(request, 'obssheet/Electro_Technical.html', context)





def etdrafts2(request, id):
    newtest = Observation.objects.get(id=id)
    #print(newtest.scope, "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    mymode = newtest.uucForCalibration.source
    m = newtest.et_observation.first().etItem.all().values('type').distinct()
    parameters = []
    for a in m:
        parameter = a['type']
        parameters.append(parameter)

    newtest2 = etItem.objects.all()
    # new_val = etobservation.objects.filter(observation=newtest).temp4.values()
    avgTemp = newtest.et_observation.first().temp4


    #trial

    get_master = newtest.instrument.all()

    # Sales.objects.all().values_list('user_id', flat=True).distinct()
    new_quer = newtest.et_observation.first().etItem.all()
    mylist = []

    for item in new_quer:
        if item.accessoriesmaster.all():
            for items in item.accessoriesmaster.all():
                mylist.append(items)

    newset = set(mylist)
    mylist = list(newset)
    # new_quer = zip(get_master,get_accessory)
    #print(\

    rh1 = newtest.et_observation.first().rh1
    rh2 = newtest.et_observation.first().rh2
    rh3 = newtest.et_observation.first().rh3


    abcd = [1,23,3,4,5,6,7,8,9,0]
    if rh1 != None:
        # itemNeed = (float(rh1) + float(rh2) + float(rh3))
        # itemNeed = round(itemNeed, 2)
        avgRh = 5 / 3
    else:
        avgRh = " "

    myLC = newtest.et_observation.first().etItem.all().values('least_count').distinct()
    abc = myLC.count()
    lc_val = None
    if abc == 1:
        lc_val = myLC.first()
        lc_val = lc_val['least_count']

    else:
        lc_val = 'Multiple'

    context = {
        'newtest':newtest,
        'newtest2': newtest2,
        'lc_val': lc_val,
        'avgTemp' : avgTemp,
        'avgRh' : avgRh,
        'parameters': parameters,
        'mymode': mymode,
        'new_quer': mylist,
        'abcd': abcd
    }

    return render(request, 'obssheet/Electro_TechnicalWithoutBudget.html', context)




def prdrafts(request, id):
    newtest = Observation.objects.get(id=id)
    abcd = [1,2]
    try:
        srftest = newtest.parent_srf.id
    except:
        abcd = newtest.cal_observation_number.rsplit('/',1)
        abcd = abcd[0]
        newdec= SRFItem.objects.get(job_no=abcd)
        newtest.parent_srf = newdec
        srftest = newtest.parent_srf.id

    srfN = SRFItem.objects.get(id=srftest)

    uucForCalibration = str(srfN.instrument)
    m = Pressure.objects.filter(observation=newtest).first()
    idR = m.id
    dataR = Pressure.objects.get(id=idR)
    check_cycle = dataR.pressure_item.first()

    if check_cycle.observation4 == None:
        cycles = 2

    elif check_cycle.observation5 == None:
        cycles = 4
    else:
        cycles = 6
    cycn = cycles + 2
    cycn2 = cycn + 1
    #print(uucForCalibration)

    context = {
        'newtest': newtest,
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'cycn': cycn,
        'cycn2': cycn2,
        'abcd': abcd
    }

    return render(request, 'obssheet/pressureobssheet.html', context)


def prdrafts2(request, id):
    newtest = Observation.objects.get(id=id)


    try:
        srftest = newtest.parent_srf.id
        srfN = newtest.parent_srf
    except:
        abcd = newtest.cal_observation_number.rsplit('/',1)
        abcd = abcd[0]
        newdec= SRFItem.objects.get(job_no=abcd)
        newtest.parent_srf = newdec
        srftest = newtest.parent_srf.id
        srfN = newdec
    uucForCalibration = str(srfN.instrument)
    m = Pressure.objects.filter(observation=newtest).first()
    idR = m.id
    dataR = Pressure.objects.get(id=idR)
    check_cycle = dataR.pressure_item.first()

    if check_cycle.observation3 == None:
        cycles = 2

    elif check_cycle.observation5 == None:
        cycles = 4
    else:
        cycles = 6
    # cycles = 4
    cycn = cycles + 2
    abcd = [1,2,3,4,5,6,7,8,9,10]
    #print(uucForCalibration)

    context = {
        'newtest': newtest,
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'cycn': cycn,
        'abcd': abcd
    }

    return render(request, 'obssheet/pressureobssheetwithoutuncertainty.html', context)





def viewuncertainity(request, id):
    ordered_obser = Observation.objects.get(id=id)


    if ordered_obser.uucForCalibration.material_type == 'Electro_Technical':
        return redirect('observation:etuncertanitys', id)

    elif ordered_obser.uucForCalibration.material_type == 'Dimension':
        return redirect('observation:dimuncertanitys', id)
    elif ordered_obser.uucForCalibration.material_type == 'Pressure':
        return redirect('observation:pruncertanitys', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weighing_Balance':
        return redirect('observation:wbUncertanitys', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weight':
        return redirect('observation:weightUncertanitys', id)

    else:
        return redirect('observation:observationDashboard')


def weightUncertanitys(request, id):
    newtest = Observation.objects.get(id=id)
    m = weightobservation.objects.filter(observation=newtest).first()
    weight_item = m.mass_item.all()
    master = newtest.parent_srf.instrument.procedure_master.master_equipment.values()
    master_uncertain = master[0]['uncertainty']
    master_range = master[0]['size']
    master_least_count = master[0]['lc_resolution']

    m = newtest.weight_observation.first().mass_item.all()

    for i in m:
        itemlist = [float(i.obs1), float(i.obs2), float(i.obs3), float(i.obs4), float(i.obs5)]
        stV = stdev(itemlist, ddof=1)

    context = {
        'newtest': newtest,
        'master_uncertain':master_uncertain,
        'stV' : stV,
        'master_range':master_range,
        'master_least_count':master_least_count,
        'weight_item':weight_item,
        'duc_unc':newtest.uucForCalibration,
    }

    return render(request, 'budgeting/weightbudgeting.html', context)

def weightdetailuncertanitys(request, id):
    newtest = MassItem.objects.get(id=id)

    obs = newtest.mass_items.first().observation
    uuc = obs.uucForCalibration

    context = {
        'newtest': newtest,
        'uuc':uuc,


    }

    return render(request, 'budgeting/weightdetaileduncertainity.html', context)


def etuncertanitys(request, id):
    newtest = Observation.objects.get(id=id)
    newtest2 = etItem.objects.all()
    iNeed = newtest.et_observation.first().etItem.all()
    m = newtest.et_observation.first().etItem.all().values('type').distinct()
    parameters = []
    for a in m:
        parameter = a['type']
        parameters.append(parameter)

    get_master = newtest.instrument.all()

    # Sales.objects.all().values_list('user_id', flat=True).distinct()
    new_quer = newtest.et_observation.first().etItem.all()
    mylist = []

    for item in new_quer:
        if item.accessoriesmaster.all():
            for items in item.accessoriesmaster.all():
                mylist.append(items)

    newset = set(mylist)
    mylist = list(newset)

    context = {
        'newtest': newtest,
        'parameters' : parameters,

        'iNeed': iNeed,
        'mylist': mylist

    }

    return render(request, 'budgeting/uncertainitybudgeting.html', context)




def dimDraft(request, id):
    newtest = Observation.objects.get(id=id)

    srftest = newtest.parent_srf.id
    srfN = SRFItem.objects.get(id=srftest)

    uucForCalibration = str(srfN.instrument)
    #print(uucForCalibration)

    context = {
        'newtest': newtest,
        'uucForCalibration': uucForCalibration,
    }

    return render(request, 'observation/dimdraft.html', context)

def detailetuncertanitys(request, id):
    newtest = etItem.objects.get(id=id)
    items = newtest
    uncetainity_fetch = newtest.etItemUncertainty()
    accuracyN = uncetainity_fetch['accuracyQ']
    accuracyN = etAccessorySpecification.objects.get(id=accuracyN)

    master_uncertainQ = uncetainity_fetch['master_uncertainQ']
    master_uncertainQ = CertItem.objects.get(id=master_uncertainQ)
    newtest2 = newtest.et_items.first().observation

    lc_duc_unit_parameter = newtest.type


    context = {
        'newtest': newtest,
        'accuracyN': accuracyN,
        'items': items,
        'master_uncertainQ': master_uncertainQ,
        'newtest2': newtest2
    }

    return render(request, 'observation/detailuncertainitybudgeting.html', context)

def pruncertanitys(request, id):
    ids = id
    newtest = Observation.objects.get(id=int(ids))
    nonN = Pressure.objects.filter(observation=newtest).first()
    idR = nonN.id

    dataR = Pressure.objects.get(id=idR)

    prid = dataR.max_vale()

    max_std_pressure = pressureItem.objects.get(id=prid)

    duc_id = max_std_pressure.duc_id
    duc_unc = UUCMaster.objects.get(id=duc_id)

    # for items in duc_unc.master_uncertainty.ub.all():
    #     #print(items)


    check_cycle = dataR.pressure_item.first()

    if check_cycle.observation3 == None:
        cycles = 2

    elif check_cycle.observation5 == None:
        cycles = 4
    else:
        cycles = 6

    dof = cycles-1


    m = newtest.pressure_observation.first().pressure_item.all()

    context = {
        'newtest': newtest,
        'cycles': cycles,
        'max_std_pressure':max_std_pressure,
        'duc_unc':duc_unc,
        'dof':dof,
    }
    return render(request, 'budgeting/prbudgeting.html', context)



def prdetailuncertanitys(request, id):
    newtest = pressureItem.objects.get(id=id)

    dataR = newtest.pressure_items.first()
    items = newtest
    item = newtest
    uncetainity_fetch = newtest.pr_ItemUncertainty()
    # accuracyN = uncetainity_fetch['accuracyQ']
    max_std_pressure = pressureItem.objects.get(id=id)
    duc_id = max_std_pressure.duc_id
    duc_unc = UUCMaster.objects.get(id=duc_id)
    master_uncertainQ = uncetainity_fetch['master_uncertainity']
    check_cycle = dataR.pressure_item.first()

    if check_cycle.observation3 == None:
        cycles = 2

    elif check_cycle.observation5 == None:
        cycles = 4
    else:
        cycles = 6

    dof = cycles-1

    ua_lim = cycles - 1
    # lc_duc_unit_parameter = newtest.type
    newtest2 = dataR.observation

    context = {
        'newtest': newtest,
        # 'accuracyN': accuracyN,
        'items': items,
        'item': item,
        'master_uncertainQ': master_uncertainQ,
        'duc_unc':duc_unc,
        'cycles': cycles,
        'ua_lim': ua_lim,
        'newtest2': newtest2
        # 'parameters' : parameters,

        # 'iNeed': iNeed

    }

    return render(request, 'observation/prdetailuncertainitybudgeting.html', context)



def dimuncertanitys(request, id):
    ids = id
    newtest = Observation.objects.get(id=int(ids))
    nonN = dimobservation.objects.filter(observation=newtest).first()
    idR = nonN.id
    dataR = dimobservation.objects.get(id=idR)
    anyitem = dataR.dimItem.first()
    duc_id = anyitem.duc_id

    dicts = {}

    duc_unc = UUCMaster.objects.get(id=duc_id)

    context = {
        'newtest': newtest,
        'duc_unc' : duc_unc,

    }
    return render(request, 'observation/dimuncertainitybudgeting.html', context)



def dimdetailuncertanitys(request, id):
    newtest = dimItem.objects.get(id=id)
    dimobs = dimobservation.objects.get(dimItem=newtest)
    obser = newtest.dim_item.first().observation

    temp_diff = float(dimobs.temp2) - float(dimobs.temp1)

    duc_id = newtest.duc_id

    dataR = newtest.dim_item.first()
    items = newtest
    item = newtest

    duc_unc = UUCMaster.objects.get(id=duc_id)

    context = {
        'newtest': newtest,
        'items': items,
        'item': item,
        'duc_unc':duc_unc,
        'obser': obser,
        'dimobs':dimobs,
        'temp_diff':temp_diff

    }

    return render(request, 'observation/dimdetailuncertainitybudgeting.html', context)

def wbdetailuncertanitys(request, id):
    newtest = WeighingBalanceItem.objects.get(id=id)

    obs = newtest.weighing_item.first().observation
    uuc = obs.uucForCalibration

    context = {
        'newtest': newtest,
        'uuc':uuc,
    }

    return render(request, 'budgeting/wbdetaileduncertainity.html', context)


def wbUncertanitys(request,id):
    newtest = Observation.objects.get(id=id)
    m = WeighingBalance.objects.filter(observation=newtest).first()
    weighing_item = m.weighing_item.all()
    master = newtest.parent_srf.instrument.procedure_master.master_equipment.values()
    master_uncertain = master[0]['uncertainty']
    master_range = master[0]['size']
    master_least_count = master[0]['lc_resolution']
    anyitem = m.weighing_item.first()
    duc_id = anyitem.duc_id
    duc_unc = UUCMaster.objects.get(id=duc_id)



    context = {
        'newtest': newtest,
        'weighing_item':weighing_item,
        'duc_unc':duc_unc
    }

    return render(request, 'budgeting/wbuncertainitybudget.html', context)

def viewdrafts(request, id):
    ordered_obser = Observation.objects.get(id=id)

    if ordered_obser.uucForCalibration.material_type == 'Electro_Technical':
        return redirect('observation:etdrafts', id)
    elif ordered_obser.uucForCalibration.material_type == 'Dimension':
        return redirect('observation:dimDraft', id)
    elif ordered_obser.uucForCalibration.material_type == 'Pressure':
        return redirect('observation:prdrafts', id)


    elif ordered_obser.uucForCalibration.material_type == 'Weighing_Balance':
        return redirect('observation:wbdraft', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weight':
        return redirect('observation:weightdraft', id)

    else:
        return redirect('observation:observationDashboard')



def viewdrafts2(request, id):
    ordered_obser = Observation.objects.get(id=id)

    if ordered_obser.uucForCalibration.material_type == 'Electro_Technical':
        return redirect('observation:etdrafts2', id)
    elif ordered_obser.uucForCalibration.material_type == 'Dimension':
        return redirect('observation:dimDraft', id)
    elif ordered_obser.uucForCalibration.material_type == 'Pressure':
        return redirect('observation:prdrafts2', id)


    elif ordered_obser.uucForCalibration.material_type == 'Weighing_Balance':
        return redirect('observation:wbdraft', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weight':
        return redirect('observation:weightdraft', id)

    else:
        return redirect('observation:observationDashboard')


def WBdraft(request, id):
    newtest = Observation.objects.get(id=id)
    srftest = newtest.parent_srf.id
    srfN = SRFItem.objects.get(id=srftest)

    uucForCalibration = str(srfN.instrument)
    anyItem = newtest.weighingbalance_observation.first().weighing_item.first()


    context = {
        'newtest': newtest,
        'uucForCalibration': uucForCalibration,
        'anyItem': anyItem
    }

    return render(request, 'obssheet/wbDraft.html', context)


def weightdraft(request, id):
    ordered_obser = Observation.objects.get(id=id)
    abcdef = [1,6,11,16,21,26,31]
    newtest=ordered_obser
    srf_id = ordered_obser.parent_srf.id
    srfN = SRFItem.objects.get(id=srf_id)
    srf_re = srfN.job_no
    txt = srf_re.rsplit("-")
    #print(txt[0], "iiiiiiiii IIIIIIIIIIII YYYYYYYYYYYYYYYYYYYY")
    srfattched = ServiceRequirement.objects.get(srfno=txt[0])
    srfNoN = srfattched.srfno

    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)


    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN

            }
    form = ObservationForm(initial=data)

    m = weightobservation.objects.filter(observation=ordered_obser).first()
    weight_item = m.mass_item.all()

    idR = m.id

    dataR = weightobservation.objects.get(id=idR)
    anyItem = dataR.mass_item.first()
    vt = anyItem.vt
    vr = anyItem.vr
    vo = anyItem.vo
    va = anyItem.va

    mass_item = dataR.mass_item.values()


    mass_itemNN = mass_item[0]
    massValN =mass_itemNN['mass_value']

    mass_item_obsunit = mass_itemNN['obsUnit']
    mass_item_nomunit = mass_itemNN['nominal_value']

    form1 = WeightForm(instance=dataR)



    context = {
        'ordered_obser': ordered_obser,
        'form': form,
        'uucForCalibration': uucForCalibration,
        'dataR':dataR,
        'massValN':massValN,
        'form1':form1,
        'weight_unit':weight_unit,
        'primary_intru':primary_intru,
        'secondry_intru':secondry_intru,
        'mass_item_nomunit':mass_item_nomunit,
        'mass_item_obsunit':mass_item_obsunit,
        'weight_item':weight_item,
        'vt': vt,
        'vr': vr,
        'va': va,
        'vo': vo,
        'newtest':ordered_obser,
        'weighing_unit':weight_unit,
        'abcdef': abcdef



    }
    return render(request, 'obssheet/weightdraft.html', context)


def viewcertificate(request, id):
    pka = int(id)
    uucertificate = UUCCertificate.objects.get(id=pka)
    ordered_obser = uucertificate.observation_created

    if ordered_obser.uucForCalibration.material_type == 'Electro_Technical':
        return redirect('observation:etcertificate', id)
    elif ordered_obser.uucForCalibration.material_type == 'Dimension':
        return redirect('observation:updatedim', id)
    elif ordered_obser.uucForCalibration.material_type == 'Pressure':
        return redirect('observation:prcertificate', id)

    elif ordered_obser.uucForCalibration.material_type == 'Weighing_Balance':
        return redirect('observation:WBcertificate', id)
    elif ordered_obser.uucForCalibration.material_type == 'Weight':
        return redirect('observation:Weightcertificate', id)

    else:
        return redirect('observation:observationDashboard')

def Weightcertificate(request, id):
    pka = int(id)
    uucertificate = UUCCertificate.objects.get(id=pka)
    myobservation = uucertificate.observation_created
    mysrf = uucertificate.observation_created.parent_srf
    ulr_no = uucertificate.ulr_number
    newtest = uucertificate.observation_created

    srftest = newtest.parent_srf.id

    srfN = SRFItem.objects.get(id=srftest)

    uucForCalibration = str(srfN.instrument)
    mex = weightobservation.objects.filter(observation=newtest).first()
    idR = mex.id
    dataR = weightobservation.objects.get(id=idR)
    print(dataR.mass_item.all())
    check_cycle = dataR.mass_item.first()

    # if check_cycle.observation4 == None:
    #     cycles = 3
    #
    # elif check_cycle.observation5 == None:
    #     cycles = 4
    # else:
    #     cycles = 6

    # print(uucForCalibration)

    context = {
        'newtest': newtest,
        'uucForCalibration': uucForCalibration,
        # 'cycles': cycles,
        # 'check_cycle': check_cycle,
        'dataR': dataR,
        'uucertificate': uucertificate,
        'mysrf': mysrf,
        'myobservation': myobservation,
        'mex': mex
    }
    return render(request, 'certificates/WeightCertificate.html', context)


def etcertificate(request, id):
    newtest = Observation.objects.get(id=id)

    myLC = newtest.et_observation.first().etItem.all().values('least_count').distinct()

    abc = myLC.count()
    lc_val = None
    if abc == 1:
        lc_val = myLC.first()
        lc_val = lc_val['least_count']

    else:
        lc_val = 'Multiple'

    r = newtest.et_observation.first().etItem.all().values()
    etitemslist = newtest.et_observation.first().etItem.all()

    m = newtest.et_observation.first().etItem.all().values('type').distinct()

    calibratedBy = newtest.et_observation.first().calibratedBy

    my_parameter_list = []
    for a in m:
        parameter = a['type']
        my_parameter_list.append(parameter)

    context = {
        'newtest': newtest,
        'lc_val': lc_val,
        'my_parameter_list': my_parameter_list,
        'etitemslist': etitemslist,
        'calibratedBy': calibratedBy.username,

    }
    return render(request, 'observation/testmul.html', context)


def prcertificate(request, id):
    pka = int(id)
    uucertificate = UUCCertificate.objects.get(id=pka)
    myobservation = uucertificate.observation_created
    mysrf = uucertificate.observation_created.parent_srf
    ulr_no = uucertificate.ulr_number
    newtest = uucertificate.observation_created

    srftest = newtest.parent_srf.id

    srfN = SRFItem.objects.get(id=srftest)

    uucForCalibration = str(srfN.instrument)
    m = Pressure.objects.filter(observation=newtest).first()
    idR=m.id
    dataR = Pressure.objects.get(id=idR)
    check_cycle = dataR.pressure_item.first()

    if check_cycle.observation4 == None:
        cycles = 3

    elif check_cycle.observation5 == None:
        cycles = 4
    else:
        cycles = 6

    if check_cycle.observation3 == None:
        dof = 1
    elif check_cycle.observation5 == None:
        dof = 2
    else:
        dof = 3

    #print(uucForCalibration)

    context = {
        'newtest': newtest,
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'check_cycle':check_cycle,
        'dataR':dataR,
        'uucertificate': uucertificate,
        'mysrf': mysrf,
        'myobservation': myobservation,
        'dof':dof
    }

    return render(request, 'certificates/prcertificate.html', context)

def WBcertificate(request, id):
    newtest = Observation.objects.get(id=id)
    weigobs = newtest.weighingbalance_observation.first()

    weighing_item = weigobs.weighing_item.all()

    context = {
        'newtest': newtest,
        'massitem':weighing_item,
    }

    return render(request, 'certificates/wbCertificate.html', context)



@csrf_exempt
def updateET(request, id):

    ordered_obser = Observation.objects.get(id=id)
    m = ordered_obser.et_observation.first().etItem.all().values('type').distinct()
    parameters = []
    for a in m:
        parameter = a['type']
        parameters.append(parameter)


    mode = ordered_obser.mode
    if mode == "Source Mode":
        a1 = "Std"
        a2 = "UUC"
    else:
        a1 = "UUC"
        a2 = "Std"

    srf_id = ordered_obser.parent_srf.id

    srfN = SRFItem.objects.get(id=srf_id)


    srfNoN = srfN.srfIt.first().srfno
    #print("gggg", srfNoN)
    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)
    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)
    cycles = srfN.instrument.procedure_master.cycles



    if cycles:
        pass
    else:
        cycles = 5

    m = etobservation.objects.filter(observation=ordered_obser).first()
    etLoop = m.etItem.all()

    etLoopItem = etLoop.values('type', 'least_count', 'accessoriesmaster').distinct()


    idR= m.id

    dataR = etobservation.objects.get(id=idR)
    #print(dataR.temp1,"asdddddddddddddddddddssssssssssssssssfaaaaaaaaaaaaaaaavvvvvvvvvvvvvvvvvvvvvvvvv")


    form1 = ETForm(instance=dataR)
    form3 = etItemForm()


    observIt = m


    electrothermal1 = m
    # #print(electrothermal1.id, 'asdsf------------------------dfdfd')
    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles
    #print(uucForCalibration.material_type)

    if request.method == "POST":

        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')
        #print("cccccc", button_clicked)

        allvalue = request.POST.getlist('arrayOID[]')
        allvalue = json.loads(allvalue[0])

        #print(allvalue, "555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")

        srfItN = SRFItem.objects.get(id=sfn_id)
        # fotest = Observation.objects.get(parent_srf=srfItN)
        # fotest.cal_observation_number = cal_observation_no


        obsIt = ordered_obser
        etObsIt = m
        #print("i am here")
        #print(allvalue, "ashu ashu ashu ashu ashu asnu ashu--------------------------------")


        obsIt.et_observation.first().etItem.all().delete()

        for item in allvalue:

            instr = etItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item.get('sn')

            if item.get('cal_point'):
                instr.nominal_value = item['cal_point']
            if item.get('value_on'):
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']

            if item.get('nom_1'):
                instr.nom_1 = item['nom_1']
            if item.get('nom_2'):
                instr.nom_2 = item['nom_2']
            if item.get('nom_3'):
                instr.nom_3 = item['nom_3']
            if item.get('nom_4'):
                instr.nom_4 = item['nom_4']
            if item.get('nom_5'):
                instr.nom_5 = item['nom_5']


            if item.get('lc_duc'):
                instr.least_count = item['lc_duc']
            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']
            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('instru_range'):
                instr.instru_range = item['instru_range']
            if item.get('instru_range_unit'):
                instr.instru_range_unit = item['instru_range_unit']

            instr.save()
            etObsIt.etItem.add(instr)
            etObsIt.save()

        etObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()

    context = {
        'ordered_obser' : ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'dataR' : dataR,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'electrothermal1': electrothermal1,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'etLoopItem': etLoopItem,
        'a1': a1,
        'a2': a2,
        'parameters': parameters
    }

    return render(request, "update_obs/updateobservation.html", context)




@csrf_exempt
def updateThermal(request, id):

    ordered_obser = Observation.objects.get(id=id)
    m = ordered_obser.et_observation.first().etItem.all().values('type').distinct()
    parameters = []
    for a in m:
        parameter = a['type']
        parameters.append(parameter)


    mode = ordered_obser.mode
    if mode == "Source Mode":
        a1 = "Std"
        a2 = "UUC"
    else:
        a1 = "UUC"
        a2 = "Std"

    srf_id = ordered_obser.parent_srf.id

    srfN = SRFItem.objects.get(id=srf_id)


    srfNoN = srfN.srfIt.first().srfno
    #print("gggg", srfNoN)
    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)
    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)
    cycles = srfN.instrument.procedure_master.cycles



    if cycles:
        pass
    else:
        cycles = 5

    m = etobservation.objects.filter(observation=ordered_obser).first()
    etLoop = m.etItem.all()

    etLoopItem = etLoop.values('type', 'least_count', 'accessoriesmaster').distinct()


    idR= m.id

    dataR = etobservation.objects.get(id=idR)
    #print(dataR.temp1,"asdddddddddddddddddddssssssssssssssssfaaaaaaaaaaaaaaaavvvvvvvvvvvvvvvvvvvvvvvvv")


    form1 = ETForm(instance=dataR)
    form3 = etItemForm()


    observIt = m


    electrothermal1 = m
    # #print(electrothermal1.id, 'asdsf------------------------dfdfd')
    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles
    #print(uucForCalibration.material_type)

    if request.method == "POST":

        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')
        #print("cccccc", button_clicked)

        allvalue = request.POST.getlist('arrayOID[]')
        allvalue = json.loads(allvalue[0])

        #print(allvalue, "555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")

        srfItN = SRFItem.objects.get(id=sfn_id)
        # fotest = Observation.objects.get(parent_srf=srfItN)
        # fotest.cal_observation_number = cal_observation_no


        obsIt = ordered_obser
        etObsIt = m
        #print("i am here")
        #print(allvalue, "ashu ashu ashu ashu ashu asnu ashu--------------------------------")


        obsIt.et_observation.first().etItem.all().delete()

        for item in allvalue:

            instr = etItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item.get('sn')

            if item.get('cal_point'):
                instr.nominal_value = item['cal_point']
            if item.get('value_on'):
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']

            if item.get('nom_1'):
                instr.nom_1 = item['nom_1']
            if item.get('nom_2'):
                instr.nom_2 = item['nom_2']
            if item.get('nom_3'):
                instr.nom_3 = item['nom_3']
            if item.get('nom_4'):
                instr.nom_4 = item['nom_4']
            if item.get('nom_5'):
                instr.nom_5 = item['nom_5']


            if item.get('lc_duc'):
                instr.least_count = item['lc_duc']
            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']
            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('instru_range'):
                instr.instru_range = item['instru_range']
            if item.get('instru_range_unit'):
                instr.instru_range_unit = item['instru_range_unit']

            instr.save()
            etObsIt.etItem.add(instr)
            etObsIt.save()

        etObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()

    context = {
        'ordered_obser' : ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'dataR' : dataR,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'electrothermal1': electrothermal1,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'etLoopItem': etLoopItem,
        'a1': a1,
        'a2': a2,
        'parameters': parameters
    }

    return render(request, "update_obs/updateobservation.html", context)


@csrf_exempt
def weighingUncertainView(request):
    if request.method == "POST":
        duc_id = request.POST.get('duc_id')
        lc_duc = request.POST.get('lc_duc')

        cal_point = request.POST.get('cal_point')
        obs_point_unit = request.POST.get('obs_point_unit')
        obs1 = request.POST.get('obs1')
        obs2 = request.POST.get('obs2')
        obs3 = request.POST.get('obs3')
        obs4 = request.POST.get('obs4')
        obs5 = request.POST.get('obs5')

        nomUnit = request.POST.get('nomUnit')
        obsUnit = request.POST.get('obsUnit')


        HR1 = request.POST.get('HR1')
        HR2 = request.POST.get('HR2')
        HR3 = request.POST.get('HR3')
        HR4 = request.POST.get('HR4')
        HR5 = request.POST.get('HR5')
        HR6 = request.POST.get('HR6')
        HR7 = request.POST.get('HR7')
        HR8 = request.POST.get('HR8')
        HR9 = request.POST.get('HR9')
        HR10 = request.POST.get('HR10')

        FR1 = request.POST.get('FR1')
        FR2 = request.POST.get('FR2')
        FR3 = request.POST.get('FR3')
        FR4 = request.POST.get('FR4')
        FR5 = request.POST.get('FR5')
        FR6 = request.POST.get('FR6')
        FR7 = request.POST.get('FR7')
        FR8 = request.POST.get('FR8')
        FR9 = request.POST.get('FR9')
        FR10 = request.POST.get('FR10')

        eccentricity_max_min = request.POST.get('eccentricity_max_min')
        temp=1


        abc = None
        if obs1 != '':
            abc = WeighingItemUncertainty(duc_id, lc_duc, cal_point, obs1, obs2, obs3, obs4, obs5, nomUnit, obsUnit,temp, eccentricity_max_min, HR1, HR2, HR3, HR4, HR5, HR6, HR7, HR8, HR9, HR10, FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9,FR10)

    #print(json.dumps(abc))
    return HttpResponse(json.dumps(abc))

dimensions_unit = (
    ('mm', 'mm'),
    ('µm', 'µm')
)


@csrf_exempt
def updatedim(request, id):

    ordered_obser = Observation.objects.get(id=id)
    srf_id = ordered_obser.parent_srf.id
    srfN = SRFItem.objects.get(id=srf_id)
    srfNoN = srfN.srfIt.first().srfno
    unt = choice_i_need
    locN = srfN.srfIt.first().location
    calN = srfNoN + '/' + str(srfN.id)

    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"



    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)

    cycles = srfN.instrument.procedure_master.cycles
    if cycles:
        pass
    else:
        cycles = 5

    m = dimobservation.objects.filter(observation=ordered_obser).first()

    idR = m.id
    dataR = dimobservation.objects.get(id=idR)

    anyItem =  m.dimItem.first()
    least_count = anyItem.least_count

    idR= m.id

    form1 = DimensionForm(instance=m)
    form3 = etItemForm()
    observIt = m
    Dimension1 = m


    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles
    #print(uucForCalibration.material_type)

    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        least_count = request.POST.get('least_count')
        button_clicked = request.POST.get('button_clicked')
        #print("cccccc", button_clicked)


        allvalue = request.POST.getlist('arrayOID[]')
        allvalue = json.loads(allvalue[0])

        srfItN = SRFItem.objects.get(id=sfn_id)

        obsIt = ordered_obser
        etObsIt = m

        obsIt.dim_observations.first().dimItem.all().delete()
        for item in allvalue:
            instr = dimItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))
            instr.job_no = item.get('sn')
            instr.least_count = least_count

            if item.get('cal_point'):
                instr.nominal_value = item['cal_point']
            if item.get('value_on'):
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']

            if item.get('method'):
                instr.method = item['method']

            if item.get('lc_duc'):
                instr.least_count = item['lc_duc']
            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']
            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']

            instr.save()
            etObsIt.dimItem.add(instr)
            etObsIt.save()


        etObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()

    context = {
        'ordered_obser' : ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'least_count':least_count,
        'dataR' : dataR,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'Dimension1': Dimension1,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'primary_intru':primary_intru,
        'secondry_intru':secondry_intru,
        'dimensions_unit':dimensions_unit

    }

    return render(request, "update_obs/updateobservation.html", context)


pressure_unit = (
    ('Pascal', 'Pascal'),
    ('bar', 'bar'),
    ('psi', 'psi'),
    ('kg/cm2', 'kg/cm2'),
    ('mmH2o', 'mmH2o'),
    ('mmHg', 'mmHg'),
    ('inHg', 'inHg'),
    ('mbar', 'mbar'),
    ('mpa', 'mpa'),
    ('kpa', 'kpa'),
    ('inH2o', 'inH2o'),
    ('cmH2o', 'cmH2o'),
    ('hpa', 'hpa'),
)

@csrf_exempt
def updatepre(request, id):
    ordered_obser = Observation.objects.get(id=id)

    try:
        srf_id = ordered_obser.parent_srf.id
    except:
        abcd = ordered_obser.cal_observation_number.rsplit('/',1)
        abcd = abcd[0]
        newdec= SRFItem.objects.get(job_no=abcd)
        ordered_obser.parent_srf = newdec
        srf_id = ordered_obser.parent_srf.id

    srfN = SRFItem.objects.get(id=srf_id)

    srfNoN = srfN.srfIt.first().srfno

    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"

    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)



    m = Pressure.objects.filter(observation=ordered_obser).first()



    idR= m.id

    dataR = Pressure.objects.get(id=idR)

    check_cycle = dataR.pressure_item.first()
    any_least_count = check_cycle.least_count
    any_middle_temp = check_cycle.middle_temp

    if check_cycle.observation3 == None and check_cycle.observation4 == None and check_cycle.observation5 == None and check_cycle.observation6 == None:
        cycles = 2

    elif check_cycle.observation3 != None and check_cycle.observation4 == None and check_cycle.observation5 == None and check_cycle.observation6 == None:
        cycles = 3

    elif check_cycle.observation3 != None and check_cycle.observation4 != None and check_cycle.observation5 == None and check_cycle.observation6 == None:
        cycles = 4
    elif check_cycle.observation3 != None and check_cycle.observation4 != None and check_cycle.observation5 != None and check_cycle.observation6 == None:
        cycles = 5

    else:
        cycles = 6


    least_count = dataR.least_count



    # #print(dataR.pressure_item.all().values())

    form1 = PressureForm(instance=dataR)

    form3 = etItemForm()


    observIt = m


    PressD = m
    # #print(electrothermal1.id, 'asdsf------------------------dfdfd')
    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles
    #print(uucForCalibration.material_type)

    #print(cycles, "gggggggggggggggggggeeeeeeee rrrrrrrrrrrrrrrrttttttttttttttttttttttttttt")

    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        least_count = request.POST.get('least_count')
        starting_temp = request.POST.get('start_temp')
        ending_temp = request.POST.get('end_temp')
        duc_id = request.POST.get('duc_id')
        diff = request.POST.get('diff')

        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')
        #print("cccccc", button_clicked)
        allvalue = request.POST.getlist('arrayOID[]')
        allvalue = json.loads(allvalue[0])
        srfItN = SRFItem.objects.get(id=sfn_id)
        obsIt = ordered_obser
        prObsIt = Pressure.objects.filter(observation=ordered_obser).first()


        obsIt.pressure_observation.first().pressure_item.all().delete()

        for item in allvalue:
            instr = pressureItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))
            instr.job_no = item.get('sn')
            instr.least_count = least_count

            instr.startingTemp = starting_temp
            instr.endingTemp = ending_temp
            instr.duc_id = duc_id
            instr.zero_deviation = diff

            if item.get('uuc'):
                instr.nominal_value = item['uuc']

            if item.get('x1'):
                instr.observation1 = item['x1']
            if item.get('x2'):
                instr.observation2 = item['x2']
            if item.get('x3'):
                instr.observation3 = item['x3']
            if item.get('x4'):
                instr.observation4 = item['x4']
            if item.get('x5'):
                instr.observation5 = item['x5']
            if item.get('x6'):
                instr.observation6 = item['x6']

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']

            instr.save()
            prObsIt.pressure_item.add(instr)
            prObsIt.least_count =least_count
            prObsIt.save()


        prObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()

    context = {
        'ordered_obser' : ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'dataR' : dataR,
        'observIt': observIt,
        'least_count':least_count,
        'idn': id,
        'srfN': srfN,
        'PressD': PressD,
        'noNeed': range(noNeed),
        'any_middle_temp':any_middle_temp,
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'primary_intru': primary_intru,
        'secondry_intru': secondry_intru,
        'pressure_unit':pressure_unit,
        'cycles':cycles,

    }

    return render(request, "update_obs/updateobservation.html", context)



def viewET(request,id):
    ordered_obser = Observation.objects.get(id=id)
    mode = ordered_obser.mode
    if mode == "Source Mode":
        a1 = "Std"
        a2 = "UUC"
    else:
        a1 = "UUC"
        a2 = "Std"

    srf_id = ordered_obser.parent_srf.id
    srfN = SRFItem.objects.get(id=srf_id)
    # srfNoN = srfN.srfIt.first().srfno

    try:
        srfNoN = ordered_obser.parent_srf.id
    except:
        abcd = ordered_obser.cal_observation_number.rsplit('/',1)
        abcd = abcd[0]
        newdec= SRFItem.objects.get(job_no=abcd)
        newtest.parent_srf = newdec
        srfNoN = ordered_obser.parent_srf.id

    #print("gggg", srfNoN)
    unt = choice_i_need
    locN = srfN.srfIt.first().location
    calN = srfNoN + '/' + str(srfN.id)
    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)
    cycles = srfN.instrument.procedure_master.cycles

    if cycles:
        pass
    else:
        cycles = 5

    m = etobservation.objects.filter(observation=ordered_obser).first()
    etLoop = m.etItem.all()

    etLoopItem = etLoop.values('type', 'least_count').distinct()
    idR = m.id
    dataR = etobservation.objects.get(id=idR)

    form1 = ETForm(instance=dataR)
    form3 = etItemForm()

    observIt = m

    electrothermal1 = m
    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles
    #print(uucForCalibration.material_type)



    context = {
        'ordered_obser': ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'dataR': dataR,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'electrothermal1': electrothermal1,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'etLoopItem': etLoopItem,
        'a1':a1,
        'a2': a2,


    }

    return render(request, "view_obs/viewobservation.html", context)



dimensions_unit = (
    ('mm', 'mm'),
    ('µm', 'µm')
)

def viewDIM(request, id):
    ordered_obser = Observation.objects.get(id=id)
    srf_id = ordered_obser.parent_srf.id
    srfN = SRFItem.objects.get(id=srf_id)
    srfNoN = srfN.srfIt.first().srfno
    unt = choice_i_need
    locN = srfN.srfIt.first().location
    calN = srfNoN + '/' + str(srfN.id)

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)

    cycles = srfN.instrument.procedure_master.cycles
    if cycles:
        pass
    else:
        cycles = 5

    m = dimobservation.objects.filter(observation=ordered_obser).first()

    idR = m.id
    dataR = dimobservation.objects.get(id=idR)

    anyItem = m.dimItem.first()
    least_count = anyItem.least_count

    idR = m.id

    form1 = DimensionForm(instance=m)
    form3 = etItemForm()
    observIt = m
    Dimension1 = m

    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles
    #print(uucForCalibration.material_type)



    context = {
        'ordered_obser': ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'least_count': least_count,
        'dataR': dataR,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'Dimension1': Dimension1,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'dimensions_unit':dimensions_unit

    }

    return render(request, "view_obs/viewobservation.html", context)


def approval(request, id):

    obs = Observation.objects.get(id=id)
    obs.approved = True
    obs.save()
    return redirect('observation:technicaldashboard')



def reject(request, id):
    obs = Observation.objects.get(id=id)
    obs.rejected = True
    obs.submit = False
    obs.rejected_by = request.user
    obs.save()
    return redirect('observation:observationDashboard')



def viewPr(request, id):

    ordered_obser = Observation.objects.get(id=id)
    newtest = ordered_obser

    try:
        srftest = newtest.parent_srf.id
    except:
        abcd = newtest.cal_observation_number.rsplit('/',1)
        abcd = abcd[0]
        newdec= SRFItem.objects.get(job_no=abcd)
        newtest.parent_srf = newdec
        srftest = newtest.parent_srf.id

    srfN = SRFItem.objects.get(id=srftest)
    srfNoN = srfN.srfIt.first().srfno

    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp

    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }

    form = ObservationForm(initial=data)

    m = Pressure.objects.filter(observation=ordered_obser).first()

    idR = m.id

    dataR = Pressure.objects.get(id=idR)

    check_cycle = dataR.pressure_item.first()
    any_least_count = check_cycle.least_count
    any_middle_temp = check_cycle.middle_temp

    if check_cycle.observation3 == None and check_cycle.observation4 == None and check_cycle.observation5 == None and check_cycle.observation6 == None:
        cycles = 2

    elif check_cycle.observation3 != None and check_cycle.observation4 == None and check_cycle.observation5 == None and check_cycle.observation6 == None:
        cycles = 3

    elif check_cycle.observation3 != None and check_cycle.observation4 != None and check_cycle.observation5 == None and check_cycle.observation6 == None:
        cycles = 4
    elif check_cycle.observation3 != None and check_cycle.observation4 != None and check_cycle.observation5 != None and check_cycle.observation6 == None:
        cycles = 5

    else:
        cycles = 6

    form1 = PressureForm(instance=dataR)

    form3 = etItemForm()

    observIt = m

    PressD = m
    # #print(electrothermal1.id, 'asdsf------------------------dfdfd')
    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles


    #print(uucForCalibration.material_type)



    context = {
        'ordered_obser': ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'dataR': dataR,
        'any_middle_temp':any_middle_temp,
        'any_least_count':any_least_count,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'PressD': PressD,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification

    }

    return render(request, "view_obs/viewobservation.html", context)



@csrf_exempt
def weighingBalanceView(request):
    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')
        id_humidity = request.POST.get('id_humidity')
        check_source_measure = request.POST.get('check_source_measure')

        start_temp = request.POST.get('start_temp')
        end_temp = request.POST.get('end_temp')
        zero_error = request.POST.get('id_zero_error')
        least_count=request.POST.get('least_count')
        allvalue = request.POST.getlist('arrayOID[]')

        E1 = request.POST.get('E1')
        E2 = request.POST.get('E2')
        E3 = request.POST.get('E3')
        E4 = request.POST.get('E4')
        E5 = request.POST.get('E5')
        E6 = request.POST.get('E6')
        E7 = request.POST.get('E7')
        E8 = request.POST.get('E8')
        E9 = request.POST.get('E9')
        E10 = request.POST.get('E10')
        E11 = request.POST.get('E11')

        HR1 = request.POST.get('HR1')
        HR2 = request.POST.get('HR2')
        HR3 = request.POST.get('HR3')
        HR4 = request.POST.get('HR4')
        HR5 = request.POST.get('HR5')
        HR6 = request.POST.get('HR6')
        HR7 = request.POST.get('HR7')
        HR8 = request.POST.get('HR8')
        HR9 = request.POST.get('HR9')
        HR10 = request.POST.get('HR10')

        HR11 = request.POST.get('HR1')
        HR12 = request.POST.get('HR12')
        HR13 = request.POST.get('HR13')
        HR14 = request.POST.get('HR14')
        HR15 = request.POST.get('HR15')
        HR16 = request.POST.get('HR16')
        HR17 = request.POST.get('HR17')
        HR18 = request.POST.get('HR18')
        HR19 = request.POST.get('HR19')
        HR20 = request.POST.get('HR20')

        FR1 = request.POST.get('FR1')
        FR2 = request.POST.get('FR2')
        FR3 = request.POST.get('FR3')
        FR4 = request.POST.get('FR4')
        FR5 = request.POST.get('FR5')
        FR6 = request.POST.get('FR6')
        FR7 = request.POST.get('FR7')
        FR8 = request.POST.get('FR8')
        FR9 = request.POST.get('FR9')
        FR10 = request.POST.get('FR10')



        FR11 = request.POST.get('FR11')
        FR12 = request.POST.get('FR12')
        FR13 = request.POST.get('FR13')
        FR14 = request.POST.get('FR14')
        FR15 = request.POST.get('FR15')
        FR16 = request.POST.get('FR16')
        FR17 = request.POST.get('FR17')
        FR18 = request.POST.get('FR18')
        FR19 = request.POST.get('FR19')
        FR20 = request.POST.get('FR20')

        EA = request.POST.get('ea')
        EB = request.POST.get('eb')
        EC = request.POST.get('ec')
        ED = request.POST.get('ed')
        EO = request.POST.get('eo')

        
        halfload_value = request.POST.get('halfload_value')
        halfloadUnit = request.POST.get('halfloadUnit')

        fulload_value = request.POST.get('fulload_value')
        fullloadUnit = request.POST.get('fullloadUnit')
        eccentricity_loading = request.POST.get('eccentricity_loading')
        eccentricityUnit = request.POST.get('eccentricityUnit')





        allvalue = json.loads(allvalue[0])

        srfItN = SRFItem.objects.get(id=sfn_id)
        obsIt = Observation.objects.create(parent_srf=srfItN, cal_observation_number=cal_observation_no, calibration_performed_at=id_calibration_performed_at)
        obsIt.mode = check_source_measure
        obsIt.uucForCalibration = srfItN.instrument



        etObsIt = WeighingBalance.objects.create(observation=obsIt, calibratedBy=request.user, remarks = remarks,starting_temp=start_temp,ending_temp=end_temp, humidity=id_humidity, zero_error=zero_error)
        #print("i am here")
        #print(allvalue)

        for item in allvalue:
            instr = WeighingBalanceItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item['sn']

            if item.get('cal_point'):
                #print(item['cal_point'])
                instr.nominal_value = item['cal_point']

            if item.get('value_on'):
                #print("*************************************************************************************************************")
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']
            if item.get('least_count'):
                instr.least_count = item['least_count']
            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']
            if item.get('rangeP'):
                instr.type = item['rangeP']

            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']

            if item.get('arraycert'):
                try:
                    for i in item['arraycert']:
                        ids = int(i)
                        cert_obj = WeightCertificate.objects.get(id=ids)
                        instr.master_weight_item.add(cert_obj)

                except:
                    pass

            instr.halfload_value=halfload_value
            instr.halfloadUnit=halfloadUnit
            instr.fulload_value=fulload_value
            instr.fullloadUnit=fullloadUnit
            instr.eccentricity_loading=eccentricity_loading
            instr.eccentricityUnit=eccentricityUnit
            instr.zero_error=zero_error
            instr.least_count=least_count

            instr.E1 = E1
            instr.E2 = E2
            instr.E3 = E3
            instr.E4 = E4
            instr.E5 = E5
            instr.E6 = E6
            instr.E7 = E7
            instr.E8 = E8
            instr.E9 = E9
            instr.E10 = E10
            instr.E11 = E11            

            instr.HR1 = HR1
            instr.HR2 = HR2
            instr.HR3 = HR3
            instr.HR4 = HR4
            instr.HR5 = HR5
            instr.HR6 = HR6
            instr.HR7 = HR7
            instr.HR8 = HR8
            instr.HR9 = HR9
            instr.HR10 = HR10

            instr.HR11 = HR11
            instr.HR12 = HR12
            instr.HR13 = HR13
            instr.HR14 = HR14
            instr.HR15 = HR15
            instr.HR16 = HR16
            instr.HR17 = HR17
            instr.HR18 = HR18
            instr.HR19 = HR19
            instr.HR20 = HR20
            

            instr.FR1 = FR1
            instr.FR2 = FR2
            instr.FR3 = FR3
            instr.FR4 = FR4
            instr.FR5 = FR5
            instr.FR6 = FR6
            instr.FR7 = FR7
            instr.FR8 = FR8
            instr.FR9 = FR9
            instr.FR10 = FR10


            instr.FR11 = FR11
            instr.FR12 = FR2
            instr.FR13 = FR13
            instr.FR14 = FR14
            instr.FR15 = FR15
            instr.FR16 = FR16
            instr.FR17 = FR17
            instr.FR18 = FR18
            instr.FR19 = FR19
            instr.FR20 = FR20

            instr.EA = EA
            instr.EB = EB
            instr.EC = EC
            instr.ED = ED
            instr.EO = EO

            instr.save()
            etObsIt.weighing_item.add(instr)
            etObsIt.save()

        etObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.save()




        return redirect('observation:observationDashboard')



weighing_unit = (
    ('g', 'g'),
    ('kg', 'kg'),
    ('mg', 'mg')
)



def updateWB(request, id):
    ordered_obser = Observation.objects.get(id=id)
    srf_id = ordered_obser.parent_srf.id
    srfN = SRFItem.objects.get(id=srf_id)
    srfNoN = srfN.srfIt.first().srfno
    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)



    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)

    cycles = srfN.instrument.procedure_master.cycles
    if cycles:
        pass
    else:
        cycles = 5

    m = WeighingBalance.objects.filter(observation=ordered_obser).first()
    idR = m.id
    dataR = WeighingBalance.objects.get(id=idR)
    idR = m.id

    anyItem = m.weighing_item.first()

    form1 = WeighingForm(instance=m)
    form3 = etItemForm()
    observIt = m
    Weighing = m

    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles

    if request.method == "POST":
        sfn_id = request.POST.get('sfn_id')
        id_calibration_performed_at = request.POST.get('id_calibration_performed_at')
        cal_observation_no = request.POST.get('cal_observation_no')
        remarks = request.POST.get('remarks')
        button_clicked = request.POST.get('button_clicked')
        id_humidity = request.POST.get('id_humidity')

        start_temp = request.POST.get('start_temp')
        end_temp = request.POST.get('end_temp')
        zero_error = request.POST.get('id_zero_error')

        HR1 = request.POST.get('HR1')
        HR2 = request.POST.get('HR2')
        HR3 = request.POST.get('HR3')
        HR4 = request.POST.get('HR4')
        HR5 = request.POST.get('HR5')
        HR6 = request.POST.get('HR6')
        HR7 = request.POST.get('HR7')
        HR8 = request.POST.get('HR8')
        HR9 = request.POST.get('HR9')
        HR10 = request.POST.get('HR10')

        FR1 = request.POST.get('FR1')
        FR2 = request.POST.get('FR2')
        FR3 = request.POST.get('FR3')
        FR4 = request.POST.get('FR4')
        FR5 = request.POST.get('FR5')
        FR6 = request.POST.get('FR6')
        FR7 = request.POST.get('FR7')
        FR8 = request.POST.get('FR8')
        FR9 = request.POST.get('FR9')
        FR10 = request.POST.get('FR10')

        EA = request.POST.get('ea')
        EB = request.POST.get('eb')
        EC = request.POST.get('ec')
        ED = request.POST.get('ed')
        EO = request.POST.get('eo')

        allvalue = request.POST.getlist('arrayOID[]')
        #print(allvalue, "gfhfgfghfg")
        allvalue = json.loads(allvalue[0])

        srfItN = SRFItem.objects.get(id=sfn_id)

        obsIt = ordered_obser
        etObsIt = m

        obsIt.weighingbalance_observation.first().weighing_item.all().delete()



        #print("i am here")
        #print(allvalue)

        for item in allvalue:
            instr = WeighingBalanceItem.objects.create(instrument=UUCMaster.objects.get(id=srfItN.instrument.id))

            instr.job_no = item['sn']

            if item.get('cal_point'):
                #print(item['cal_point'])
                instr.nominal_value = item['cal_point']

            if item.get('value_on'):
                instr.value_on = item['value_on']
            if item.get('obs1'):
                instr.observation_1 = item['obs1']
            if item.get('obs2'):
                instr.observation_2 = item['obs2']
            if item.get('obs3'):
                instr.observation_3 = item['obs3']
            if item.get('obs4'):
                instr.observation_4 = item['obs4']
            if item.get('obs5'):
                instr.observation_5 = item['obs5']
            if item.get('least_count'):
                instr.least_count = item['least_count']
            if item.get('lc_duc_unit_parameter'):
                instr.type = item['lc_duc_unit_parameter']
            if item.get('rangeP'):
                instr.type = item['rangeP']

            if item.get('duc_id'):
                instr.duc_id = item['duc_id']
            if item.get('cal_point_unit'):
                instr.calculation_unit = item['cal_point_unit']

            if item.get('nomUnit'):
                instr.nomUnit = item['nomUnit']
            if item.get('obsUnit'):
                instr.obsUnit = item['obsUnit']

            instr.HR1 = HR1
            instr.HR2 = HR2
            instr.HR3 = HR3
            instr.HR4 = HR4
            instr.HR5 = HR5
            instr.HR6 = HR6
            instr.HR7 = HR7
            instr.HR8 = HR8
            instr.HR9 = HR9
            instr.HR10 = HR10

            instr.FR1 = FR1
            instr.FR2 = FR2
            instr.FR3 = FR3
            instr.FR4 = FR4
            instr.FR5 = FR5
            instr.FR6 = FR6
            instr.FR7 = FR7
            instr.FR8 = FR8
            instr.FR9 = FR9
            instr.FR10 = FR10

            instr.EA = EA
            instr.EB = EB
            instr.EC = EC
            instr.ED = ED
            instr.EO = EO



            instr.save()
            etObsIt.weighing_item.add(instr)
            etObsIt.starting_temp = start_temp
            etObsIt.ending_temp = end_temp
            etObsIt.humidity = id_humidity
            etObsIt.zero_error = zero_error
            etObsIt.save()

        etObsIt.save()

        if button_clicked == 'Save':
            obsIt.is_saves = True
        else:
            obsIt.is_saves = False
        if button_clicked == 'Submit':
            obsIt.submit = True
        else:
            obsIt.submit = False

        obsIt.calibration_performed_at = id_calibration_performed_at
        obsIt.location = id_calibration_performed_at

        obsIt.save()



    context = {
        'ordered_obser': ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'dataR': dataR,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'Weighing': Weighing,
        'anyItem': anyItem,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'weighing_unit': weighing_unit,
        'primary_intru':primary_intru,
        'secondry_intru':secondry_intru


    }

    return render(request, "update_obs/updateobservation.html", context)

weighing_unit = (
    ('g', 'g'),
    ('kg', 'kg'),
    ('mg', 'mg')
)


def viewWB(request, id):
    ordered_obser = Observation.objects.get(id=id)
    srf_id = ordered_obser.parent_srf.id
    srfN = SRFItem.objects.get(id=srf_id)
    srfNoN = srfN.srfIt.first().srfno
    unt = choice_i_need
    locN = ordered_obser.calibration_performed_at
    calN = srfNoN + '/' + str(srfN.id)

    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"


    if ordered_obser.mode == "Source Mode":
        primary_intru = "Std"
        secondry_intru = "UUC"
    else:
        primary_intru = "Std"
        secondry_intru = "UUC"

    ref_standardN = srfN.instrument.procedure_master.ref_standard
    uucForCalibration = srfN.instrument
    environmental_conditionN = srfN.instrument.procedure_master.environmental_condition_temp
    data = {'cal_observation_number': calN,
            'calibration_performed_at': locN,
            'ref_standard': ref_standardN,
            'environmental_condition': environmental_conditionN
            }
    form = ObservationForm(initial=data)

    cycles = srfN.instrument.procedure_master.cycles
    if cycles:
        pass
    else:
        cycles = 5

    m = WeighingBalance.objects.filter(observation=ordered_obser).first()
    idR = m.id
    dataR = WeighingBalance.objects.get(id=idR)
    idR = m.id

    anyItem = m.weighing_item.first()

    form1 = WeighingForm(instance=m)
    form3 = etItemForm()
    observIt = m
    Weighing = m
    obserItem=m.weighing_item.all()

    obserItem2=m.weighing_item.first()

    tempVar = srfN.instrument.procedure_master.templateT
    noNeed = srfN.instrument.procedure_master.cycles



    context = {
        'obserItem':obserItem,
        'obserItem2':obserItem2,
        'weighing_unit':weighing_unit,
        'ordered_obser': ordered_obser,
        'form': form,
        'form1': form1,
        'form3': form3,
        'dataR': dataR,
        'observIt': observIt,
        'idn': id,
        'srfN': srfN,
        'anyItem':anyItem,
        'Weighing': Weighing,
        'noNeed': range(noNeed),
        'uucForCalibration': uucForCalibration,
        'cycles': cycles,
        'choice_i_need': choice_i_need,
        'type_clarification': type_clarification,
        'primary_intru': primary_intru,
        'secondry_intru': secondry_intru

    }

    return render(request, "view_obs/viewobservation.html", context)

@csrf_exempt
def getContact(request):
    if request.method == "POST":
        allinstru = request.POST.getlist('arrayIN[]')
        allinstru_list = json.loads(allinstru[0])

        certinstrus = []

        for instrus in allinstru_list:
            if instrus.get('instrument'):
                ids = instrus['instrument']
                abc = instrumentMaster.objects.get(id=ids)
                certficate = abc.instrument_certificate.first()
                certinstrus.append(certficate)
   
        context = {
            'certinstrus':certinstrus,
            }
        
        return render(request,"observation/drop.html", context)



def generateobs(request, id):
    observation = Observation.objects.get(id=id)
    onbn = Observation.objects.get(id=id)
    try:
        observation = UUCCertificate.objects.get(observation_created=observation)

    except:
        genrate = UUCCertificate.objects.create(observation_created=observation)
        genrate.observation_generated = True
        genrate.save()
        observation = genrate

        observation.item_calibarted_at = observation.observation_created.calibration_performed_at
        observation.type = observation.observation_created.uucForCalibration.material_type
        observation.acceptance_limits = observation.observation_created
        observation.range = observation.observation_created.parent_srf.range
        observation.calibration_range = observation.observation_created.operating_range
        observation.zero_error = observation.observation_created.zero_error
        observation.condition = observation.observation_created.parent_srf.physical_condition
        observation.item_location = observation.observation_created
        observation.serial_number = observation.observation_created.parent_srf.mfrno
        observation.location = observation.observation_created.calibration_performed_at
        observation.nomenclature = observation.observation_created.uucForCalibration.instrument_name

        observation.temperature_limit = observation.observation_created.uucForCalibration.procedure_master.environmental_condition_temp
        observation.humidity_limit = observation.observation_created.uucForCalibration.procedure_master.environmental_condition_humidity

        observation.make = observation.observation_created.parent_srf.make_model
        observation.model = observation.observation_created.parent_srf.make_model

        observation.created_on = observation.observation_created.calibrated_on
        observation.suggested_date_of_calibration = observation.observation_created.calibrated_on
        observation.item_received = observation.observation_created.calibrated_on
        observation.calibrated_on = observation.observation_created.calibrated_on

    form = obssheetForm(instance=observation)

    last_certi = UUCCertificate.objects.all()[:10]
    if request.method == 'POST':
        print('post')
        form = obssheetForm(instance=observation, data=request.POST)
        if form.is_valid():
            print('valid')

            form.save()
            return redirect('observation:observationDashboard')
    context = {
        'form': form,
        'last_certi': last_certi
    }
    return render(request, "observation/obasheetgeneate.html", context)
