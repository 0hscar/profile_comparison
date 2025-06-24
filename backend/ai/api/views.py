from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.http import StreamingHttpResponse
from profiles.models.business_profile import BusinessProfile
from profiles.services.business_profile import profile_assistant_response
from competitors.services.serper import get_competitors_from_serper
from profiles.utils.timing_utils import timeit
from profiles.mockdata.fake_profile import FAKE_PROFILE

@api_view(['POST'])
@permission_classes([AllowAny])
@timeit("Profile Assistant Stream")
def profile_assistant_stream(request):
    question = request.data.get("question", "")
    profile = BusinessProfile(**FAKE_PROFILE)
    def stream():
        for chunk in profile_assistant_response(question, profile):
            yield chunk
    return StreamingHttpResponse(stream(), content_type="text/plain")
