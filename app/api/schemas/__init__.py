from app.api.schemas.destination import (
    DestinationBase, DestinationCreate, DestinationUpdate, Destination
)
from app.api.schemas.attraction import (
    AttractionBase, AttractionCreate, AttractionUpdate, Attraction, OpeningHours
)
from app.api.schemas.hotel import (
    HotelBase, HotelCreate, HotelUpdate, Hotel
)
from app.api.schemas.itinerary import (
    ActivityBase, ActivityCreate, ActivityUpdate, Activity,
    ItineraryDayBase, ItineraryDayCreate, ItineraryDayUpdate, ItineraryDay,
    ItineraryBase, ItineraryCreate, ItineraryUpdate, Itinerary, ItineraryRequest
)
from app.api.schemas.itinerary_template import (
    ItineraryTemplateBase, ItineraryTemplateCreate, 
    ItineraryTemplateUpdate, ItineraryTemplate
)