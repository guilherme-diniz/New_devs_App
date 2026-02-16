from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

class Property(BaseModel):
    id: str
    tenant_id: str
    name: str
    timezone: str
    created_at: datetime
    