from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.http import StreamingHttpResponse, JsonResponse
from profiles.models.business_profile import BusinessProfile
from profiles.services.business_profile import profile_assistant_response
from competitors.services.serper import get_competitors_from_serper
from profiles.utils.timing_utils import timeit
from profiles.mockdata.fake_profile import FAKE_PROFILE
import time

@api_view(['POST'])
@permission_classes([AllowAny])
@timeit("Profile Assistant Stream")
def profile_assistant_stream(request):
    question = request.data.get("question", "")
    profile = BusinessProfile(**FAKE_PROFILE)
    def stream():
        last_heartbeat = time.time()
        for chunk in profile_assistant_response(question, profile):
            yield chunk
            # Heartbeat every 2 seconds if no chunk is sent
            now = time.time()
            if now - last_heartbeat > 2:
                yield " "  # send a space as heartbeat
                last_heartbeat = now
        # Final heartbeat to ensure flush
        yield " "
    return StreamingHttpResponse(stream(), content_type="text/event-stream")
