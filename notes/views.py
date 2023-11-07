from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note

class NoteView(APIView):
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Note added 😁')
        return Response('Failed to add note 🙁')

    def get(self, request, pk=None):
        if pk:
            data = Note.objects.get(id=pk)
            serializer = NoteSerializer(data)
        else: 
            data = Note.objects.all()
            serializer = NoteSerializer(data, many=True)
        return Response(serializer.data)
    
    def patch(self, request, pk=None):
        note_to_update = Note.objects.get(id=pk)
        serializer = NoteSerializer(instance=note_to_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Note updated successfully 😀')
        return Response('Could not update the Note...')
    
    def delete(self, request, pk=None):
        note_to_delete = Note.objects.get(id=pk)
        if note_to_delete.delete():
            return Response('Note deleted successfully 😀')
        return Response('Could not delete the Note...')