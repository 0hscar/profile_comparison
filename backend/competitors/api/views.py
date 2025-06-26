from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Import the BusinessProfile and get_competitors_from_serper from the correct services location
from profiles.models.business_profile import BusinessProfile
from competitors.services.serper import get_competitors_from_serper
from profiles.mockdata.fake_profile import FAKE_PROFILE

@api_view(['GET'])
@permission_classes([AllowAny])
def get_competitors(request):
    """
    Returns competitors as a JSON array.
    """
    try:
        profile = BusinessProfile(**FAKE_PROFILE)
        max_results = int(request.query_params.get("max_results", 5))
        nearby = list(get_competitors_from_serper(profile, mode="nearby", max_results=max_results))
        similar = list(get_competitors_from_serper(profile, mode="similar", max_results=max_results))
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({
        "nearby": nearby,
        "similar": similar
    })
