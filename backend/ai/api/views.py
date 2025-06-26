from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.http import StreamingHttpResponse, JsonResponse
from profiles.models.business_profile import BusinessProfile
from profiles.services.business_profile import profile_assistant_response
from competitors.services.serper import get_competitors_from_serper
from core.timing_utils import timeit
from profiles.mockdata.fake_profile import FAKE_PROFILE
import time

@api_view(['POST'])
@permission_classes([AllowAny])
@timeit("Profile Assistant Stream")
def profile_assistant_stream(request):
    question = request.data.get("question", "")
    model = request.data.get("model", "gpt-4.1-mini")
    profile = BusinessProfile(**FAKE_PROFILE)
    if not question:
        return JsonResponse({"error": "Missing 'question' in request."}, status=400)
    if not model:
        return JsonResponse({"error": "Missing 'model' in request."}, status=400)
    if not profile:
        return JsonResponse({"error": "Profile could not be loaded."}, status=500)



    def stream():
        try:
            last_heartbeat = time.time()
            for chunk in profile_assistant_response(question, profile, model=model):
                yield chunk
                now = time.time()
                if now - last_heartbeat > 2:
                    yield " "
                    last_heartbeat = now
            yield " "
        except Exception:
            yield "Issue with AI response"
    return StreamingHttpResponse(stream(), content_type="text/event-stream")
