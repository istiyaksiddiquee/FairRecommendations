from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime 

class AuthenticatedServiceClient:
    
    def __init__(self, allowed):
        self.allowed = allowed

    def is_authenticated(self):
        return self.allowed

class JwtServiceOnlyAuthentication(JSONWebTokenAuthentication):

    allowed_uuid_list = [
        'b12408f0-d239-49cb-8098-c88f76fad069',
        '8aedce54-865b-4394-97d1-77901d660154',
        '447f95fe-82f7-41dc-af1c-4a97ed38eb39',
        '69e3f4be-51a7-4478-a18f-bb9b3539174f',
        '7e330164-7e65-4724-802f-05b3be976443',
        'bad56e77-958f-43a9-8f13-8d8975b23afa',
        'dbe847ea-871b-4815-9216-d6826bba5681',
        'f0388aa0-2a89-4e94-baed-01b4bfa53acd',
        'd52867f2-4d04-4c07-93a0-f0c467d3c17d',
        '74ffb31c-6077-49ee-a7d0-6f06610fd2bc',
        '03b3ec7e-4c82-4c6d-bfb6-956f2619d196',
        '2bb20195-1bef-449f-8e19-b3d10e5da4cc',
        'a4e809b3-026c-4c72-97f1-123c512a6a94',
        'a599b010-6728-405a-814c-9b228638496f',
        'c1996a00-92a5-40ff-9c26-b79dabb2538f',
        '37bd075f-04cc-469a-8f48-ad5709327476',
        'e1f7cd60-6519-4214-af71-87444b1b7391'
    ]


    def authenticate_credentials(self, payload):
        # Assign properties from payload to the AuthenticatedServiceClient object if necessary
        allowed = True
        current_timestamp = datetime.now().timestamp()

        if payload['uuid'] not in self.allowed_uuid_list:
            raise AuthenticationFailed("Authentication Failed. Please Contact Admin", 401)
        elif payload['token_expiry'] - current_timestamp < 0:            
            raise AuthenticationFailed("Authentication Failed. Please Contact Admin", 401)

        return AuthenticatedServiceClient(allowed)
