from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from pdf_app import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('docs/', views.doc_list, name='doc_list'),
    path('docs/update-view/', views.doc_list_update, name='doc_list_update'),
    path('docs/upload/', views.upload_doc, name='upload_doc'),
    path('docs/<int:pk>/', views.delete_doc, name='delete_doc'),
    path('docs/update/<int:pk>/', views.update_file_status, name='update_file_status'),
	path('docs/tableView/', views.StructuredView, name='StructuredView'),
    path('upload-csv/', views.csv_upload, name="csv_upload"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)