# utils/user_info_handler.py

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
    return UserInfo.objects.create(
        name=metadata.get("name"),
        phone_number=metadata.get("phone_number"),
        email=metadata.get("email"),
        pincode=metadata.get("pincode"),
        type=metadata.get("type"),
        description=metadata.get("description"),
        source=source
    )
