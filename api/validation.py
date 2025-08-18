


























from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: str = Field(..., regex="^(open|in_progress|completed|closed)$")
    priority: int = Field(..., ge=1, le=5)
    due_date: Optional[datetime] = None

    @validator('due_date', pre=True, always=True)
    def check_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date must be in the future')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, regex="^(open|in_progress|completed|closed)$")
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None

    @validator('due_date', pre=True, always=True)
    def check_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date must be in the future')
        return v

class RunCreate(BaseModel):
    task_id: int
    status: str = Field(..., regex="^(pending|running|completed|failed)$")
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    @validator('ended_at', pre=True, always=True)
    def check_ended_at(cls, v, values):
        if v and values.get('started_at') and v < values['started_at']:
            raise ValueError('Ended at must be after started at')
        return v

class RunUpdate(BaseModel):
    status: Optional[str] = Field(None, regex="^(pending|running|completed|failed)$")
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    @validator('ended_at', pre=True, always=True)
    def check_ended_at(cls, v, values):
        if v and values.get('started_at') and v < values['started_at']:
            raise ValueError('Ended at must be after started at')
        return v

class ResultCreate(BaseModel):
    task_id: int
    data: dict
    status: str = Field(..., regex="^(success|failure)$")

class ResultUpdate(BaseModel):
    data: Optional[dict] = None
    status: Optional[str] = Field(None, regex="^(success|failure)$")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=8, max_length=50)
    is_active: bool = True
    is_admin: bool = False

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(User):
    hashed_password: str





























