from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    # The index page
    path('', views.index, name='index'),

    # test page for problem 1
    path('test1/', views.test1, name='test1'),

    # used by yoursite.com/collection, where collection is the MongoDB collection you want to view
    path('<slug:collection>/', views.db, name='db'),

    # used by the DataTables AJAX to load the data
    path('datatables/<slug:collection>', views.datatables, name='datatables'),

    # used by the DataTables AJAX to edit the data
    path('editor/<slug:collection>/<doc_id>', views.editor, name='editor'),

]
