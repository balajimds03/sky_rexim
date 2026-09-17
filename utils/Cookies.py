def set_secure_cookies(response,key,value,max_age=None):
    response.set_cookie(key=key,value=value,secure=True,samesite=None,max_age=max_age)