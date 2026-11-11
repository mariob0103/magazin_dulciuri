class MiddlewareNou:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self,request):
        req_headers = request.META
        str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if str_lista_ip:
            ip = str_lista_ip.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.ip_client = ip
        response = self.get_response(request)
        return response
    