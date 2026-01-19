# server/tools.py
import asyncio
from infra.database import get_db_session
from services.property_service import PropertyService
from services.content_service import ContentGeneratorService

def register_tools(mcp):
    """
    Registers the tools in the FastMCP instance using the Service layer.
    """

    @mcp.tool()
    async def search_properties(
        city: str | None = None, 
        min_price: float = 0.0, 
        max_price: float = 1000000.0, 
        status: str = "available"
    ) -> list[dict]:
        """Search for properties with filters."""
        # Using to_thread to keep the event loop non-blocking
        def sync_search():
            with get_db_session() as db:
                props = PropertyService.search_properties(
                    db, city, min_price, max_price, status)
                return ContentGeneratorService.format_property_list(props)
        
        return await asyncio.to_thread(sync_search)
    
    @mcp.tool()
    async def get_property_details(property_id: str) -> dict:
        """Retrieves full technical details for a specific property ID."""
        def sync_get():
            with get_db_session() as db:
                p = PropertyService.get_by_id(db, property_id)
                return ContentGeneratorService.format_property_detail(p)
            
        return await asyncio.to_thread(sync_get)
    
    @mcp.tool()
    async def generate_listing_content(
        property_id: str, 
        target_language: str = "en", 
        tone: str | None = None
    ) -> str:
        """Generates SEO-optimized HTML listing content."""
        def sync_gen():
            with get_db_session() as db:
                p = PropertyService.get_by_id(db, property_id)
                return ContentGeneratorService.generate_listing_content(
                            p, target_language, tone)
        
        return await asyncio.to_thread(sync_gen)

    @mcp.tool()
    async def add_property(
        property_id: str,
        city: str, 
        price: float, 
        rooms: int, 
        status: str, 
        description: str = "", 
        features: str = ""
    ) -> dict:
        """Adds a new property. Status should be 'available' or 'sold'."""
        def sync_add():
            with get_db_session() as db:
                try:
                    new_prop = PropertyService.create_property(
                        db, property_id, city, price, rooms, status, description, features
                    )
                    return ContentGeneratorService.format_action_result(
                        success=True,
                        message=f"Property {new_prop.id} created successfully"
                    )
                except Exception as e:
                        return ContentGeneratorService.format_action_result(
                        success=False,
                        message=f"Could not create property: {str(e)}"
                    )
        
        return await asyncio.to_thread(sync_add)

    @mcp.tool()
    async def delete_property(property_id: str) -> dict:
        """
        Permanently removes a property from the catalog by its ID.
        """
        def sync_delete():
            with get_db_session() as db:
                try:
                    success = PropertyService.delete_property(db, property_id)
                    if success:
                        return ContentGeneratorService.format_action_result(
                            success=True,
                            message=f"Property {property_id} deleted"
                        )
                    return ContentGeneratorService.format_action_result(
                            success=False,
                            message=f"Property {property_id} not found"
                        )
                except Exception as e:
                    return ContentGeneratorService.format_action_result(
                            success=False,
                            message=f"Could not delete property: {str(e)}"
                        )
        
        return await asyncio.to_thread(sync_delete)
    
    @mcp.tool()
    async def update_property(
        property_id: str,
        city: str | None = None,
        price: float | None = None,
        rooms: int | None = None,
        status: str | None = None,
        description: str | None = None,
        features: str | None = None
    ) -> dict:
        """
        Updates an existing property in the catalog. 
        Only provide the fields that need to be changed.
        """
        def sync_update():
            with get_db_session() as db:
                try:
                    update_data = {
                        "city": city,
                        "price": price,
                        "rooms": rooms,
                        "status": status,
                        "description": description,
                        "features": features
                    }
                    
                    # Discard None values
                    update_data = {k: v for k, v in update_data.items() if v is not None}

                    updated_prop = PropertyService.update_property(
                        db, property_id, **update_data)
                    
                    if updated_prop:
                        return ContentGeneratorService.format_action_result(
                            success=True,
                            message=f"Property {property_id} updated successfully"
                        )
                    else:
                        return ContentGeneratorService.format_action_result(
                            success=False,
                            message=f"Property {property_id} not found"
                        )
                except Exception as e:
                    return ContentGeneratorService.format_action_result(
                        success=False,
                        message=f"Could not update property: {str(e)}"
                    )

        return await asyncio.to_thread(sync_update)

    @mcp.tool()
    async def seed_data() -> dict:
        """Seed the database with samples."""
        def sync_seed():
            with get_db_session() as db:
                try:
                    success = PropertyService.create_sample_data(db)
                    if success:
                        return ContentGeneratorService.format_action_result(
                            success=True,
                            message="Data seeded successfully"
                        )
                    return ContentGeneratorService.format_action_result(
                        success=False,
                        message="Database already had data."
                    )
                except Exception as e:
                    return ContentGeneratorService.format_action_result(
                        success=False,
                        message=f"Could not seed data: {str(e)}"
                    )
        
        return await asyncio.to_thread(sync_seed)