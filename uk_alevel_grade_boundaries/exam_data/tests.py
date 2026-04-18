from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from exam_data.models import ExamBoard,Subject,OverallGradeBoundary, GradeStatistic, ComponentGradeBoundary, DocumentURL


class OverallGradeBoundaryTestCase(TestCase):
    def setUp(self):
        self.exam_board = ExamBoard.objects.create(name = "AQA")
        self.subject = Subject.objects.create(exam_board = self.exam_board, name = "Physics")

    def test_year_too_low(self):
        boundary = OverallGradeBoundary(subject = self.subject, year = 2007, grade = "A", grade_threshold = 50 )
        with self.assertRaises(ValidationError):
            boundary.full_clean()

    def test_year_too_high(self):
        boundary = OverallGradeBoundary(subject = self.subject, year = now().year + 1, grade ="A", grade_threshold = 50 )
        with self.assertRaises(ValidationError):
            boundary.full_clean()
    
    def test_duplicate_boundaries(self):
        OverallGradeBoundary.objects.create(subject = self.subject, year = 2020, grade = "A", grade_threshold = 50)

        with self.assertRaises(IntegrityError):
            OverallGradeBoundary.objects.create(subject = self.subject, year = 2020, grade = "A", grade_threshold = 90 )
    
    def test_grade_threshold_positive(self):
        boundary = OverallGradeBoundary(subject = self.subject, year = 2020, grade = "A", grade_threshold = -50 )
        with self.assertRaises(ValidationError):
            boundary.full_clean()

class GradeStatisticsTestCase(TestCase):
    def setUp(self):
        self.exam_board = ExamBoard.objects.create(name = "AQA")
        self.subject = Subject.objects.create(exam_board = self.exam_board, name = "Physics")
    
    def test_year_too_high(self):
        statistic = GradeStatistic(subject = self.subject, year = now().year+1, grade = "A", percentage = 0.25, num_students = 100)
        with self.assertRaises(ValidationError):
            statistic.full_clean()

    def test_year_too_low(self):
        statistic = GradeStatistic(subject = self.subject, year = 2000, grade = "A", percentage = 0.25, num_students = 100)
        with self.assertRaises(ValidationError):
            statistic.full_clean()
    
    def test_percentage_too_low(self):
        statistic = GradeStatistic(subject = self.subject, year = 2018, grade = "A", percentage = -0.25, num_students = 100)
        with self.assertRaises(ValidationError):
            statistic.full_clean()

    def test_percentage_too_high(self):
        statistic = GradeStatistic(subject = self.subject, year = 2020, grade = "A", percentage =101.25, num_students = 100)
        with self.assertRaises(ValidationError):
            statistic.full_clean()
        
    def test_negative_number_of_students(self):
        statistic = GradeStatistic(subject = self.subject, year = 2020, grade = "A", percentage = 0.25, num_students = -100)
        with self.assertRaises(ValidationError):
            statistic.full_clean()
    
    def test_unique_statistic(self):
        GradeStatistic.objects.create(subject = self.subject, year = 2020, grade = "A", percentage = 0.25, num_students = 100)
        with self.assertRaises(IntegrityError):
            GradeStatistic.objects.create(subject = self.subject, year = 2020, grade = "A", percentage = 0.85, num_students = 100)

class ComponentGradeBoundaryTestCase(TestCase):
    def setUp(self):
        self.exam_board = ExamBoard.objects.create(name = "AQA")
        self.subject = Subject.objects.create(exam_board = self.exam_board, name = "Physics")
        self.boundary = OverallGradeBoundary.objects.create(subject = self.subject, year = 2020, grade = "A", grade_threshold = 50)
    
    def test_grade_threshold(self):
        component = ComponentGradeBoundary(paper_number = "1", overall_grade_boundary = self.boundary, grade="A", grade_threshold = -30)
        with self.assertRaises(ValidationError):
            component.full_clean()
    
    def test_unique_component(self):
        ComponentGradeBoundary.objects.create(paper_number = "1", overall_grade_boundary = self.boundary, grade="A", grade_threshold = 30)
        with self.assertRaises(IntegrityError):
            ComponentGradeBoundary.objects.create(paper_number = "1", overall_grade_boundary = self.boundary, grade="A", grade_threshold = 70)


class ExamDataAPITestCase(APITestCase):
    def setUp(self):
        self.exam_board1 = ExamBoard.objects.create(name="AQA")
        self.exam_board2 = ExamBoard.objects.create(name="Edexcel")
        self.exam_board3 = ExamBoard.objects.create(name="OCR")

        self.subject1 = Subject.objects.create(exam_board=self.exam_board1, name="Maths")
        self.subject2 = Subject.objects.create(exam_board=self.exam_board1, name="English")
        self.subject3 = Subject.objects.create(exam_board=self.exam_board1, name="Physics")

        self.boundary1 = OverallGradeBoundary.objects.create(subject=self.subject1, year=2018, grade="A", grade_threshold=259)
        self.boundary2 = OverallGradeBoundary.objects.create(subject=self.subject1, year=2018, grade="B", grade_threshold=230)
        self.boundary3 = OverallGradeBoundary.objects.create(subject=self.subject1, year=2024, grade="B", grade_threshold=220)
        self.boundary4 = OverallGradeBoundary.objects.create(subject=self.subject1, year=2023, grade="C", grade_threshold=120)

        self.statistic1 = GradeStatistic.objects.create(subject=self.subject1, year=2018, grade="A", percentage = 24.5, num_students=2000)
        self.statistic2 = GradeStatistic.objects.create(subject=self.subject1, year=2018, grade="B", percentage = 45.5, num_students=4000)
        self.statistic3 = GradeStatistic.objects.create(subject=self.subject1, year=2018, grade="D", percentage = 31.75, num_students=6000)

        self.paper1 = ComponentGradeBoundary.objects.create(paper_number=1, overall_grade_boundary=self.boundary1, grade="E", grade_threshold=25)

        self.url1 = DocumentURL.objects.create(paper=self.paper1, document_type="past_paper",  url="https://www.aqa.org.uk/past-paper.pdf")
        self.url2 = DocumentURL.objects.create(paper=self.paper1, document_type="mark_scheme",  url="https://www.aqa.org.uk/past-paper.pdf")

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
        url = reverse('grade-statistic-list', kwargs={"exam_board_name":"AQA", "subject_name":"Maths"})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_component_grade_list(self):
        url = reverse('component-grade-list',  kwargs={"exam_board_name":"AQA", "subject_name":"Maths", "year":2018})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_url_list(self):
        url = reverse('url-list', kwargs={"exam_board_name":"AQA", "subject_name":"Maths", "year":2018, "paper_number":1})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    



        
            
            


