# services/property_service.py
from sqlalchemy.orm import Session
from domain.models import Property, PropertyStatus

class PropertyService:
    """
    Handles data access logic for Property entities.
    """

    @staticmethod
    def get_all_properties(db: Session) -> list[Property]:
        """Fetches all properties from the database."""
        return db.query(Property).all()

    @staticmethod
    def search_properties(
        db: Session, 
        city: str | None = None, 
        min_price: float = 0, 
        max_price: float = 1e9, 
        status: str = "available"
    ) -> list[Property]:
        try:
            status_enum = PropertyStatus[status.lower()]
        except KeyError:
            status_enum = PropertyStatus.available
        query = db.query(Property).filter(
            Property.status == status_enum)
        if city:
            query = query.filter(Property.city.ilike(f"%{city}%"))
        query = query.filter(
            Property.price >= min_price, 
            Property.price <= max_price)
        return query.all()

    @staticmethod
    def get_by_id(db: Session, property_id: str) -> Property:
        return db.query(Property).filter(Property.id == property_id).first()
    
    @staticmethod
    def create_property(
        db: Session, 
        property_id: str,
        city: str, 
        price: float, 
        rooms: int, 
        status: str, 
        description: str, 
        features: str
    ) -> Property:
        """
        Creates a new property record in the database.
        """
        try:
            if not property_id or not property_id.strip():
                raise ValueError("The property_id cannot be empty.")
            try:
                status_enum = PropertyStatus[status.lower()]
            except KeyError:
                raise KeyError("The 'status' parameter only can be 'available' or 'sold'.")

            new_prop = Property(
                id=property_id,
                city=city,
                price=price,
                rooms=rooms,
                status=status_enum,
                description=description,
                features=features
            )
            db.add(new_prop)
            return new_prop
        except Exception as e:
            raise e

    @staticmethod
    def delete_property(db: Session, property_id: str) -> bool:
        """
        Deletes a property by its ID.
        Returns True if deleted, False if not found.
        """
        try:
            if not property_id or not property_id.strip():
                raise ValueError("The property_id cannot be empty.")
            prop = db.query(Property).filter(Property.id == property_id).first()
            
            if not prop:
                return False
                
            db.delete(prop)
            return True
        except Exception as e:
            raise e
        
    @staticmethod
    def update_property(
        db: Session, 
        property_id: str,
        **kwargs
    ) -> Property | bool:
        """
        Updates an existing property. Returns the updated property or False 
        if not found.
        """
        try:
            prop = db.query(Property).filter(Property.id == property_id).first()
            if not prop:
                return False

            if "status" in kwargs and kwargs["status"]:
                try:
                    kwargs["status"] = PropertyStatus[kwargs["status"].lower()]
                except KeyError:
                    raise KeyError("The 'status' parameter only can be 'available' or 'sold'.")

            for key, value in kwargs.items():
                if value is not None:
                    setattr(prop, key, value)

            return prop
        except Exception as e:
            raise e

    @staticmethod
    def create_sample_data(db: Session) -> bool:
        """
        Seeds the database if empty.
        """
        if db.query(Property).count() == 0:
            samples = [
                Property(id="prop_001", city="Madrid", price=300000, rooms=2, status="available", description="Bright apartment in downtown", features=""),
                Property(id="prop_002", city="Barcelona", price=450000, rooms=3, status="available", description="Penthouse with sea views", features=""),
                Property(id="prop_003", city="Sevilla", price=180000, rooms=2, status="available", description="Classic house in Santa Cruz", features="")
            ]
            db.add_all(samples)
            return True
        return False