from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    priority = serializers.ChoiceField(choices=['low', 'medium', 'high'])
    completed = serializers.BooleanField(default=False)  # Если нужно
