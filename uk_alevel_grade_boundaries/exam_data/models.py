from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class ExamBoard(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    exam_board = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    class Meta:
        indexes = [models.Index(fields=['exam_board', 'name'])]
        constraints = [models.UniqueConstraint(fields=['exam_board', 'name'], name='unique_subject')]

    def __str__(self):
        return f"{self.exam_board.name} {self.name}"
    
class ExamSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(now().year)
        ])
    
    class Meta:
        indexes = [models.Index(fields=['subject', 'year'])]
        constraints = [models.UniqueConstraint(fields=['subject', 'year'], name='unique_exam')]
    
    def __str__(self):
        return f"{self.subject} {self.year}"

class OverallGradeBoundary(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    grade_threshold = models.IntegerField(validators=[ MinValueValidator(0)])
    class Meta:
        indexes = [models.Index(fields=['exam_session'])]
        constraints = [models.UniqueConstraint(fields=['exam_session', 'grade'], name='unique_boundary')]

    def __str__(self):
        return f"{self.exam_session} {self.grade} : {self.grade_threshold}"


class GradeStatistic(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    percentage = models.DecimalField(
        max_digits=5,  
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    num_students = models.IntegerField(validators=[ MinValueValidator(0)])

    class Meta:
        indexes =  [models.Index(fields=['exam_session'])]
        constraints = [models.UniqueConstraint(fields=['exam_session', 'grade'], name='unique_statistic')]

    def __str__(self):
        return f"{self.exam_session} {self.grade} : {self.percentage}"
    
class ExamPaper(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    paper_number = models.CharField(max_length=10)

    class Meta:
        indexes =[models.Index(fields=['exam_session'])]
        constraints = [models.UniqueConstraint(fields=['exam_session','paper_number'], name = 'unique_paper')]
    
    def __str__(self):
        return f"{self.exam_session} paper:{self.paper_number}"

class ComponentGradeBoundary(models.Model):
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    grade_threshold = models.IntegerField(validators=[ MinValueValidator(0)])

    class Meta:
        indexes = [models.Index(fields=['exam_paper'])]
        constraints = [models.UniqueConstraint(fields=['exam_paper', 'grade'], name='unique_component_boundary')]

    def __str__(self):
        return f"{self.exam_paper} {self.grade} - {self.grade_threshold}"

class DocumentURL(models.Model):
    DOCUMENT_TYPES = [("past_paper", "Past Paper"),
                      ("mark_scheme", "Mark Scheme"),
                      ("exam_report", "Exam Report")]
    paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices = DOCUMENT_TYPES)
    url = models.URLField(max_length=500, unique=True)

    class Meta:
        indexes = [models.Index(fields=['paper', 'document_type'])]
        constraints = [models.UniqueConstraint(fields=['paper','document_type'], name='unique_doc')]

    def __str__(self):
        return f"{self.paper} {self.document_type}"