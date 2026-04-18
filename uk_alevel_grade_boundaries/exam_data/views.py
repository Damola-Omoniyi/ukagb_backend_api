from exam_data.models import ExamBoard, Subject, OverallGradeBoundary, GradeStatistic, ComponentGradeBoundary, DocumentURL
from exam_data.serializers import (ExamBoardSerializer, SubjectSerializer, OverallGradeSerializer, 
                                   GradeStatisticSerializer, ComponentGradeSerializer, URLSerializer)
from rest_framework import generics

class ExamBoardList(generics.ListAPIView):
    queryset = ExamBoard.objects.all()
    serializer_class = ExamBoardSerializer


class SubjectList(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        exam_board_name = self.kwargs.get("exam_board_name")
        return Subject.objects.filter(exam_board__name=exam_board_name)

class GradeBoundaryList(generics.ListAPIView):
    serializer_class = OverallGradeSerializer
    def get_queryset(self):
        exam_board_name = self.kwargs.get("exam_board_name")
        subject_name = self.kwargs.get("subject_name")
        
        return OverallGradeBoundary.objects.filter(subject__name = subject_name,
                                                   subject__exam_board__name = exam_board_name)


class GradeStatisticList(generics.ListAPIView):
    serializer_class = GradeStatisticSerializer

    def get_queryset(self):
        exam_board_name = self.kwargs.get("exam_board_name")
        subject_name = self.kwargs.get("subject_name")
        
        return GradeStatistic.objects.filter(subject__name = subject_name,
                                             subject__exam_board__name = exam_board_name)


class ComponentGradeList(generics.ListAPIView):
    serializer_class = ComponentGradeSerializer

    def get_queryset(self):
        year = self.kwargs.get("year")
        exam_board_name = self.kwargs.get("exam_board_name")
        subject_name = self.kwargs.get("subject_name")
        return ComponentGradeBoundary.objects.filter(overall_grade_boundary__subject__name = subject_name,
                                                     overall_grade_boundary__subject__exam_board__name = exam_board_name,
                                                     overall_grade_boundary__year = year
                                                     )

class DocumentURLList(generics.ListAPIView):
    serializer_class = URLSerializer

    def get_queryset(self):
        year = self.kwargs.get("year")
        exam_board_name = self.kwargs.get("exam_board_name")
        subject_name = self.kwargs.get("subject_name")
        paper_number = self.kwargs.get("paper_number")

        return DocumentURL.objects.filter(paper__overall_grade_boundary__subject__name = subject_name,
                                                     paper__overall_grade_boundary__subject__exam_board__name = exam_board_name,
                                                     paper__overall_grade_boundary__year = year,
                                                     paper__paper_number = paper_number)
