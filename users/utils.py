from datetime import timedelta
from django.utils import timezone
from salaryDisbursments.settings import SECRET_KEY
import jwt

def token_generator(user):
    exp = timezone.now() + timedelta(hours=1)
    payload = {
        'exp': exp,
        'email': user.email,
        'contract': user.contract_number,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'company': user.company_id,
        'user': user.user_type,
        'id': user.id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def refresh_token_generator(user):
    exp = timezone.now() + timedelta(days=7)
    payload = {
        'exp': exp,
        'email': user.email,
        'contract': user.contract_number,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'company': user.company_id,
        'user': user.user_type,
        'id': user.id,
        'iat': timezone.now(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token