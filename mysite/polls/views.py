import json

from django.http import JsonResponse
from django.shortcuts import render
from django.http import Http404

from mongo_datatables import DataTables, Editor

from .models import MongoCollection, MongoConnection


def index(request):
    return render(request, 'polls/index.html')


def test1(request):

    collection = "col1"
    test_docs = MongoCollection(collection).find()

    return render(request, 'polls/test1.html', {'test_docs': test_docs, 'collection': collection})




def db(request, collection):
    """Used by yoursite.com/collection, where collection is the MongoDB collection you want to display.  This view in
    combination with the jQuery in db.html will render any collection as a table, regardless of the keys in each
    document, but it might be overly memory intensive for tens of thousands of documents.

    :param request:
    :param collection:
    :return:
    """

    col_obj = MongoCollection(collection)
    if not col_obj.count({}):
        raise Http404("Collection does not exist")

    # get every possible key from every document in the collection.
    keys = []
    for each in col_obj.find({}, {'_id': 0}):
        for key in each:
            if key not in keys:
                keys.append(key)

    return render(request, 'polls/db.html', {'collection': collection, 'keys': keys})


def datatables(request, collection):
    """Used by the DataTables AJAX to load the data.

    :param request:
    :param collection:
    :return:
    """

    request_args = json.loads(request.POST.get("args"))
    mongo = MongoConnection()

    data = DataTables(mongo, collection, request_args).get_rows()

    return JsonResponse(data)


def editor(request, collection, doc_id):
    """Used by the DataTables Editor to modify the data.

    :param request:
    :param collection:
    :param doc_id:
    :return:
    """

    request_args = json.loads(request.POST.get("args"))
    mongo = MongoConnection()

    data = Editor(mongo, collection, request_args, doc_id).update_rows()

    return JsonResponse(data)
