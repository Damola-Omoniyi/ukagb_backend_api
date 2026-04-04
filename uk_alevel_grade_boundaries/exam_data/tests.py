from django.test import TestCase
from exam_data.models import ExamBoard,Subject,OverallGradeBoundary, GradeStatistic, ComponentGradeBoundary
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now

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






        
            
            


