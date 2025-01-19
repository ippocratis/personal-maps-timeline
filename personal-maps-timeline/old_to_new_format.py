import json
import os
from datetime import datetime

def convert_latlng(latE7, lngE7):
    """Convert latitudeE7 and longitudeE7 to decimal degrees."""
    return f"{latE7 / 1e7:.7f}°, {lngE7 / 1e7:.7f}°"

def convert_timestamp(timestamp):
    """Convert ISO 8601 timestamp to desired format."""
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return dt.isoformat()

def convert_2022_to_timeline2(input_file, output_file):
    """Convert a single file from the 2022_AUGUST format to Timeline2."""
    try:
        with open(input_file, 'r') as infile:
            data = json.load(infile)
        
        # Check if 'timelineObjects' key exists
        if "timelineObjects" not in data:
            print(f"Skipping {input_file}: 'timelineObjects' key not found.")
            return
        
        timeline2 = {"semanticSegments": []}
        
        for obj in data["timelineObjects"]:
            if "activitySegment" in obj:
                segment = obj["activitySegment"]
                semantic_segment = {
                    "startTime": convert_timestamp(segment["duration"]["startTimestamp"]),
                    "endTime": convert_timestamp(segment["duration"]["endTimestamp"]),
                    "timelinePath": []
                }
                
                for waypoint in segment.get("waypointPath", {}).get("waypoints", []):
                    semantic_segment["timelinePath"].append({
                        "point": convert_latlng(waypoint["latE7"], waypoint["lngE7"]),
                        "time": convert_timestamp(segment["duration"]["startTimestamp"])
                    })
                
                timeline2["semanticSegments"].append(semantic_segment)
            
            elif "placeVisit" in obj:
                visit = obj["placeVisit"]
                location = visit.get("location", {})
                semantic_segment = {
                    "startTime": convert_timestamp(visit["duration"]["startTimestamp"]),
                    "endTime": convert_timestamp(visit["duration"]["endTimestamp"]),
                    "visit": {
                        "topCandidate": {
                            "placeId": location.get("placeId", "NO_PLACE_ID"),  # Use "NO_PLACE_ID" for missing placeId
                            "semanticType": location.get("semanticType", "UNKNOWN"),
                            "placeLocation": {
                                "latLng": convert_latlng(location.get("latitudeE7", 0), location.get("longitudeE7", 0))  # Default lat/lng to 0 if missing
                            }
                        }
                    }
                }
                timeline2["semanticSegments"].append(semantic_segment)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as outfile:
            json.dump(timeline2, outfile, indent=2)
        
        print(f"Converted: {input_file} -> {output_file}")
    
    except json.JSONDecodeError:
        print(f"Skipping {input_file}: Invalid JSON format.")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def process_directory(input_dir, output_dir):
    """Recursively process all JSON files in a directory and its subdirectories."""
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                input_file = os.path.join(root, file)
                # Preserve directory structure in the output directory
                relative_path = os.path.relpath(input_file, input_dir)
                output_file = os.path.join(output_dir, relative_path)
                convert_2022_to_timeline2(input_file, output_file)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py input_dir output_dir")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    process_directory(input_dir, output_dir)

