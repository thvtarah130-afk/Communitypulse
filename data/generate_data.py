import random
import pandas as pd
import os

# Locations around a sample area (e.g., NYC)
LOCATIONS = [
    {"name": "Brooklyn", "lat": 40.6782, "lon": -73.9442},
    {"name": "Manhattan", "lat": 40.7831, "lon": -73.9712},
    {"name": "Queens", "lat": 40.7282, "lon": -73.7949},
    {"name": "Bronx", "lat": 40.8448, "lon": -73.8648},
    {"name": "Staten Island", "lat": 40.5795, "lon": -74.1502},
    {"name": "Jersey City", "lat": 40.7178, "lon": -74.0431},
    {"name": "Newark", "lat": 40.7357, "lon": -74.1724},
    {"name": "Yonkers", "lat": 40.9312, "lon": -73.8987},
]

ISSUE_TYPES = ["health", "food", "education", "infrastructure", "other"]
URGENCIES = ["low", "medium", "high"]
SKILLS = ["medical", "teaching", "logistics", "construction", "counseling", "first-aid", "cooking", "driving"]

def generate_issues(count=100):
    issues = []
    for _ in range(count):
        loc = random.choice(LOCATIONS)
        itype = random.choice(ISSUE_TYPES)
        urgency = random.choice(URGENCIES)
        people = random.randint(5, 500)
        
        # Randomize description based on type
        desc_map = {
            "health": f"Need for {random.choice(['medical supplies', 'doctors', 'vaccines', 'checkups'])} in {loc['name']}.",
            "food": f"Shortage of {random.choice(['clean water', 'grains', 'canned food', 'fresh produce'])} affecting community.",
            "education": f"Lack of {random.choice(['teachers', 'textbooks', 'stationary', 'internet access'])} in local schools.",
            "infrastructure": f"Issue with {random.choice(['roads', 'bridge', 'power grid', 'water pipes'])} near {loc['name']}.",
            "other": f"General assistance required for {random.choice(['waste management', 'security', 'community coordination'])}."
        }
        
        issues.append({
            "location": loc["name"],
            "lat": loc["lat"] + random.uniform(-0.05, 0.05),
            "lon": loc["lon"] + random.uniform(-0.05, 0.05),
            "issue_type": itype,
            "description": desc_map[itype],
            "urgency": urgency,
            "people_affected": people
        })
    return pd.DataFrame(issues)

def generate_volunteers(count=30):
    volunteers = []
    names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hank", "Ivy", "Jack", 
             "Kelly", "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Rose", "Sam", "Tina",
             "Umar", "Vera", "Will", "Xena", "Yara", "Zane", "Leo", "Ruby", "Oscar", "Maya"]
    
    for i in range(min(count, len(names))):
        loc = random.choice(LOCATIONS)
        v_skills = random.sample(SKILLS, random.randint(1, 3))
        
        volunteers.append({
            "name": names[i],
            "skills": ", ".join(v_skills),
            "availability": random.choice(["Weekends", "Full-time", "Mon-Wed", "Evenings"]),
            "location": loc["name"],
            "lat": loc["lat"] + random.uniform(-0.02, 0.02),
            "lon": loc["lon"] + random.uniform(-0.02, 0.02)
        })
    return pd.DataFrame(volunteers)

if __name__ == "__main__":
    data_dir = "C:/Users/thvta/.gemini/antigravity/scratch/community_insight/data"
    os.makedirs(data_dir, exist_ok=True)
    
    issues_df = generate_issues(100)
    issues_df.to_csv(os.path.join(data_dir, "sample_issues.csv"), index=False)
    
    vols_df = generate_volunteers(30)
    vols_df.to_csv(os.path.join(data_dir, "sample_volunteers.csv"), index=False)
    
    print(f"Generated sample data in {data_dir}")
