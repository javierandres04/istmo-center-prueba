from rest_framework.exceptions import NotFound

# Generic class to manage CRUD operations in services
class BaseCrudService:
    model = None
    serializer_class = None

    @classmethod
    def create(cls, data):
        serializer = cls.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @classmethod
    def get_all(cls):
        return cls.model.objects.all().order_by('id')

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.model.objects.get(id=id)
        except cls.model.DoesNotExist:
            raise NotFound(f"{cls.model.__name__.lower()} not found.")

    @classmethod
    def update(cls, id, data, partial=False):
        instance = cls.get_by_id(id)
        serializer = cls.serializer_class(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @classmethod
    def delete(cls, id):
        instance = cls.get_by_id(id)
        instance.delete()
        return instance