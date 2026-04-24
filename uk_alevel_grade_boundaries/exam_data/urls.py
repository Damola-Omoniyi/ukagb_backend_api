from django.urls import path
from exam_data import views

urlpatterns = [
    path("exam-boards/", views.ExamBoardList.as_view(), name="exam-board-list"),
    path("<str:exam_board_name>/subjects/", views.SubjectList.as_view(), name="subject-list"),
    path("<str:exam_board_name>/<str:subject_name>/GradeBoundaries/", views.GradeBoundaryList.as_view(), name="grade-boundaries-list"),
    path("<str:exam_board_name>/<str:subject_name>/<int:year>/statistics/", views.GradeStatisticList.as_view(), name = "grade-statistic-list"),
    path("<str:exam_board_name>/<str:subject_name>/<int:year>/", views.ComponentGradeList.as_view(), name="component-grade-list"),
    path("<str:exam_board_name>/<str:subject_name>/<int:year>/<str:paper_number>/", views.DocumentURLList.as_view(), name="url-list")
]

