from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
# from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import api_view
from .models import Person, VisitOccurrence, ConditionOccurrence, DrugExposure, Death, Concept
from .serializers import PersonSerializer, VisitOccurrenceSerializer, ConditionOccurrenceSerializer, DrugExposureSerializer, DeathSerializer, ConceptSerializer



# Create your views here.

# 응답 요청 확인용 
@api_view(('GET',))
def test(request):
 
    person = Person.objects.all()[1:3]
    person2 = Person.objects.all()[4:6]
    
    serializer = PersonSerializer(person, many=True)
    serializer2 = PersonSerializer(person2, many=True)
    memo = [{'data' :'!@$!@#$$#@!#@$'}]
    context = serializer.data + memo + serializer2.data
   
    return Response(context)
    

# 환자 통계 보여주기 위한 api 입니다.
@api_view(('GET',))
def patient(request):
    
    person = Person.objects.all()
    # death = Death.objects.all()

    # dict형태가 보여주기 편할거같아서 선택했습니다.
    race = {
        'asian' : 0,
        'other' : 0,
        'native' : 0,
        'white' : 0,
        'black' : 0
    }
    gender = {
        'M' : 0,
        'F' : 0
    }
    ethnicity = {
        'hispanic' : 0,
        'nonhispanic' : 0
    }

    for i in person:
        gender[i.gender_source_value] += 1
        race[i.race_source_value] += 1
        ethnicity[i.ethnicity_source_value] += 1

    context = {
       '전체 환자 수' : len(person),
       '성별 환자 수' : gender,
       '인종별 환자 수' : race,
       '민족별 환자 수' : ethnicity,
    #    '사망 환자 수' : len(death),   
    }
    
    return Response(context)



# 방문 통계 보여주기 위한 api 입니다.
@api_view(('GET',))
def visit(request):
    
    visit = VisitOccurrence.objects.all()
    person = Person.objects.all()

    visit_concept = {
        9201 : 0,
        9202 : 0,
        9203 : 0,
    }
    gender = {
        'M' : 0,
        'F' : 0
    }
    ethnicity = {
        'hispanic' : 0,
        'nonhispanic' : 0
    }
    race = {
        'asian' : 0,
        'other' : 0,
        'native' : 0,
        'white' : 0,
        'black' : 0
    }
    ages = {
        '0~9':0,
        '10~19':0,
        '20~29':0,
        '30~39':0,
        '40~49':0,
        '50~59':0,
        '60~69':0,
        '70~79':0,
        '80~89':0,
        '90~99':0,
        '100~109':0,
    }

    for i in visit:
        visit_concept[i.visit_concept_id] += 1
        
        ex_person = get_object_or_404(person, person_id=i.person_id)
        # 이부분에서 연산이 장난 아닌듯.
        gender[ex_person.gender_source_value] += 1
        race[ex_person.race_source_value] += 1
        ethnicity[ex_person.ethnicity_source_value] += 1
        visit_age = int(i.visit_start_date.year) - int(ex_person.year_of_birth)
        # age부분은 떠오르는 방법이 없어서 if문으로 일일이 처리했습니다.
        if visit_age < 10:
            ages['0~9'] += 1
        elif visit_age < 20:
            ages['10~19'] += 1
        elif visit_age < 30:
            ages['20~29'] += 1
        elif visit_age < 40:
            ages['30~39'] += 1
        elif visit_age < 50:
            ages['40~49'] += 1
        elif visit_age < 60:
            ages['50~59'] += 1
        elif visit_age < 70:
            ages['60~69'] += 1
        elif visit_age < 80:
            ages['70~79'] += 1
        elif visit_age < 90:
            ages['80~89'] += 1
        elif visit_age < 100:
            ages['90~99'] += 1
        elif visit_age < 110:
            ages['100~109'] += 1
        

    context = {
       '방문 유형별 방문 수' : visit_concept,
       '성별 환자 수' : gender,
       '인종별 환자 수' : race,
       '민족별 환자 수' : ethnicity,
       '방문시 연령대' : ages,   
    }
    
    return Response(context)
   


