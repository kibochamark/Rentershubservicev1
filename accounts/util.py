import random


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



def generate_otp():

    otp= random.randint(1000, 9999)

    return otp


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }