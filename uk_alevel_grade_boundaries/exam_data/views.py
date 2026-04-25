from django.shortcuts import get_object_or_404
from rest_framework import generics
from exam_data.models import (ExamBoard, Subject, ExamSession, OverallGradeBoundary, GradeStatistic, ExamPaper, 
                              ComponentGradeBoundary, DocumentURL)

from exam_data.serializers import (ExamBoardSerializer, SubjectSerializer, OverallGradeSerializer, 
                                   GradeStatisticSerializer, ComponentGradeSerializer, URLSerializer)

class ExamBoardList(generics.ListAPIView):
    queryset = ExamBoard.objects.all()
    serializer_class = ExamBoardSerializer


class SubjectList(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        exam_board = get_object_or_404(ExamBoard, name=self.kwargs["exam_board_name"])
        return Subject.objects.filter(exam_board=exam_board)

class GradeBoundaryList(generics.ListAPIView):
    serializer_class = OverallGradeSerializer

    def get_queryset(self):
        exam_board = get_object_or_404(ExamBoard, name=self.kwargs["exam_board_name"])
        subject = get_object_or_404(Subject, exam_board=exam_board, name=self.kwargs["subject_name"])
        return OverallGradeBoundary.objects.filter(exam_session__subject = subject)

class GradeStatisticList(generics.ListAPIView):
    serializer_class = GradeStatisticSerializer

    def get_queryset(self):
        exam_board = get_object_or_404(ExamBoard, name=self.kwargs["exam_board_name"])
        subject = get_object_or_404(Subject, exam_board=exam_board, name=self.kwargs["subject_name"])
        exam_session = get_object_or_404(ExamSession, subject=subject, year=self.kwargs["year"])
        
        return GradeStatistic.objects.filter(exam_session = exam_session)


class ComponentGradeList(generics.ListAPIView):
    serializer_class = ComponentGradeSerializer

    def get_queryset(self):
        exam_board = get_object_or_404(ExamBoard, name=self.kwargs["exam_board_name"])
        subject = get_object_or_404(Subject, exam_board=exam_board, name=self.kwargs["subject_name"])
        exam_session = get_object_or_404(ExamSession, subject=subject, year=self.kwargs["year"])
        return ComponentGradeBoundary.objects.filter(exam_paper__exam_session = exam_session)

class DocumentURLList(generics.ListAPIView):
    serializer_class = URLSerializer

    def get_queryset(self):
        exam_board = get_object_or_404(ExamBoard, name=self.kwargs["exam_board_name"])
        subject = get_object_or_404(Subject, exam_board=exam_board, name=self.kwargs["subject_name"])
        exam_session = get_object_or_404(ExamSession, subject=subject, year=self.kwargs["year"])
        exam_paper = get_object_or_404(ExamPaper,exam_session=exam_session, paper_number=self.kwargs["paper_number"])
        return DocumentURL.objects.filter(paper=exam_paper)
