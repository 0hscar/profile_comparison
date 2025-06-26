from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from profiles.models.business_profile import BusinessProfile
from profiles.mockdata.fake_profile import FAKE_PROFILE


class BusinessProfileView(APIView):
    """
    Retrieval of a fake business profile (Swapped for real for production).
    """
    permission_classes = [AllowAny]
    def get(self, request):
        return Response(FAKE_PROFILE)
