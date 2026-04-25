from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from exam_data.models import (ExamBoard, Subject, ExamSession, OverallGradeBoundary, GradeStatistic, ExamPaper, 
                              ComponentGradeBoundary, DocumentURL)

class ModelTestCase(TestCase):
    def setUp(self):
        self.exam_board = ExamBoard.objects.create(name = "AQA")
        self.subject = Subject.objects.create(exam_board = self.exam_board, name = "Physics")
        self.exam_session = ExamSession.objects.create(subject=self.subject, year=2021)
        self.boundary = OverallGradeBoundary.objects.create(exam_session=self.exam_session, grade='A', grade_threshold=100)
        self.statistic = GradeStatistic.objects.create(exam_session=self.exam_session, grade="A", percentage=12.5, num_students = 40)
        self.exam_paper = ExamPaper.objects.create(exam_session = self.exam_session, paper_number="1")
        self.exam_paper2 = ExamPaper.objects.create(exam_session = self.exam_session, paper_number="2")
        self.component_boundary = ComponentGradeBoundary.objects.create(exam_paper=self.exam_paper, grade="A", grade_threshold=60)
        self.url = 'https://www.aqa.org.uk/files/sample-papers-and-mark-schemes.2022.june.AQA-71921-QP-JUN22_PDF/5ada22f946e7ffd420d45c1cef788840c42f261c.pdf'
        self.document = DocumentURL.objects.create(paper=self.exam_paper, document_type="past_paper", url=self.url)

    # Tests for Subject Model
    def test_duplicate_subject(self):
        with self.assertRaises(IntegrityError):
            Subject.objects.create(exam_board=self.exam_board, name="Physics")
        
    # Tests for the ExamSession Model
    def test_exam_session_year_too_low(self):
        exam_session = ExamSession(subject = self.subject, year = 1990)
        with self.assertRaises(ValidationError):
            exam_session.full_clean()
        
    def test_exam_session_year_too_high(self):
        exam_session = ExamSession(subject=self.subject, year=now().year+10)
        with self.assertRaises(ValidationError):
            exam_session.full_clean()
    
    def test_duplicate_exam_session(self):
        with self.assertRaises(IntegrityError):
            ExamSession.objects.create(subject=self.subject, year=2021)
        
    # Tests for OverallBoundary Model
    def test_grade_threshold_too_low(self):
        boundary = OverallGradeBoundary(exam_session=self.exam_session, grade='C', grade_threshold=-20)
        with self.assertRaises(ValidationError):
            boundary.full_clean()

    def test_duplicate_boundary(self):
        with self.assertRaises(IntegrityError):
            OverallGradeBoundary.objects.create(exam_session=self.exam_session, grade='A', grade_threshold=150)
    
    # Test for GradeStatistic Model
    def test_percentage_too_low(self):
        statistic = GradeStatistic(exam_session=self.exam_session, grade="C", percentage=-10, num_students = 40)
        with self.assertRaises(ValidationError):
            statistic.full_clean()
    
    def test_percentage_too_high(self):
        statistic = GradeStatistic(exam_session=self.exam_session, grade="D", percentage=101, num_students = 40)
        with self.assertRaises(ValidationError):
            statistic.full_clean()
    
    def test_num_students_too_low(self):
        statistic = GradeStatistic(exam_session=self.exam_session, grade="B", percentage=10, num_students = -40)
        with self.assertRaises(ValidationError):
            statistic.full_clean()
    
    def test_duplicate_stat(self):
        with self.assertRaises(IntegrityError):
            GradeStatistic.objects.create(exam_session=self.exam_session, grade="A", percentage=17.5, num_students = 60)
        
    # Test for Exam Paper - test for duplicates
    def test_duplicate_exam_paper(self):
        with self.assertRaises(IntegrityError):
            ExamPaper.objects.create(exam_session = self.exam_session, paper_number="1")

    # Test for component boundary - test grade threshold and duplicates
    def test_paper_threshold_too_low(self):
        component_boundary = ComponentGradeBoundary(exam_paper=self.exam_paper, grade="B", grade_threshold=-30)
        with self.assertRaises(ValidationError):
            component_boundary.full_clean()
    
    def test_duplicate_paper(self):
        with self.assertRaises(IntegrityError):
            ComponentGradeBoundary.objects.create(exam_paper=self.exam_paper, grade="A", grade_threshold=80)

    # Test URLS - test duplicates
    def test_duplicate_documents(self):
        with self.assertRaises(IntegrityError):
            DocumentURL.objects.create(paper=self.exam_paper, document_type="past_paper", url="https://chatgpt.com/?temporary-chat=true")

    def test_duplicate_urls(self):
        with self.assertRaises(IntegrityError):
            DocumentURL.objects.create(paper=self.exam_paper2, document_type="mark_scheme",  url=self.url)


        
        
    
    



        
    
        