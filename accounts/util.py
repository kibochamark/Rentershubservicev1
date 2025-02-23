import random

import geocoder
# otp using pyotp
import pyotp
import os

import requests
from django.conf import settings


def send_otp(mobile, otp):
    """
    Send OTP via SMS.
    """
    url = "https://quicksms.advantasms.com/api/services/sendsms/"
    payload = {
        "apikey": settings.SMS_API_KEY,
        "partnerID": "4283",
        "message": f"Your OTP is {otp}",
        "shortcode": "RENTERS_HUB",
        "mobile": mobile
    }
    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)
    # print(response.content)
    return response.ok



def send_message(mobile, message):
    """
    Send message via SMS.
    """
    url = "https://quicksms.advantasms.com/api/services/sendsms/"
    payload = {
        "apikey": settings.SMS_API_KEY,
        "partnerID": "4283",
        "message": message,
        "shortcode": "RENTERS_HUB",
        "mobile": mobile
    }
    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)
    # print(response.content)
    return response.ok



def get_geocode(address):
    try:

        geo = geocoder.google(address ,key=settings.GOOGLE_API_KEY)
        print(geo, "geo")
        return (geo.status_code, {
            "lat" : geo.latlng[0],
            "lon" : geo.latlng[1]
        })
        # return bool(response.ok)
    except Exception as e:
        print(e)
        return (400, e)



def generate_otp(duration=300):
    # Create a secret key (keep it secret!)̥
    # secret_key = pyotp.random_base32()

    otp = pyotp.TOTP(os.environ.get("otp_secret"), interval=duration)
    # Generate an OTP using TOTP after every 30 seconds
    # print("Your TOTP is: ", otp.now())


    return otp.now()





def verify_otp(user_otp,  duration=300):
    otp = pyotp.TOTP(os.environ.get("otp_secret"), interval=duration)

    if otp.verify(user_otp):
        return  True


    return False


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }








