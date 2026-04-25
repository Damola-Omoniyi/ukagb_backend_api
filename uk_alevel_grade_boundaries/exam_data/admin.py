from django.contrib import admin
from exam_data.models import (ExamBoard, Subject, ExamSession, OverallGradeBoundary, GradeStatistic, ExamPaper, 
                              ComponentGradeBoundary, DocumentURL)

admin.site.register(ExamBoard)
admin.site.register(Subject)
admin.site.register(ExamSession)
admin.site.register(OverallGradeBoundary)
admin.site.register(GradeStatistic)
admin.site.register(ExamPaper)
admin.site.register(ComponentGradeBoundary)
admin.site.register(DocumentURL)
