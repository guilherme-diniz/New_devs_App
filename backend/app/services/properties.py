from typing import List, Dict, Any
from app.core.database_pool import DatabasePool
from app.models.property import Property

async def list_properties(tenant_id: str) -> List[Property]:
    """
    Get properties for a tenant.
    """
    try:
        from sqlalchemy import text

        db_pool = DatabasePool()
        await db_pool.initialize()

        if not db_pool.session_factory:
            raise Exception("Database pool not available")

        session = await db_pool.get_session()
        try:
            query = text("""
                SELECT id, tenant_id, name, timezone, created_at
                FROM properties
                WHERE tenant_id = :tenant_id
                ORDER BY name
            """)

            result = await session.execute(query, {"tenant_id": tenant_id})
            rows = result.fetchall()

            return [
                Property(
                    id=row.id,
                    tenant_id=row.tenant_id,
                    name=row.name,
                    timezone=row.timezone,
                    created_at=row.created_at.isoformat() if row.created_at else None,
                )
                for row in rows
            ]
        finally:
            await session.close()

    except Exception as e:
        print(f"Error getting properties: {e}")
        return []