from rest_framework import serializers
from exam_data.models import (ExamBoard, Subject, ExamSession, OverallGradeBoundary, GradeStatistic, ExamPaper, 
                              ComponentGradeBoundary, DocumentURL)

class ExamBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamBoard
        fields = ["id", "name"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSession
        fields = ["id","year"]

class OverallGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallGradeBoundary
        fields = ["id", "grade", "grade_threshold"]

class ComponentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentGradeBoundary
        fields = ["id", "grade", "grade_threshold"]

class GradeStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeStatistic
        fields = ["id", "grade", "percentage", "num_students"]

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamPaper
        fields = ["id", "paper_number"]

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentURL
        fields = ["id", "document_type", "url"]