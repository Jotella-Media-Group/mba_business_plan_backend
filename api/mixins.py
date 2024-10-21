from typing import Sequence
from typing import Type

from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
        SessionAuthentication,
    ]

    permission_classes = [IsAuthenticated]
