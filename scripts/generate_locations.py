import json
import random
import requests

SOURCE_URL = "https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json"


def main():
    resp = requests.get(SOURCE_URL, timeout=60)
    resp.raise_for_status()
    cities = resp.json()
    sample = random.sample(cities, 200)
    locs = []
    for c in sample:
        locs.append({
            "name": c["name"],
            "country": c["country"],
            "latitude": float(c["lat"]),
            "longitude": float(c["lng"])
        })
    with open("locations.json", "w") as f:
        json.dump(locs, f, indent=2)
    print("Wrote", len(locs), "locations to locations.json")


if __name__ == "__main__":
    main()
