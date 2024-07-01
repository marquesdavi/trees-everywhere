from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from ..models import Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filter_by = self.request.query_params.get("filter_by")

        if filter_by == "created":
            return Account.objects.filter(created_by=user).order_by("name")

        return Account.objects.filter(users=user).order_by("name")

    def get_object(self):
        try:
            obj = Account.objects.get(pk=self.kwargs["pk"])

            if (
                obj.created_by != self.request.user
                and self.request.user not in obj.users.all()
            ):
                raise PermissionDenied(
                    "You do not have permission to access this account."
                )
            return obj
        except Account.DoesNotExist:
            raise NotFound("Account not found.")

    def perform_create(self, serializer):
        account = serializer.save(created_by=self.request.user)
        account.users.add(self.request.user)

    def perform_update(self, serializer):
        self.get_object()
        serializer.save()

    def perform_destroy(self, instance):
        self.get_object()
        instance.delete()

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(exc, PermissionDenied):
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
