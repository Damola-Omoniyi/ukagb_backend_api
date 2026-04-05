from rest_framework import serializers
from exam_data.models import (ExamBoard, Subject, OverallGradeBoundary,
                              GradeStatistic, ComponentGradeBoundary, DocumentURL)

class ExamBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamBoard
        fields = ["id", "name"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]

class OverallGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallGradeBoundary
        fields = ["id", "year", "grade", "grade_threshold"]

class ComponentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentGradeBoundary
        fields = ["id", "paper_number", "grade", "grade_threshold"]

class GradeStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeStatistic
        fields = ["id", "grade", "percentage", "num_students"]

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentURL
        fields = ["id", "document_type", "url"]