# utils/user_info_handler.py

import re
from rest_framework.exceptions import ValidationError

from .models import UserInfo


def validate_request_data(data, required_fields):
    user_info_data = data.get("user_info")
    if not user_info_data:
        raise ValidationError("user_info is required.")

    metadata = user_info_data.get("metadata")
    if not isinstance(metadata, dict):
        raise ValidationError("metadata must be a valid JSON object.")

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}.")

    return metadata



def create_user_info(metadata, source):
    name = metadata.get('name',"").strip()
    phone_number = metadata.get('phone_number',"").strip()
    email = metadata.get('email',"").strip()
    pincode = metadata.get('pincode',"").strip()


    if not re.match(r'^[6-9]\d{9}$', phone_number):
            raise ValidationError("Mobile number must be 10 digits and start with 6, 7, 8, or 9.")
    

    if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
            raise ValidationError("Only valid Gmail addresses with a name before @gmail.com are allowed.")

    if not (pincode.isdigit() and len(pincode) == 6):
            raise ValidationError("The pin code should be exactly 6 digits.")
    
    return UserInfo.objects.create(
        name=name,
        phone_number=phone_number,
        email=email,
        pincode=pincode,
        type=metadata.get("type"),
        description=metadata.get("description"),
        source=source
    )
