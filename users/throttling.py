from rest_framework.throttling import SimpleRateThrottle

class RegisterRateThrottle(SimpleRateThrottle):
    rate = '5/hour'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            ip = self.get_ident(request)
            return f"register_ip_{ip}"
        return None
