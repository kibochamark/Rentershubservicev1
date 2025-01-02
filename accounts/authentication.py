from rest_framework.authentication import  TokenAuthentication as BaseAuth



class TokenAuthentication(BaseAuth):
    keyword='Token'