import time
import django
from django.utils import simplejson
from django.core.serializers import json
from tastypie.serializers import Serializer

class CustomJSONSerializer(Serializer):
    def to_json(self, data, options=None):
        """
        Given some Python data, produces JSON output.
        """
        options = options or {}
        data = self.to_simple(data, options)

        if django.get_version() >= '1.5':
            return json.json.dumps(data, cls=json.DjangoJSONEncoder, sort_keys=True, ensure_ascii=False)
        else:
            return simplejson.dumps(data, cls=json.DjangoJSONEncoder, sort_keys=True, ensure_ascii=False)

    def from_json(self, content):
        """
        Given some JSON data, returns a Python dictionary of the decoded data.
        """
        return simplejson.loads(content)