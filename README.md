리드미입니당



# 0.

> 데이터 베이스 받아서 작업해봤습니다.
>
> 백부분만 구현하였고, test는 POSTMAN을 사용하였습니다.





# 1. 사용방법

> 가상환경을 사용하실분들은 사용하셔도 됩니다.
>
> db관련 부분은 비어놔서 그쪽만 수정하고 돌리면 됩니다.
>
> ```
> cd CDM
> pip install -r requirements.txt
> python manage.py runserver
> ```
>
> 



# 2. 진행과정

### 1. 장고설치

```
pip install django, djangorestframework, psycopg2
```

> django는 장고설치 djangorestframework는 보내고 받기를 편하게 하기 위해서
>
> psycopg2는 posrgresql을 사용하기위해 설치했다



```
python manage.py startapp people
```

> 으로 people이라는 폴더를 생성해주었습니다.



### 2. db확인

```
python manage.py inspectdb > people/models.py
```

> models.py에 기존의 db의 정보를 받고 확인한뒤에 

```
python manage.py makemigrations
python manage.py migrate
```

> 로 db와 연동합니다.
>
> 이후 요청을 보내보면서 결과를 확인했습니다.



# 3. api설명

> 로컬로 돌려서 ``` http://127.0.0.1:8000/ ```로 시작합니다

- 환자통계

```
['GET']
http://127.0.0.1:8000/people/patient/
```

> 환자 테이블의 간단한 통계를 보여줍니다.
>
> 예상결과 : 
>
> ```
> {
> 
>   "전체 환자 수": 1000,
> 
>   "성별 환자 수": {
> 
>     "M": 548,
> 
>     "F": 452
> 
>   },
> 
>   "인종별 환자 수": {
> 
>     "asian": 65,
> 
>     "other": 1,
> 
>     "native": 3,
> 
>     "white": 845,
> 
>     "black": 86
> 
>   },
> 
>   "민족별 환자 수": {
> 
>     "hispanic": 120,
> 
>     "nonhispanic": 880
> 
>   }
> 
> }
> ```



- 방문통계

```
['GET']
http://127.0.0.1:8000/people/visit/
```

> 방문  테이블의 간단한 통계를 보여줍니다.
>
> 예상결과 : 
>
> ```
> {
>     "방문 유형별 방문 수": {
>         "9201": 1309,
>         "9202": 37026,
>         "9203": 3475
>     },
>     "성별 환자 수": {
>         "M": 22503,
>         "F": 19307
>     },
>     "인종별 환자 수": {
>         "asian": 2826,
>         "other": 82,
>         "native": 89,
>         "white": 35487,
>         "black": 3326
>     },
>     "민족별 환자 수": {
>         "hispanic": 4829,
>         "nonhispanic": 36981
>     },
>     "방문시 연령대": {
>         "0~9": 3225,
>         "10~19": 4738,
>         "20~29": 5509,
>         "30~39": 5645,
>         "40~49": 5825,
>         "50~59": 6023,
>         "60~69": 4678,
>         "70~79": 3587,
>         "80~89": 1658,
>         "90~99": 838,
>         "100~109": 84
>     }
> }
> ```



- concept 관련 검색

```
['GET']
http://127.0.0.1:8000/people/search/?search=4071&page=1
```

> 찾고자 하는 concept_id의 일부, 혹은 전체를 search에 넣고, page를 입력하면 데이터가 출력됩니다.
>
> 한페이지에 100개의 결과물이 출력됩니다.
>
> 예상결과 : 
>
> ```
> {
>     "페이지": "1 / 143",
>     "page_obj": [
>         {
>             "concept_id": 14071,
>             "concept_name": "Other dislocation of unspecified wrist and hand",
>             "domain_id": "Condition",
>             "vocabulary_id": "ICD10CM",
>             "concept_class_id": "6-char nonbill code",
>             "standard_concept": null,
>             "concept_code": "S63.096",
>             "valid_start_date": "2014-01-01",
>             "valid_end_date": "2099-12-31",
>             "invalid_reason": null
>         },
>         {
>             "concept_id": 194071,
>             "concept_name": "Pylorospasm",
>             "domain_id": "Condition",
>             "vocabulary_id": "SNOMED",
>             "concept_class_id": "Clinical Finding",
>             "standard_concept": "S",
>             "concept_code": "335002",
>             "valid_start_date": "1970-01-01",
>             "valid_end_date": "2099-12-31",
>             "invalid_reason": null
>         },
>     ...
> ```



- table row에 해당하는 유저 검색

```
['GET']
http://127.0.0.1:8000/people/onlyOne/?user=1022983&page=1
```

> 각 테이블의 row라고 해서 유저에 대한 정보라고 생각을 했습니다.
>
> user에 관련된 데이터를 table에서 전부 검색해서 보여줍니다. 그 테이블에서 나온 concept_id정보는 테이블 정보가 끝나는 지점에서 한번에 보여주게 했습니다.
>
> 예상결과 : 
>
> ```
> {
>     "유저정보": "1022983",
>     "페이지": "1 / 2",
>     "page_obj": [
>         {
>             "person_id": 1022983,
>             "gender_concept_id": 8507,
>             "year_of_birth": 1950,
>             "month_of_birth": 2,
>             "day_of_birth": 26,
>             "birth_datetime": "1950-02-26T00:00:00Z",
>             "race_concept_id": 8527,
>             "ethnicity_concept_id": 0,
>             "location_id": null,
>             "provider_id": null,
>             "care_site_id": null,
>             "person_source_value": "e0b46681-1ccf-488e-9766-bbdb1fe53af2",
>             "gender_source_value": "M",
>             "gender_source_concept_id": 0,
>             "race_source_value": "white",
>             "race_source_concept_id": 0,
>             "ethnicity_source_value": "hispanic",
>             "ethnicity_source_concept_id": 0
>         },
>         {
>             "person_table 관련정보": {
>                 "8507": "MALE",
>                 "8527": "White",
>                 "0": "No matching concept"
>             }
>         },
>         {
>             "visit_occurrence_id": 120483647,
>             "person_id": 1022983,
>             "visit_concept_id": 9202,
>             "visit_start_date": "1968-04-21",
>             "visit_start_datetime": "1968-04-21T10:23:09Z",
>             "visit_end_date": "1968-04-21",
>             "visit_end_datetime": "1968-04-21T10:53:09Z",
>             "visit_type_concept_id": 44818517,
>     ...
> ```
>
> 
>
> 만약에 person_id가 일치하지 않거나, 혹은 일부 내용만으로 찾으면 person_id의 일부분이 일치되는 table내용이 나온다.
>
> 예상결과:
>
> ```
> {
>     "페이지": "1 / 1",
>     "page_obj": [
>         {
>             "person_id": 1022320,
>             "gender_concept_id": 8532,
>             "year_of_birth": 2016,
>             "month_of_birth": 5,
>             "day_of_birth": 8,
>             "birth_datetime": "2016-05-08T00:00:00Z",
>             "race_concept_id": 8527,
>             "ethnicity_concept_id": 0,
>             "location_id": null,
>             "provider_id": null,
>             "care_site_id": null,
>             "person_source_value": "7401a3f0-37f0-4e84-bf3d-32dc5d59f814",
>             "gender_source_value": "F",
>             "gender_source_concept_id": 0,
>             "race_source_value": "white",
>             "race_source_concept_id": 0,
>             "ethnicity_source_value": "nonhispanic",
>             "ethnicity_source_concept_id": 0
>         },
>         {
>             "person_id": 1022983,
>             "gender_concept_id": 8507,
>             "year_of_birth": 1950,
>             "month_of_birth": 2,
>             "day_of_birth": 26,
>             "birth_datetime": "1950-02-26T00:00:00Z",
>             "race_concept_id": 8527,
>             "ethnicity_concept_id": 0,
>             "location_id": null,
>             "provider_id": null,
>             "care_site_id": null,
>             "person_source_value": "e0b46681-1ccf-488e-9766-bbdb1fe53af2",
>             "gender_source_value": "M",
>             "gender_source_concept_id": 0,
>             "race_source_value": "white",
>             "race_source_concept_id": 0,
>             "ethnicity_source_value": "hispanic",
>             "ethnicity_source_concept_id": 0
>         }
>     ]
> }
> ```





# 4. 후기

- 일단 DB에서 데이터 꺼내는 속도가 너무 느렸다. 

- 4만개의 데이터를 그냥 뿌리는데에 시간이 오래 걸리는 것으로 보아, 네트워크상에 문제일수도 있다고 생각은 했지만, 그래도 너무 느리다.(특히 Concept)



- 모델들 사이에 연관관계가 설정되어있지 않았다. 정규화 과정이 필요할것같다.

  - person 테이블에서 concept 테이블로 내용을 찾기 위해서 filter을 사용했는데, 역참조가 더 빠르다.

  

- 만약에 특정한 데이터들의 모음을 많이 쓰는데, 정보들이 여러 테이블에 흩어져있다면, 새로운 중복된 테이블을 만드는것도 방법이다.

  - 데이터 중복이 일어나고, 저장시에 시간이 좀더 걸리지만, 특정 정보들만 규합하는데에는 매우 빠르다.



- DEATH 테이블은 primary key가 없어서 django에서는 조회 자체가 불가능합니다.



- 시간이 없어서 serializer에 상세한 설정은 안했지만, 특정 항목들만 넣게 설정한다면, 원하는 항목만 추릴수 있습니다.

- 방문통계에서 연산이 엄청나게 큰데, 이중for때문인것으로 생각된다. 아마 정규화 과정이 된다면, 역참조로 좀더 빠른 연산이 가능할것이다.