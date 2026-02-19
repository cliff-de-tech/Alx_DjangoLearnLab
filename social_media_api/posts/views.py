from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.response import Response

from notifications.models import Notification
from .models import Comment, Like, Post
from .serializers import CommentSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """CRUD for posts with filtering and search."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD for comments."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Notify post author if commenter is a different user
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=comment.post,
            )


class FeedView(generics.ListAPIView):
    """Return posts from users the current user follows, ordered by most recent."""

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikePostView(generics.GenericAPIView):
    """Like a post."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {'message': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Notify the post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post,
            )
        return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    """Unlike a post."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response(
                {'message': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        like.delete()
        return Response({'message': 'Post unliked.'}, status=status.HTTP_200_OK)
