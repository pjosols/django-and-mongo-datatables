from pymongo import MongoClient


class MongoConnection(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['test-db']


class MongoCollection(MongoConnection):
    """A Generic Mongo Object class with common methods for querying MongoDB collections.

    """
    def __init__(self, collection):
        """
        :param collection:  The MongoDB collection to query against.
        """
        super(MongoCollection, self).__init__()
        self._collection = self.db[collection]

    def aggregate(self, match, group, limit=None):
        """Mongo aggregate

        :param match:
        :param group:
        :param limit:
        :return:
        """
        agg_ = [match, group]
        if limit:
            agg_.append(limit)
        return self._collection.aggregate(agg_)

    def choices(self, type_=str, **kwargs):
        """Returns all unique combinations of the 'value' and 'text' keys; used for populating form choices (for example
        drop down menus).

        :param type_: The type to return the values as; str by default.
        :param kwargs: Any keyword args, like {group: 'EngOps'}
        :return: all unique combinations of the 'value' and 'text' keys as list of tuples
        """
        filter_ = {}
        if kwargs:
            filter_.update(kwargs)
        data = self._collection.find(filter_)
        all_results = [(type_(d['val']), type_(d['text'])) for d in data]
        unique_results = set(all_results)
        return sorted(list(unique_results), key=lambda x: x[1])  # sorted by 2nd val [1] in tuple

    def count(self, filter_):
        """

        :param filter_:
        :return:
        """

        return self._collection.count(filter_)

    def delete_one(self, **kwargs):
        """Deletes one document

        :param kwargs: Any filter to limit the results of the distinct list
        :return: list of unique values in given key
        """
        return self._collection.delete_one(kwargs)

    def distinct(self, key, **kwargs):
        """Returns a list of all distinct values for a key, and allows querying by kwargs.

        :param key:  The Mongo collection key from which to return all unique values
        :param kwargs: Any filter to limit the results of the distinct list
        :return: list of unique values in given key
        """
        return self._collection.distinct(key, kwargs)

    def find(self, custom_filter=None, projection=None, limit=0, sort_key="_id", sort_dir=1):
        """Mongo find.  Find all docs, filtered by custom_filter, and exclude _id from the results.

        :param custom_filter: A dictionary with a custom filter.
        :param projection: A Mongo projection.
        :param limit: Optional limit
        :param sort_key: Optional sort key
        :param sort_dir: Optional sort order
        :return: Returns all documents matching filter_, as a list
        """
        filter_ = {}
        if custom_filter:
            filter_.update(custom_filter)

        return list(self._collection.find(filter_, projection).limit(limit).sort(sort_key, sort_dir))

    def find_one(self, filter_, projection=None):
        """Mongo findOne

        :param filter_:
        :param projection:
        :return:  Return dictionary
        """

        return self._collection.find_one(filter_, projection)

    def find_one_and_update(self, filter_, update_, options_=None, **kwargs):
        """

        :param filter_:
        :param update_:
        :param options_:
        :return:
        """

        return self._collection.find_one_and_update(filter_, update_, options_, **kwargs)

    def insert(self, data):
        """

        :param data: dictionary/object to be inserted as Mongo document
        :return: Mongo _id as string
        """
        return self._collection.insert(data)

    def insert_one(self, document):
        """

        :return:
        """

        return self._collection.insert_one(document)

    def remove(self, custom_filter=None):
        """Remove Mongo document by _id

        :return:
        """
        filter_ = {}
        if custom_filter:
            filter_.update(custom_filter)
        return self._collection.remove(filter_)

    def update_many(self, query_, update_):
        """

        :param query_:
        :param update_:
        :param upsert_:
        :return:
        """

        return self._collection.update_many(query_, update_)

    def update_one(self, query_, update_, upsert_=False):
        """

        :param query_:
        :param update_:
        :param upsert_:
        :return:
        """

        return self._collection.update_one(query_, update_, upsert=upsert_)
