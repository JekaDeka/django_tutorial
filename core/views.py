from rest_framework import viewsets


class ActionSerializedViewSet(viewsets.ModelViewSet):
    """
    provides custom serializer for specific viewset action
    declate serilizer in dict:
    action_serializers = {
        'list': ReportListSerializer,
        'retrieve': ReportPostPutSerializer,
        'create': ReportPostPutSerializer,
        'update': ReportPostPutSerializer,
        'partial_update': ReportPostPutSerializer,
    }
    """
    action_serializers = {}

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return self.serializer_class
