"""Middlewares"""

# Django
from django.shortcuts import redirect, reverse

# URLs
UPDATE_PROFILE = 'users:update'
LOGOUT = 'users:logout'

class ProfileCompletionMiddleware:
    """Profile completion middleware
    
    Ensure every user that is interactig with the platform
    have their profile picture and biography
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """code to be executed for each request before the vies is called"""
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user.profile
                
                if not profile.picture or not profile.biography:
                    if request.path not in [reverse(UPDATE_PROFILE), reverse(LOGOUT)] :
                        return redirect(UPDATE_PROFILE)

        response = self.get_response(request)
        return response
