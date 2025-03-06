import base64
import random

from django.shortcuts import get_object_or_404
import geocoder
# otp using pyotp
from django.utils import timezone


import requests
from django.conf import settings
import secrets
import string
import bcrypt
import datetime
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from accounts.models import Otp


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
    print(response.content)
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

# otp = pyotp.TOTP(os.environ.get("otp_secret"), interval=300)

# def generate_otp(duration=300):
#     # Create a secret key (keep it secret!)̥
#     # secret_key = pyotp.random_base32()


#     # Generate an OTP using TOTP after every 30 seconds
#     # print("Your TOTP is: ", otp.now())


#     return otp.now()





# def verify_otp(user_otp,  duration=300):
   

#     if otp.verify(user_otp):
#         return  True


#     return False


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }








# Assuming you have a database and a way to store/retrieve OTPs
# (replace with your actual database logic)
salt_bytes = bcrypt.gensalt()
def generate_otp(length=6, contact=""):
    """Generates a cryptographically secure OTP."""
    alphabet = string.digits
    otp = ''.join(secrets.choice(alphabet) for i in range(length))
    try:
        store_otp(contact, otp)
        return (200, otp)
    except Exception as e:
        return (400, e)

# def hash_otp(otp):
#     """Hashes an OTP using bcrypt."""
#     salt = bcrypt.gensalt()
#     hashed_otp = bcrypt.hashpw(otp.encode('utf-8'), salt)
#     return hashed_otp, salt

def store_otp(contact, otp, expiration_minutes=5):
    """Stores a hashed OTP in the database."""
    
    hashed_otp = make_password(otp)

    expiration = datetime.datetime.now() + timedelta(minutes=expiration_minutes)
     #Encode hashed_otp

    otp_data = {
        'contact': contact,
        'secret': hashed_otp, #Store the base64 encoded hashed_otp
        'expiration': expiration,
    }

    try:
        
        if Otp.objects.filter(contact=contact).exists():
            print("true")
            existing_otp = Otp.objects.filter(contact=contact).first()
            existing_otp.delete()
           
        new_otp = Otp.objects.create(
            contact=otp_data["contact"],
            secret=otp_data['secret'],
            expiration=otp_data["expiration"]
        )
        new_otp.save()
        return (200, new_otp)
    except Exception as error:
        return (400, error)

    

def verify_otp(contact, user_entered_otp):
    """Verifies a user-entered OTP."""
    # Retrieve the stored OTP and expiration from the database
    # Example:
    otp_data = get_object_or_404(Otp, contact=contact) 
    # print(otp_data, "otp")
    if otp_data is None:
        return False # no otp found for that user.
    stored_hashed_otp = otp_data.secret
    expiration = otp_data.expiration

    # print(timezone.now() > expiration)

    # Check expiration
    if timezone.now() > expiration:
        # print("true")
        #otp has expired.
        return False
    
    if otp_data:


        # print("reached",otp_data.secret)
    # Hash the user-entered OTP and compare
  
        # print(check_password(user_entered_otp, otp_data.secret))
    
        if check_password(user_entered_otp, otp_data.secret):
            # print("reached")
            # OTP is valid
            # Invalidate the OTP (delete from database)
            # Your database logic to delete the otp.
            return True
    
    return False



