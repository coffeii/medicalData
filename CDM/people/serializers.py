from rest_framework.serializers import ModelSerializer
from .models import Person, VisitOccurrence, ConditionOccurrence, DrugExposure, Death, Concept


class PersonSerializer(ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'
        

class VisitOccurrenceSerializer(ModelSerializer):

    class Meta:
        model = VisitOccurrence
        fields = '__all__'


class ConditionOccurrenceSerializer(ModelSerializer):

    class Meta:
        model = ConditionOccurrence
        fields = '__all__'


class DrugExposureSerializer(ModelSerializer):

    class Meta:
        model = DrugExposure
        fields = '__all__'


class DeathSerializer(ModelSerializer):

    class Meta:
        model = Death
        fields = '__all__'


class ConceptSerializer(ModelSerializer):

    class Meta:
        model = Concept
        fields = '__all__'