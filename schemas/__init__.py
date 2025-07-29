
"""Data schemas for the multi-agent system"""

from pydantic import BaseModel
from typing import Dict, List, Optional

class BaseDataSchema(BaseModel):
    """Base schema for all data types"""
    id: str
    data_type: str
    content: str
    metadata: Optional[Dict] = None

class VideoData(BaseDataSchema):
    """Schema for video data"""
    data_type: str = "video"
    duration: Optional[float] = None
    resolution: Optional[str] = None

class AudioData(BaseDataSchema):
    """Schema for audio data"""
    data_type: str = "audio"
    duration: Optional[float] = None
    sample_rate: Optional[int] = None

class ImageData(BaseDataSchema):
    """Schema for image data"""
    data_type: str = "image"
    width: Optional[int] = None
    height: Optional[int] = None

class DocumentData(BaseDataSchema):
    """Schema for document data"""
    data_type: str = "document"
    page_count: Optional[int] = None
    format: Optional[str] = None

class TextData(BaseDataSchema):
    """Schema for text data"""
    data_type: str = "text"
    length: Optional[int] = None
    language: Optional[str] = None
