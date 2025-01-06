import random

# otp using pyotp
import pyotp



def send_otp(mobile, otp):
 """
 Send OTP via SMS.
 """
     # url = f"https://2factor.in/API/V1/{settings.SMS_API_KEY}/SMS/{mobile}/{otp}/Your OTP is"
     # payload = ""
     # headers = {'content-type': 'application/x-www-form-urlencoded'}
     # response = requests.get(url, data=payload, headers=headers)
     # print(response.content)
     # return bool(response.ok)
 pass



def generate_otp(duration=300):
    # Create a secret key (keep it secret!)̥
    secret_key = pyotp.random_base32()

    otp = pyotp.TOTP(secret_key, interval=duration)
    # Generate an OTP using TOTP after every 30 seconds
    print("Your TOTP is: ", otp.now())


    return (otp.now(), secret_key)





def verify_otp(user_otp, secret_key, duration=300):
    otp = pyotp.TOTP(secret_key, interval=duration)

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








