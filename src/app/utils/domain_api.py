import os

def get_domain_api():
    if os.getenv("APP_ENV") == "production":
        return os.getenv("DOMAIN_PROD")
    elif os.getenv("APP_ENV") == "testing":
        return os.getenv("DOMAIN_TEST")
    else:
        return os.getenv("DOMAIN_LOCAL")