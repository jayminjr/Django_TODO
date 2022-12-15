from rest_framework.response import Response
from todoapp.api.serializers import TodoSerializer
from todoapp.models import Todo
from rest_framework import status
from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


class TodoAPIView(APIView):
    """
    A APIView to perform CRUD operation on todo table
    """

    def get_object(self, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            if todo.user == self.request.user:
                return todo
            else:
                raise Http404
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
            serializer = TodoSerializer(data)
        else:
            data = Todo.objects.filter(user=self.request.user).order_by("-created_at")
            serializer = TodoSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = TodoSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=self.request.user)

        return Response(
            {
                "message": "Todo Created Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, pk=None, format=None):
        todo_to_update = self.get_object(pk)
        serializer = TodoSerializer(
            instance=todo_to_update, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Todo Updated Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk, format=None):
        todo_to_delete = self.get_object(pk)

        todo_to_delete.delete()

        return Response(
            {"message": "Todo Deleted Successfully"}, status=status.HTTP_200_OK
        )
