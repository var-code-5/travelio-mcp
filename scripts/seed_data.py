#!/usr/bin/env python
"""
Database seeder script for Travelio application.
Seeds the database with realistic data for Phuket and Krabi regions in Thailand.
"""
import asyncio
import json
from datetime import datetime, time
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.models.destination import Destination
from app.db.models.attraction import Attraction
from app.db.models.hotel import Hotel
from app.db.base import Base
from app.core.config import settings

# Thai destinations data
DESTINATIONS = [
    {
        "name": "Phuket",
        "country": "Thailand",
        "description": "Thailand's largest island, known for its beautiful beaches, clear waters, and vibrant nightlife.",
        "latitude": 7.9519,
        "longitude": 98.3381,
        "image_url": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?q=80&w=1000",
        "popularity_score": 9.2,
        "attractions": [
            {
                "name": "Patong Beach",
                "description": "Phuket's most popular beach, known for its vibrant nightlife and wide range of activities.",
                "category": "Beach",
                "latitude": 7.9016,
                "longitude": 98.2971,
                "image_url": "https://images.unsplash.com/photo-1589394777611-25e8719591a7?q=80&w=1000",
                "rating": 4.3,
                "price_range": 1,
                "visit_duration_minutes": 180,
                "opening_hours": {
                    "monday": {"open": "00:00", "close": "23:59"},
                    "tuesday": {"open": "00:00", "close": "23:59"},
                    "wednesday": {"open": "00:00", "close": "23:59"},
                    "thursday": {"open": "00:00", "close": "23:59"},
                    "friday": {"open": "00:00", "close": "23:59"},
                    "saturday": {"open": "00:00", "close": "23:59"},
                    "sunday": {"open": "00:00", "close": "23:59"}
                },
                "is_must_visit": True
            },
            {
                "name": "Phang Nga Bay",
                "description": "Famous for its limestone cliffs, hidden caves, and emerald green waters.",
                "category": "Natural Landmark",
                "latitude": 8.2751,
                "longitude": 98.5039,
                "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?q=80&w=1000",
                "rating": 4.8,
                "price_range": 3,
                "visit_duration_minutes": 360,
                "opening_hours": {
                    "monday": {"open": "08:00", "close": "17:00"},
                    "tuesday": {"open": "08:00", "close": "17:00"},
                    "wednesday": {"open": "08:00", "close": "17:00"},
                    "thursday": {"open": "08:00", "close": "17:00"},
                    "friday": {"open": "08:00", "close": "17:00"},
                    "saturday": {"open": "08:00", "close": "17:00"},
                    "sunday": {"open": "08:00", "close": "17:00"}
                },
                "is_must_visit": True
            },
            {
                "name": "Big Buddha",
                "description": "A 45-meter tall marble statue of Buddha that offers panoramic views of the island.",
                "category": "Religious Site",
                "latitude": 7.8276,
                "longitude": 98.3116,
                "image_url": "https://images.unsplash.com/photo-1585468274952-66591eb14165?q=80&w=1000",
                "rating": 4.6,
                "price_range": 1,
                "visit_duration_minutes": 120,
                "opening_hours": {
                    "monday": {"open": "08:00", "close": "19:30"},
                    "tuesday": {"open": "08:00", "close": "19:30"},
                    "wednesday": {"open": "08:00", "close": "19:30"},
                    "thursday": {"open": "08:00", "close": "19:30"},
                    "friday": {"open": "08:00", "close": "19:30"},
                    "saturday": {"open": "08:00", "close": "19:30"},
                    "sunday": {"open": "08:00", "close": "19:30"}
                },
                "is_must_visit": True
            },
            {
                "name": "Old Phuket Town",
                "description": "Historical district with colorful Sino-Portuguese buildings, cafes, and shops.",
                "category": "Cultural",
                "latitude": 7.8856,
                "longitude": 98.3922,
                "image_url": "https://images.unsplash.com/photo-1587996597484-04245d2e9f4e?q=80&w=1000",
                "rating": 4.4,
                "price_range": 1,
                "visit_duration_minutes": 180,
                "opening_hours": {
                    "monday": {"open": "10:00", "close": "22:00"},
                    "tuesday": {"open": "10:00", "close": "22:00"},
                    "wednesday": {"open": "10:00", "close": "22:00"},
                    "thursday": {"open": "10:00", "close": "22:00"},
                    "friday": {"open": "10:00", "close": "22:00"},
                    "saturday": {"open": "10:00", "close": "22:00"},
                    "sunday": {"open": "10:00", "close": "22:00"}
                },
                "is_must_visit": False
            },
            {
                "name": "Phi Phi Islands",
                "description": "Group of islands known for stunning beaches, clear waters, and limestone cliffs.",
                "category": "Island",
                "latitude": 7.7407,
                "longitude": 98.7784,
                "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?q=80&w=1000",
                "rating": 4.7,
                "price_range": 3,
                "visit_duration_minutes": 480,
                "opening_hours": {
                    "monday": {"open": "07:00", "close": "18:00"},
                    "tuesday": {"open": "07:00", "close": "18:00"},
                    "wednesday": {"open": "07:00", "close": "18:00"},
                    "thursday": {"open": "07:00", "close": "18:00"},
                    "friday": {"open": "07:00", "close": "18:00"},
                    "saturday": {"open": "07:00", "close": "18:00"},
                    "sunday": {"open": "07:00", "close": "18:00"}
                },
                "is_must_visit": True
            },
            {
                "name": "Wat Chalong",
                "description": "The largest and most important Buddhist temple in Phuket.",
                "category": "Religious Site",
                "latitude": 7.8459,
                "longitude": 98.3371,
                "image_url": "https://images.unsplash.com/photo-1558431382-27e303142255?q=80&w=1000",
                "rating": 4.5,
                "price_range": 1,
                "visit_duration_minutes": 90,
                "opening_hours": {
                    "monday": {"open": "07:00", "close": "17:00"},
                    "tuesday": {"open": "07:00", "close": "17:00"},
                    "wednesday": {"open": "07:00", "close": "17:00"},
                    "thursday": {"open": "07:00", "close": "17:00"},
                    "friday": {"open": "07:00", "close": "17:00"},
                    "saturday": {"open": "07:00", "close": "17:00"},
                    "sunday": {"open": "07:00", "close": "17:00"}
                },
                "is_must_visit": False
            },
            {
                "name": "Kata Beach",
                "description": "Beautiful sandy beach known for good swimming and surfing conditions.",
                "category": "Beach",
                "latitude": 7.8203,
                "longitude": 98.2977,
                "image_url": "https://images.unsplash.com/photo-1589394775548-0ea23e2e2aa0?q=80&w=1000",
                "rating": 4.5,
                "price_range": 1,
                "visit_duration_minutes": 240,
                "opening_hours": {
                    "monday": {"open": "00:00", "close": "23:59"},
                    "tuesday": {"open": "00:00", "close": "23:59"},
                    "wednesday": {"open": "00:00", "close": "23:59"},
                    "thursday": {"open": "00:00", "close": "23:59"},
                    "friday": {"open": "00:00", "close": "23:59"},
                    "saturday": {"open": "00:00", "close": "23:59"},
                    "sunday": {"open": "00:00", "close": "23:59"}
                },
                "is_must_visit": False
            },
            {
                "name": "Phuket Fantasea",
                "description": "Cultural theme park showcasing Thai heritage and traditions through shows and entertainment.",
                "category": "Entertainment",
                "latitude": 7.9563,
                "longitude": 98.2768,
                "image_url": "https://images.unsplash.com/photo-1617525104975-5a0a4d793010?q=80&w=1000",
                "rating": 4.2,
                "price_range": 4,
                "visit_duration_minutes": 240,
                "opening_hours": {
                    "monday": {"open": "17:30", "close": "23:00"},
                    "tuesday": {"open": "17:30", "close": "23:00"},
                    "wednesday": {"open": "17:30", "close": "23:00"},
                    "thursday": {"open": "17:30", "close": "23:00"},
                    "friday": {"open": "17:30", "close": "23:00"},
                    "saturday": {"open": "17:30", "close": "23:00"},
                    "sunday": {"open": "17:30", "close": "23:00"}
                },
                "is_must_visit": False
            },
            {
                "name": "Bangla Road",
                "description": "Famous nightlife street in Patong with bars, clubs, and entertainment.",
                "category": "Nightlife",
                "latitude": 7.8933,
                "longitude": 98.2967,
                "image_url": "https://images.unsplash.com/photo-1591602555925-7d13a8c8595b?q=80&w=1000",
                "rating": 4.0,
                "price_range": 3,
                "visit_duration_minutes": 180,
                "opening_hours": {
                    "monday": {"open": "18:00", "close": "03:00"},
                    "tuesday": {"open": "18:00", "close": "03:00"},
                    "wednesday": {"open": "18:00", "close": "03:00"},
                    "thursday": {"open": "18:00", "close": "03:00"},
                    "friday": {"open": "18:00", "close": "03:00"},
                    "saturday": {"open": "18:00", "close": "03:00"},
                    "sunday": {"open": "18:00", "close": "03:00"}
                },
                "is_must_visit": False
            },
            {
                "name": "Karon Viewpoint",
                "description": "Scenic viewpoint offering panoramic views of three beaches: Kata Noi, Kata, and Karon.",
                "category": "Viewpoint",
                "latitude": 7.8278,
                "longitude": 98.3015,
                "image_url": "https://images.unsplash.com/photo-1599643466448-55f8929b7a58?q=80&w=1000",
                "rating": 4.6,
                "price_range": 1,
                "visit_duration_minutes": 60,
                "opening_hours": {
                    "monday": {"open": "00:00", "close": "23:59"},
                    "tuesday": {"open": "00:00", "close": "23:59"},
                    "wednesday": {"open": "00:00", "close": "23:59"},
                    "thursday": {"open": "00:00", "close": "23:59"},
                    "friday": {"open": "00:00", "close": "23:59"},
                    "saturday": {"open": "00:00", "close": "23:59"},
                    "sunday": {"open": "00:00", "close": "23:59"}
                },
                "is_must_visit": True
            }
        ],
        "hotels": [
            {
                "name": "The Slate",
                "description": "Luxury resort inspired by Phuket's tin mining past, featuring unique design elements and extensive facilities.",
                "address": "116, Moo 1, Sakhu, Thalang, Phuket 83110",
                "latitude": 8.0889,
                "longitude": 98.2969,
                "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1000",
                "rating": 4.8,
                "price_per_night": 350.0,
                "amenities": ["Swimming pool", "Spa", "Fitness center", "Restaurant", "Bar", "Beach access"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Amanpuri",
                "description": "Ultra-luxury resort set on a private peninsula with breathtaking Andaman Sea views.",
                "address": "Pansea Beach, Cherngtalay, Thalang, Phuket 83110",
                "latitude": 7.9894,
                "longitude": 98.2770,
                "image_url": "https://images.unsplash.com/photo-1535827841776-24afc1e255ac?q=80&w=1000",
                "rating": 4.9,
                "price_per_night": 850.0,
                "amenities": ["Private beach", "Spa", "Yoga pavilion", "Fine dining", "Water sports", "Infinity pool"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Holiday Inn Resort Phuket",
                "description": "Family-friendly resort in the heart of Patong, walking distance to the beach and entertainment.",
                "address": "52 Thaweewong Road, Patong, Kathu, Phuket 83150",
                "latitude": 7.8970,
                "longitude": 98.2957,
                "image_url": "https://images.unsplash.com/photo-1606046604972-77cc76aee944?q=80&w=1000",
                "rating": 4.3,
                "price_per_night": 120.0,
                "amenities": ["Swimming pools", "Kids club", "Restaurants", "Fitness center", "Spa"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Kata Rocks",
                "description": "Luxury resort featuring private pool villas with stunning ocean views.",
                "address": "186/22 Kok Tanode Road, Kata Beach, Phuket 83100",
                "latitude": 7.8083,
                "longitude": 98.2987,
                "image_url": "https://images.unsplash.com/photo-1615460549969-36fa19521a4f?q=80&w=1000",
                "rating": 4.7,
                "price_per_night": 450.0,
                "amenities": ["Infinity pools", "Spa", "Fitness center", "Restaurant", "Bar"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "The Westin Siray Bay Resort & Spa",
                "description": "Beachfront resort offering modern amenities and spectacular bay views.",
                "address": "21/4 Moo 1 T.Rasada A.Muang, Phuket 83000",
                "latitude": 7.8818,
                "longitude": 98.4241,
                "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?q=80&w=1000",
                "rating": 4.4,
                "price_per_night": 220.0,
                "amenities": ["Swimming pools", "Beach access", "Spa", "Fitness center", "Kids club"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Centara Grand Beach Resort Phuket",
                "description": "Luxury beachfront resort with a water park and extensive facilities for families.",
                "address": "683 Patak Road, Karon Beach, Phuket 83100",
                "latitude": 7.8397,
                "longitude": 98.2945,
                "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?q=80&w=1000",
                "rating": 4.5,
                "price_per_night": 280.0,
                "amenities": ["Water park", "Spa", "Fitness center", "Kids club", "Restaurants", "Bars"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            }
        ]
    },
    {
        "name": "Krabi",
        "country": "Thailand",
        "description": "A province on southern Thailand's Andaman coast, known for its stunning limestone karsts, beautiful islands, and relaxed atmosphere.",
        "latitude": 8.0862,
        "longitude": 98.9063,
        "image_url": "https://images.unsplash.com/photo-1509358271058-acd22cc93898?q=80&w=1000",
        "popularity_score": 8.9,
        "attractions": [
            {
                "name": "Railay Beach",
                "description": "Stunning beach surrounded by limestone cliffs, accessible only by boat and famous for rock climbing.",
                "category": "Beach",
                "latitude": 8.0094,
                "longitude": 98.8343,
                "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?q=80&w=1000",
                "rating": 4.8,
                "price_range": 1,
                "visit_duration_minutes": 240,
                "opening_hours": {
                    "monday": {"open": "00:00", "close": "23:59"},
                    "tuesday": {"open": "00:00", "close": "23:59"},
                    "wednesday": {"open": "00:00", "close": "23:59"},
                    "thursday": {"open": "00:00", "close": "23:59"},
                    "friday": {"open": "00:00", "close": "23:59"},
                    "saturday": {"open": "00:00", "close": "23:59"},
                    "sunday": {"open": "00:00", "close": "23:59"}
                },
                "is_must_visit": True
            },
            {
                "name": "Ao Nang Beach",
                "description": "Popular beach with beautiful views, restaurants, and shops along the beachfront.",
                "category": "Beach",
                "latitude": 8.0327,
                "longitude": 98.8150,
                "image_url": "https://images.unsplash.com/photo-1548080819-40e672cd157d?q=80&w=1000",
                "rating": 4.5,
                "price_range": 1,
                "visit_duration_minutes": 180,
                "opening_hours": {
                    "monday": {"open": "00:00", "close": "23:59"},
                    "tuesday": {"open": "00:00", "close": "23:59"},
                    "wednesday": {"open": "00:00", "close": "23:59"},
                    "thursday": {"open": "00:00", "close": "23:59"},
                    "friday": {"open": "00:00", "close": "23:59"},
                    "saturday": {"open": "00:00", "close": "23:59"},
                    "sunday": {"open": "00:00", "close": "23:59"}
                },
                "is_must_visit": True
            },
            {
                "name": "Hong Islands",
                "description": "Group of islands with beautiful beaches, clear waters, and a large lagoon.",
                "category": "Island",
                "latitude": 8.0689,
                "longitude": 98.7363,
                "image_url": "https://images.unsplash.com/photo-1588867702719-969c8c464e96?q=80&w=1000",
                "rating": 4.7,
                "price_range": 3,
                "visit_duration_minutes": 300,
                "opening_hours": {
                    "monday": {"open": "07:00", "close": "17:00"},
                    "tuesday": {"open": "07:00", "close": "17:00"},
                    "wednesday": {"open": "07:00", "close": "17:00"},
                    "thursday": {"open": "07:00", "close": "17:00"},
                    "friday": {"open": "07:00", "close": "17:00"},
                    "saturday": {"open": "07:00", "close": "17:00"},
                    "sunday": {"open": "07:00", "close": "17:00"}
                },
                "is_must_visit": True
            },
            {
                "name": "Tiger Cave Temple (Wat Tham Suea)",
                "description": "Buddhist temple complex with panoramic views from the top of a 1,237-step climb.",
                "category": "Religious Site",
                "latitude": 8.1267,
                "longitude": 98.9242,
                "image_url": "https://images.unsplash.com/photo-1528181304800-259b08848526?q=80&w=1000",
                "rating": 4.6,
                "price_range": 1,
                "visit_duration_minutes": 180,
                "opening_hours": {
                    "monday": {"open": "08:00", "close": "17:00"},
                    "tuesday": {"open": "08:00", "close": "17:00"},
                    "wednesday": {"open": "08:00", "close": "17:00"},
                    "thursday": {"open": "08:00", "close": "17:00"},
                    "friday": {"open": "08:00", "close": "17:00"},
                    "saturday": {"open": "08:00", "close": "17:00"},
                    "sunday": {"open": "08:00", "close": "17:00"}
                },
                "is_must_visit": False
            },
            {
                "name": "Emerald Pool (Sa Morakot)",
                "description": "Natural pool with crystal clear emerald-colored water, surrounded by forest.",
                "category": "Natural Landmark",
                "latitude": 7.9262,
                "longitude": 99.2535,
                "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?q=80&w=1000",
                "rating": 4.5,
                "price_range": 2,
                "visit_duration_minutes": 120,
                "opening_hours": {
                    "monday": {"open": "08:30", "close": "17:00"},
                    "tuesday": {"open": "08:30", "close": "17:00"},
                    "wednesday": {"open": "08:30", "close": "17:00"},
                    "thursday": {"open": "08:30", "close": "17:00"},
                    "friday": {"open": "08:30", "close": "17:00"},
                    "saturday": {"open": "08:30", "close": "17:00"},
                    "sunday": {"open": "08:30", "close": "17:00"}
                },
                "is_must_visit": True
            },
            {
                "name": "Krabi Town Night Market",
                "description": "Vibrant night market with local food, souvenirs, and cultural performances.",
                "category": "Market",
                "latitude": 8.0637,
                "longitude": 98.9177,
                "image_url": "https://images.unsplash.com/photo-1591197172062-c718f82aba20?q=80&w=1000",
                "rating": 4.3,
                "price_range": 1,
                "visit_duration_minutes": 120,
                "opening_hours": {
                    "monday": {"open": "17:00", "close": "22:00"},
                    "tuesday": {"open": "17:00", "close": "22:00"},
                    "wednesday": {"open": "17:00", "close": "22:00"},
                    "thursday": {"open": "17:00", "close": "22:00"},
                    "friday": {"open": "17:00", "close": "22:00"},
                    "saturday": {"open": "17:00", "close": "22:00"},
                    "sunday": {"open": "17:00", "close": "22:00"}
                },
                "is_must_visit": False
            },
            {
                "name": "4 Islands Tour",
                "description": "Tour including Koh Poda, Koh Gai (Chicken Island), Koh Tup, and Koh Mor, known for beautiful beaches and snorkeling.",
                "category": "Tour",
                "latitude": 7.9646,
                "longitude": 98.8302,
                "image_url": "https://images.unsplash.com/photo-1547542928-4a3c4b5b0b08?q=80&w=1000",
                "rating": 4.7,
                "price_range": 3,
                "visit_duration_minutes": 360,
                "opening_hours": {
                    "monday": {"open": "08:00", "close": "16:00"},
                    "tuesday": {"open": "08:00", "close": "16:00"},
                    "wednesday": {"open": "08:00", "close": "16:00"},
                    "thursday": {"open": "08:00", "close": "16:00"},
                    "friday": {"open": "08:00", "close": "16:00"},
                    "saturday": {"open": "08:00", "close": "16:00"},
                    "sunday": {"open": "08:00", "close": "16:00"}
                },
                "is_must_visit": True
            },
            {
                "name": "Phra Nang Cave Beach",
                "description": "Beautiful beach with a shrine in a cave, accessible from Railay.",
                "category": "Beach",
                "latitude": 8.0028,
                "longitude": 98.8375,
                "image_url": "https://images.unsplash.com/photo-1560179406-1c6c60e0dc76?q=80&w=1000",
                "rating": 4.8,
                "price_range": 1,
                "visit_duration_minutes": 180,
                "opening_hours": {
                    "monday": {"open": "00:00", "close": "23:59"},
                    "tuesday": {"open": "00:00", "close": "23:59"},
                    "wednesday": {"open": "00:00", "close": "23:59"},
                    "thursday": {"open": "00:00", "close": "23:59"},
                    "friday": {"open": "00:00", "close": "23:59"},
                    "saturday": {"open": "00:00", "close": "23:59"},
                    "sunday": {"open": "00:00", "close": "23:59"}
                },
                "is_must_visit": True
            }
        ],
        "hotels": [
            {
                "name": "Rayavadee",
                "description": "Luxury resort set on the edge of Krabi Marine National Park, surrounded by beaches and limestone cliffs.",
                "address": "214 Moo 2, Tambon Ao-Nang, Amphur Muang, Krabi 81000",
                "latitude": 8.0093,
                "longitude": 98.8368,
                "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1000",
                "rating": 4.9,
                "price_per_night": 650.0,
                "amenities": ["Private beach", "Spa", "Restaurants", "Tennis court", "Water sports"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Centara Grand Beach Resort & Villas Krabi",
                "description": "Luxury beachfront resort with private bay access and stunning views of limestone formations.",
                "address": "396-396/1 Moo 2, Ao Nang, Muang, Krabi 81000",
                "latitude": 8.0200,
                "longitude": 98.8218,
                "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?q=80&w=1000",
                "rating": 4.6,
                "price_per_night": 320.0,
                "amenities": ["Private beach", "Spa", "Swimming pools", "Water sports", "Kids club"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Phulay Bay, a Ritz-Carlton Reserve",
                "description": "Ultra-luxury resort with private pavilions and villas overlooking the Andaman Sea.",
                "address": "111 Moo 3, Nongthalay, Muang, Krabi 81180",
                "latitude": 8.0655,
                "longitude": 98.7605,
                "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1000",
                "rating": 4.8,
                "price_per_night": 750.0,
                "amenities": ["Private pools", "Spa", "Beachfront dining", "Fitness center", "Yoga pavilion"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Dusit Thani Krabi Beach Resort",
                "description": "Elegant beachfront resort with extensive facilities and tropical gardens.",
                "address": "155 Moo 2, Nong Thale, Muang, Krabi 81180",
                "latitude": 8.0556,
                "longitude": 98.7550,
                "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?q=80&w=1000",
                "rating": 4.5,
                "price_per_night": 250.0,
                "amenities": ["Beach access", "Swimming pools", "Spa", "Fitness center", "Tennis courts"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            },
            {
                "name": "Sofitel Krabi Phokeethra Golf & Spa Resort",
                "description": "Luxury resort featuring the largest pool in Thailand and an adjacent golf course.",
                "address": "200 Moo 3, Klong Muang Beach, Nong Thale, Krabi 81180",
                "latitude": 8.0585,
                "longitude": 98.7540,
                "image_url": "https://images.unsplash.com/photo-1556292935-06d8ddf4160e?q=80&w=1000",
                "rating": 4.7,
                "price_per_night": 290.0,
                "amenities": ["Golf course", "Spa", "Huge swimming pool", "Fitness center", "Kids club"],
                "has_restaurant": True,
                "has_pool": True,
                "has_spa": True,
                "has_gym": True,
                "has_free_wifi": True
            }
        ]
    }
]

async def seed_database():
    """Seed the database with destinations, attractions, and hotels."""
    # Create SQLAlchemy engine
    engine = create_async_engine(settings.DATABASE_URI)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with engine.begin() as conn:
        # Uncomment the next line if you want to drop existing tables (be careful!)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Insert data
    async with async_session() as session:
        # For each destination
        for dest_data in DESTINATIONS:
            # Extract attractions and hotels
            attractions_data = dest_data.pop("attractions", [])
            hotels_data = dest_data.pop("hotels", [])
            
            # Create destination
            destination = Destination(**dest_data)
            session.add(destination)
            await session.flush()  # Flush to get the ID
            
            # Create attractions for this destination
            for attr_data in attractions_data:
                # Convert opening hours to JSON string
                attr_data["opening_hours"] = json.dumps(attr_data["opening_hours"])
                attr_data["destination_id"] = destination.id
                attraction = Attraction(**attr_data)
                session.add(attraction)
            
            # Create hotels for this destination
            for hotel_data in hotels_data:
                # Convert amenities to JSON string
                hotel_data["amenities"] = json.dumps(hotel_data["amenities"])
                hotel_data["destination_id"] = destination.id
                hotel = Hotel(**hotel_data)
                session.add(hotel)
        
        # Commit all changes
        await session.commit()
    
    print(f"Successfully seeded database with {len(DESTINATIONS)} destinations")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(seed_database())
