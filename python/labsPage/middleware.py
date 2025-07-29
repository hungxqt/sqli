"""
Custom middleware for iframe embedding control
"""

class IframeEmbeddingMiddleware:
    """
    Custom middleware to control iframe embedding behavior
    Provides more flexibility than Django's default XFrameOptionsMiddleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Remove any existing X-Frame-Options header
        if 'X-Frame-Options' in response:
            del response['X-Frame-Options']
        
        # Add Content Security Policy header for iframe control
        # This allows embedding from any origin (for educational purposes)
        response['Content-Security-Policy'] = "frame-ancestors *;"
        
        # Optional: Add specific domains only
        # response['Content-Security-Policy'] = "frame-ancestors 'self' https://trusted-domain.com;"
        
        return response
