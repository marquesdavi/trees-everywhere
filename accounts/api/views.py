import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from ..models import Account
from .serializers import AccountSerializer

logger = logging.getLogger(__name__)


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filter_by = self.request.query_params.get("filter_by")

        logger.debug(f"Getting queryset for user {user}, filter_by={filter_by}")

        if filter_by == "created":
            queryset = Account.objects.filter(created_by=user).order_by("name")
        else:
            queryset = Account.objects.filter(users=user).order_by("name")

        logger.info(f"Queryset for user {user}: {queryset}")
        return queryset

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
            logger.warning(f"Account with id {self.kwargs['pk']} not found.")
            raise NotFound("Account not found.")

    def perform_create(self, serializer):
        account = serializer.save(created_by=self.request.user)
        account.users.add(self.request.user)
        logger.info(f"Account created by {self.request.user}: {account}")

    def perform_update(self, serializer):
        account = self.get_object()
        serializer.save()
        logger.info(f"Account updated by {self.request.user}: {account}")

    def perform_destroy(self, instance):
        account = self.get_object()
        account.delete()
        logger.info(f"Account deleted by {self.request.user}: {account}")

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            logger.error(f"Validation error: {exc}")
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(exc, PermissionDenied):
            logger.error(f"Permission denied: {exc}")
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            logger.error(f"Not found: {exc}")
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        logger.error(f"Unhandled exception: {exc}")
        return super().handle_exception(exc)
