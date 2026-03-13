from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class ExamBoard(models.Model):
    name = models.CharField(max_length=200)

class Subject(models.Model):
    exam_board = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class OverallGradeBoundary(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_board = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(now().year)
        ]
    )
    grade = models.CharField(max_length=10)
    grade_threshold = models.IntegerField(validators=[ MinValueValidator(0)])

class GradeStatistic(models.Model):
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(now().year)
        ]
    )
    grade = models.CharField(max_length=10)
    percentage = models.DecimalField(
        max_digits=5,  
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    num_students = models.IntegerField(validators=[ MinValueValidator(0)])

class ComponentGradeBoundary(models.Model):
    paper_number = models.CharField(max_length=10)
    overall_grade_boundary = models.ForeignKey(OverallGradeBoundary, on_delete= models.CASCADE)
    grade = models.CharField(max_length=10)
    grade_threshold = models.IntegerField(validators=[ MinValueValidator(0)])

class DocumentURL(models.Model):
    DOCUMENT_TYPES = [("past_paper", "Past Paper"),
                      ("mark_scheme", "Mark Scheme"),
                      ("exam_report", "Exam Report")]
    paper = models.ForeignKey(ComponentGradeBoundary, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices = DOCUMENT_TYPES)
    url = models.URLField(max_length=500)