# concept 관련 정보를 찾는 api입니다
@api_view(('GET',))
def search(request):
    search = request.GET.get('search')
    # 'GET'방식 안에 들어있는 값을 꺼내서
    result = Concept.objects.filter(concept_id__contains=search).order_by('concept_id')
    # '__contains'로 해당값이 들어있는 모든 객체들을 선택했다.
    # 이후 값으로 정렬하면서 원하는값이 정확하면 가장 먼저 나오게 설정했다.
    serializer = ConceptSerializer(result, many=True)
    paginator = Paginator(serializer.data, 100)
    # Pagination 부분은 공식문서를 참고했습니다.
    # https://docs.djangoproject.com/en/3.2/topics/pagination/
    page_number = request.GET.get('page')
    page_obj = paginator.page(page_number).object_list
    
    totals = paginator.num_pages

    context = {
        '페이지' : f'{page_number} / {totals}',
        'page_obj' : page_obj,
    }
    
    return Response(context)



# 유저에 대한 모든 정보를 찾는 api입니다
@api_view(('GET',))
def onlyOne(request):
    user_id = request.GET.get('user')
    # 일치하는 유저가 있다면
    if Person.objects.filter(person_id=user_id).exists():
        theOne = Person.objects.get(person_id=user_id)
        visits = VisitOccurrence.objects.filter(person_id__exact=user_id)
        conditions = ConditionOccurrence.objects.filter(person_id__exact=user_id)
        drugs = DrugExposure.objects.filter(person_id__exact=user_id)

        theOne_serializer = PersonSerializer(theOne)
        visit_serializer = VisitOccurrenceSerializer(visits, many=True)
        condition_serializer = ConditionOccurrenceSerializer(conditions, many=True)
        drug_serializer = DrugExposureSerializer(drugs, many=True)

        # concept_id와 결합파트
        # theOne은 하나 이므로 for문 없이 그냥
        gender_concept_id = theOne.gender_concept_id
        race_concept_id = theOne.race_concept_id
        ethnicity_concept_id = theOne.ethnicity_concept_id
        gender_concept = Concept.objects.filter(concept_id=gender_concept_id)
        race_concept = Concept.objects.filter(concept_id=race_concept_id)
        ethnicity_concept = Concept.objects.filter(concept_id=ethnicity_concept_id)

        # concept_id 관련 첨부는 table이 끝나는 부분에 나오게 수정했다.
        id_extra_data = [{'person_table 관련정보' : {
            gender_concept_id : gender_concept[0].concept_name,
            race_concept_id : race_concept[0].concept_name,
            ethnicity_concept_id : ethnicity_concept[0].concept_name,
        }
        }]
        
        # 여러개의 데이터가 들어갈수 있으므로 for문을 돌린다.
        visit_temp = []
        for i in visits:
            visit_temp.append(i.visit_concept_id)

        visit_extra_data = [{'visit_table 관련정보': {}}]
        # 중복제거를 위한 set
        for i in set(visit_temp):
            visit_concept = Concept.objects.filter(concept_id__exact=i)
            visit_extra_data[0]['visit_table 관련정보'][f'{i}'] = visit_concept[0].concept_name


        condition_temp = []
        for i in conditions:
            condition_temp.append(i.condition_concept_id)

        condition_extra_data = [{'condition_table 관련정보': {}}]

        for i in set(condition_temp):
            condition_concept = Concept.objects.filter(concept_id__exact=i)
            condition_extra_data[0]['condition_table 관련정보'][f'{i}'] = condition_concept[0].concept_name


        drug_temp = []
        for i in drugs:
            drug_temp.append(i.drug_concept_id)

        drug_extra_data = [{'drug_table 관련정보': {}}]

        for i in set(drug_temp):
            drug_concept = Concept.objects.filter(concept_id__exact=i)
            drug_extra_data[0]['drug_table 관련정보'][f'{i}'] = drug_concept[0].concept_name


        total_data = [theOne_serializer.data] + id_extra_data + visit_serializer.data + visit_extra_data + condition_serializer.data + condition_extra_data + drug_serializer.data + drug_extra_data
        paginator = Paginator(total_data, 100)

        page_number = request.GET.get('page')
        page_obj = paginator.page(page_number).object_list
        
        totals = paginator.num_pages

        context = {
            '유저정보' : user_id,
            '페이지' : f'{page_number} / {totals}',
            'page_obj' : page_obj,
        }
        return Response(context)

    # 일치하는 유저가 없을때 유저 목록 반환
    else: 
        people = Person.objects.filter(person_id__contains=user_id).order_by('person_id')
        serializer = PersonSerializer(people, many=True)
        paginator = Paginator(serializer.data, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.page(page_number).object_list      
        totals = paginator.num_pages

        context = {
            '페이지' : f'{page_number} / {totals}',
            'page_obj' : page_obj,
        }
        
        return Response(context)