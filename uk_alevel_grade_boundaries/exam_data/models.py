from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class ExamBoard(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    exam_board = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        indexes = [models.Index(fields=['exam_board'])]

    def __str__(self):
        return f"{self.exam_board} {self.name}"

class OverallGradeBoundary(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(now().year)
        ])
    grade = models.CharField(max_length=10)
    grade_threshold = models.IntegerField(validators=[ MinValueValidator(0)])
    
    class Meta:
        indexes = [models.Index(fields=['subject','year'])]
        constraints = [models.UniqueConstraint(fields=['subject', 'year', 'grade'], name='unique_boundary')]

    def __str__(self):
        return f"{self.subject}  {self.year} {self.grade} : {self.grade_threshold}"

class GradeStatistic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
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

    class Meta:
        indexes =  [models.Index(fields=['subject', 'year'])]
        constraints = [models.UniqueConstraint(fields=['subject', 'year', 'grade'], name='unique_statistic')]


    def __str__(self):
        return f"{self.subject}  {self.year} {self.grade} : {self.percentage}"

class ComponentGradeBoundary(models.Model):
    paper_number = models.CharField(max_length=10)
    overall_grade_boundary = models.ForeignKey(OverallGradeBoundary, on_delete= models.CASCADE)
    grade = models.CharField(max_length=10)
    grade_threshold = models.IntegerField(validators=[ MinValueValidator(0)])

    class Meta:
        indexes = [models.Index(fields=['overall_grade_boundary','paper_number'])]
        constraints = [models.UniqueConstraint(fields=['overall_grade_boundary','paper_number', 'grade'], name='unique_component_boundary')]

    def __str__(self):
        return f"{self.overall_grade_boundary.subject} {self.overall_grade_boundary.year} paper {self.paper_number} {self.grade} : {self.grade_threshold}"

class DocumentURL(models.Model):
    DOCUMENT_TYPES = [("past_paper", "Past Paper"),
                      ("mark_scheme", "Mark Scheme"),
                      ("exam_report", "Exam Report")]
    paper = models.ForeignKey(ComponentGradeBoundary, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices = DOCUMENT_TYPES)
    url = models.URLField(max_length=500)

    class Meta:
        indexes = [models.Index(fields=['paper', 'document_type'])]

    def __str__(self):
        return f"{self.paper} {self.document_type}"