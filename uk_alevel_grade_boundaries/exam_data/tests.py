from django.test import TestCase
from .models import ExamBoard, Subject, OverallGradeBoundary, GradeStatistic, ComponentGradeBoundary, DocumentURL
from django.utils.timezone import now

class ExamBoardTestCase(TestCase):
    def setUp(self):
        ExamBoard.objects.create(name="AQA")
        ExamBoard.objects.create(name="Edexcel")
        ExamBoard.objects.create(name="OCR")
    
    def test_exam_board_names(self):
        boards = ExamBoard.objects.all()
        names = [b.name for b in boards]
        expected_names = ["AQA", "Edexcel", "OCR"]
        self.assertCountEqual(names, expected_names)  
    
class SimpleModelTests(TestCase):
    def setUp(self):
        # Create an ExamBoard
        self.aqa = ExamBoard.objects.create(name="AQA")
        
        # Create a Subject
        self.maths = Subject.objects.create(exam_board=self.aqa, name="Mathematics")
        
        # OverallGradeBoundary
        self.overall = OverallGradeBoundary.objects.create(
            subject=self.maths,
            exam_board=self.aqa,
            year=2025,
            grade="A",
            grade_threshold=85
        )
        
        # GradeStatistic
        self.stat = GradeStatistic.objects.create(
            year=2025,
            grade="A",
            percentage=23.5,
            num_students=120
        )
        
        # ComponentGradeBoundary
        self.component = ComponentGradeBoundary.objects.create(
            paper_number="1",
            overall_grade_boundary=self.overall,
            grade="A",
            grade_threshold=43
        )
        
        # DocumentURL
        self.doc = DocumentURL.objects.create(
            paper=self.component,
            document_type="past_paper",
            url="https://example.com/paper.pdf"
        )
    
    def test_models_created(self):
        # Check objects exist
        self.assertEqual(ExamBoard.objects.count(), 1)
        self.assertEqual(Subject.objects.count(), 1)
        self.assertEqual(OverallGradeBoundary.objects.count(), 1)
        self.assertEqual(GradeStatistic.objects.count(), 1)
        self.assertEqual(ComponentGradeBoundary.objects.count(), 1)
        self.assertEqual(DocumentURL.objects.count(), 1)
        
        # Optional: check some field values
        self.assertEqual(self.aqa.name, "AQA")
        self.assertEqual(self.maths.name, "Mathematics")
        self.assertEqual(self.overall.grade_threshold, 85)
        self.assertEqual(self.stat.percentage, 23.5)
        self.assertEqual(self.component.paper_number, "1")
        self.assertEqual(self.doc.document_type, "past_paper")
