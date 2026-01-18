# services/content_service.py
from domain.models import Property

class ContentGeneratorService:
    """
    Handles the formatting and generation of text content for the MCP tools.
    """

    @staticmethod
    def format_property_list(properties: list[Property]) -> list[dict]:
        """
        Standardizes format of a list of Property objects (summary view).
        """
        if not properties:
            return []

        return [
            {
                "id": prop.id,
                "city": prop.city,
                "price": prop.price,
                "rooms": prop.rooms,
                "status": prop.status.value,
            }
            for prop in properties
        ]

    @staticmethod
    def format_property_detail(prop: Property | None) -> dict:
        """
        Standardizes the output for a single property detail (full technical
        details).
        """
        if not prop:
            return {"error": "Property not found"}
            
        return ({
            "id": prop.id, 
            "city": prop.city, 
            "price": prop.price, 
            "rooms": prop.rooms, 
            "status": prop.status.value,
            "description": prop.description, 
            "features": prop.features 
            } 
        )
    
    @staticmethod
    def generate_listing_content(
        prop: Property, 
        target_language: str = "en", 
        tone: str | None = None
    ) -> str:
        if not prop:
            return "Error: Property not found for content"
        
        # Mocking the AI generation logic
        title = f"Amazing property in {prop.city} - Only {prop.price}€"
        description = f"Looking for a home with {prop.rooms} rooms? {prop.description}"
        
        return f"""
        <title>{title}</title>
        <meta name="description" content="{description}">
        <meta name="language" content="{target_language}">
        <section>
            <h1>Property Details</h1>
            <p>Status: {prop.status.value}</p>
            <p>Tone: {tone}</p>
        </section>
        """

    @staticmethod
    def format_action_result(
        success: bool, 
        message: str, 
        data: dict | None = None
    ) -> dict:
        """
        Standardizes the JSON response for all aux write operations.
        
        Args:
            success (bool): Whether the operation was successful.
            message (str): A human-readable description of the result.
            data (dict, optional): Additional data related to the action.
            
        Returns:
            dict: A standardized response dictionary.
        """
        return {
            "status": "success" if success else "error",
            "message": message,
            "data": data or {}
        }
    
    