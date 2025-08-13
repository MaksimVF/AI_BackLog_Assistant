


"""
Input Validation and Sanitization Utilities
"""

import re
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ValidationError as PydanticValidationError, validator, Field, constr
from utils.error_handling import ValidationError as AIValidationError

class SanitizedString(str):
    """String type that sanitizes HTML and other potentially dangerous content"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise TypeError('Must be a string')

        # Basic HTML sanitization
        sanitized = re.sub(r'<[^>]*>', '', value)
        return sanitized

class DocumentId(str):
    """Validated document ID format"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise TypeError('Must be a string')

        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', value):
            raise ValueError('Invalid document ID format')

        return value

class APIRequestModel(BaseModel):
    """Base model for API request validation"""

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            SanitizedString: str,
            DocumentId: str
        }

class DocumentProcessingRequest(APIRequestModel):
    """Request model for document processing"""

    document_id: DocumentId
    content: SanitizedString
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    source: Optional[constr(max_length=50)] = 'user_upload'

    @validator('metadata')
    def validate_metadata(cls, value):
        if not isinstance(value, dict):
            raise ValueError('Metadata must be a dictionary')
        # Additional metadata validation can be added here
        return value

class UserInputRequest(APIRequestModel):
    """Request model for user text input"""

    user_input: SanitizedString = Field(..., min_length=1, max_length=10000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    session_id: Optional[DocumentId] = None

class InputValidator:
    """Utility class for input validation and sanitization"""

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input to prevent XSS and injection attacks"""
        if not text:
            return text

        # Remove HTML tags
        sanitized = re.sub(r'<[^>]*>', '', text)
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[\0\b\t\n\r\x0b\x0c]', '', sanitized)
        return sanitized.strip()

    @staticmethod
    def validate_document_id(doc_id: str) -> str:
        """Validate document ID format"""
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', doc_id):
            raise AIValidationError(
                f"Invalid document ID format: {doc_id}",
                field="document_id",
                context={"invalid_id": doc_id}
            )
        return doc_id

    @staticmethod
    def validate_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metadata structure"""
        if not isinstance(metadata, dict):
            raise AIValidationError(
                "Metadata must be a dictionary",
                field="metadata"
            )

        # Check for suspicious keys
        suspicious_keys = ['__proto__', 'constructor', 'prototype']
        for key in metadata.keys():
            if key in suspicious_keys:
                raise AIValidationError(
                    f"Invalid metadata key: {key}",
                    field="metadata",
                    context={"invalid_key": key}
                )

        return metadata

    @staticmethod
    def validate_and_sanitize_request(
        request_data: Dict[str, Any],
        expected_fields: List[str]
    ) -> Dict[str, Any]:
        """
        Validate and sanitize a complete API request

        Args:
            request_data: Raw request data
            expected_fields: List of expected field names

        Returns:
            Validated and sanitized data

        Raises:
            AIValidationError: If validation fails
        """
        if not isinstance(request_data, dict):
            raise AIValidationError("Request must be a dictionary")

        # Check for required fields
        missing_fields = [field for field in expected_fields if field not in request_data]
        if missing_fields:
            raise AIValidationError(
                f"Missing required fields: {', '.join(missing_fields)}",
                field="request",
                context={"missing_fields": missing_fields}
            )

        # Sanitize all string fields
        sanitized_data = {}
        for key, value in request_data.items():
            if isinstance(value, str):
                sanitized_data[key] = InputValidator.sanitize_text(value)
            elif isinstance(value, dict):
                sanitized_data[key] = InputValidator.validate_metadata(value)
            else:
                sanitized_data[key] = value

        return sanitized_data

def validate_pydantic_model(model_class: type(BaseModel), data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate data against a Pydantic model and return validated data

    Args:
        model_class: Pydantic model class to validate against
        data: Input data to validate

    Returns:
        Validated data as dictionary

    Raises:
        AIValidationError: If validation fails
    """
    try:
        model_instance = model_class(**data)
        return model_instance.dict()
    except PydanticValidationError as e:
        error_details = []
        for error in e.errors():
            field = error['loc'][0] if error['loc'] else 'request'
            error_details.append({
                'field': field,
                'message': error['msg'],
                'input': error.get('input', None)
            })

        raise AIValidationError(
            "Validation failed",
            field="request",
            context={"errors": error_details}
        )

def sanitize_dict(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively sanitize all string values in a dictionary

    Args:
        input_dict: Dictionary to sanitize

    Returns:
        Sanitized dictionary
    """
    if not isinstance(input_dict, dict):
        return input_dict

    sanitized = {}
    for key, value in input_dict.items():
        if isinstance(value, str):
            sanitized[key] = InputValidator.sanitize_text(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_dict(item) if isinstance(item, dict) else item for item in value]
        else:
            sanitized[key] = value

    return sanitized

def sanitize_list(input_list: List[Any]) -> List[Any]:
    """
    Sanitize all string values in a list

    Args:
        input_list: List to sanitize

    Returns:
        Sanitized list
    """
    if not isinstance(input_list, list):
        return input_list

    return [
        sanitize_dict(item) if isinstance(item, dict) else
        InputValidator.sanitize_text(item) if isinstance(item, str) else
        item
        for item in input_list
    ]

