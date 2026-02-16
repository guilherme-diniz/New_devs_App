from app.models.property import Property
from app.services.properties import list_properties
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from app.core.auth import authenticate_request as get_current_user
from app.core.database_pool import DatabasePool

router = APIRouter()


@router.get("/properties")
async def get_properties(
    current_user: dict = Depends(get_current_user),
) -> List[Property]:

    tenant_id = getattr(current_user, "tenant_id", "default_tenant") or "default_tenant"
    
    properties = await list_properties(tenant_id)
    
    return properties