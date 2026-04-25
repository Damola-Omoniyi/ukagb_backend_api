from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from exam_data.models import (ExamBoard, Subject, ExamSession, OverallGradeBoundary, GradeStatistic, ExamPaper, 
                              ComponentGradeBoundary, DocumentURL)


class ExamDataAPITestCase(APITestCase):
    def setUp(self):
        self.exam_board1 = ExamBoard.objects.create(name="AQA")
        self.exam_board2 = ExamBoard.objects.create(name="Edexcel")
        self.exam_board3 = ExamBoard.objects.create(name="OCR")

        self.subject1 = Subject.objects.create(exam_board=self.exam_board1, name="Maths")
        self.subject2 = Subject.objects.create(exam_board=self.exam_board1, name="English")
        self.subject3 = Subject.objects.create(exam_board=self.exam_board1, name="Physics")

        self.exam_session1 = ExamSession.objects.create(subject=self.subject1, year =2018)
        self.exam_session2 = ExamSession.objects.create(subject=self.subject1, year =2019)

        self.boundary1 = OverallGradeBoundary.objects.create(exam_session=self.exam_session1, grade="A", grade_threshold=259)
        self.boundary2 = OverallGradeBoundary.objects.create(exam_session=self.exam_session1, grade="B", grade_threshold=230)
        self.boundary3 = OverallGradeBoundary.objects.create(exam_session=self.exam_session2, grade="B", grade_threshold=220)
        self.boundary4 = OverallGradeBoundary.objects.create(exam_session=self.exam_session2, grade="C", grade_threshold=120)

        self.statistic1 = GradeStatistic.objects.create(exam_session=self.exam_session1, grade="A", percentage = 24.5, num_students=2000)
        self.statistic2 = GradeStatistic.objects.create(exam_session=self.exam_session1, grade="B", percentage = 45.5, num_students=4000)
        self.statistic3 = GradeStatistic.objects.create(exam_session=self.exam_session1, grade="D", percentage = 31.75, num_students=6000)

        self.paper1 = ExamPaper.objects.create(exam_session=self.exam_session1, paper_number="1")
        self.paper_boundary = ComponentGradeBoundary.objects.create(exam_paper=self.paper1, grade="E", grade_threshold=25)

        self.url1 = DocumentURL.objects.create(paper=self.paper1, document_type="past_paper",  url="https://www.aqa.org.uk/past-paper.pdf")
        self.url2 = DocumentURL.objects.create(paper=self.paper1, document_type="mark_scheme",  url="https://www.ocr.org.uk/mark-scheme")

    def test_exam_board_list(self):
        url = reverse('exam-board-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_subject_list(self):
        url = reverse('subject-list', kwargs={"exam_board_name": "AQA"})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_grade_boundaries_list(self):
        url = reverse('grade-boundaries-list', kwargs={"exam_board_name":"AQA", "subject_name":"Maths"})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_grade_statistics_list(self):
        url = reverse('grade-statistic-list', kwargs={"exam_board_name":"AQA", "subject_name":"Maths", "year":2018})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_component_grade_list(self):
        url = reverse('component-grade-list',  kwargs={"exam_board_name":"AQA", "subject_name":"Maths", "year":2018})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_url_list(self):
        url = reverse('url-list', kwargs={"exam_board_name":"AQA", "subject_name":"Maths", "year":2018, "paper_number":"1"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    



        
            
            


