from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, viewsets
from rest_framework.permissions import IsAuthenticated

from comments.serializers import CommentSerializer, CreateCommentSerializer, CreatePostSerializer, PostSerializer
from .models import Comment, Post, Rate


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCommentSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Comment.objects.all()


class AddRatingAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        user = request.user
        comment = get_object_or_404(Comment, id=comment_id)

        if Rate.objects.filter(user=user, comment=comment).exists():
            return Response({'error': 'Вы уже оценили данный комментарий'}, status=status.HTTP_400_BAD_REQUEST)

        rating_value = int(request.data.get('rating', 0))
        if not rating_value or rating_value not in [-1, 1]:
            return Response({'error': 'неправильная оценка'}, status=status.HTTP_400_BAD_REQUEST)

        rate = Rate(user=user, comment=comment, value=rating_value)
        rate.save()

        return Response({'success': 'Комментарий оценен'}, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostSerializer
        return PostSerializer
