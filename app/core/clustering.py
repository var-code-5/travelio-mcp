from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import KMeans
from math import radians, sin, cos, sqrt, atan2

class AttractionClusterer:
    """
    Class for clustering attractions based on geographical proximity.
    Uses K-means clustering algorithm to group attractions.
    """
    
    def cluster_attractions(self, attractions: List[Dict], num_clusters: int) -> Dict[int, List[Dict]]:
        """
        Cluster attractions into specified number of groups based on geographical proximity.
        
        Args:
            attractions: List of attraction dictionaries with latitude and longitude
            num_clusters: Number of clusters to create (typically number of days)
            
        Returns:
            Dictionary mapping cluster ID to list of attractions in that cluster
        """
        if len(attractions) < num_clusters:
            # If fewer attractions than clusters, adjust the number of clusters
            num_clusters = max(1, len(attractions))
        
        # Extract coordinates for clustering
        coordinates = np.array([[a["latitude"], a["longitude"]] for a in attractions])
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(coordinates)
        
        # Group attractions by cluster
        clustered_attractions = {}
        for i, label in enumerate(cluster_labels):
            cluster_id = int(label)
            if cluster_id not in clustered_attractions:
                clustered_attractions[cluster_id] = []
            
            clustered_attractions[cluster_id].append(attractions[i])
        
        return clustered_attractions
    
    def find_central_point(self, attractions: List[Dict]) -> Dict[str, float]:
        """
        Find the central point among a set of attractions.
        
        Args:
            attractions: List of attraction dictionaries with latitude and longitude
            
        Returns:
            Dictionary with latitude and longitude of central point
        """
        if not attractions:
            raise ValueError("Cannot find central point for empty attraction list")
        
        # Calculate the centroid (simple average of coordinates)
        latitudes = [a["latitude"] for a in attractions]
        longitudes = [a["longitude"] for a in attractions]
        
        center_lat = sum(latitudes) / len(latitudes)
        center_lon = sum(longitudes) / len(longitudes)
        
        return {"latitude": center_lat, "longitude": center_lon}
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using the Haversine formula.
        
        Args:
            lat1: Latitude of point 1
            lon1: Longitude of point 1
            lat2: Latitude of point 2
            lon2: Longitude of point 2
            
        Returns:
            Distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371.0
        
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return distance
