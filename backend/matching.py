import math
from typing import List

def haversine_distance(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2):
        return 999.0 # Default fallback distance
    
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_match_score(issue, volunteer):
    score = 0.0
    
    # 1. Skill Relevance (Max 40 points)
    # Match issue type and description keywords with volunteer skills
    issue_keywords = set([issue.issue_type.lower()])
    desc_words = [w.strip(".,!?").lower() for w in issue.description.split() if len(w) > 3]
    issue_keywords.update(desc_words)
    
    vol_skills = set([s.strip().lower() for s in volunteer.skills.replace(",", " ").split()])
    
    match_count = len(issue_keywords.intersection(vol_skills))
    if match_count > 0:
        score += min(40, 20 + (match_count * 10))
    elif issue.issue_type.lower() in vol_skills:
        score += 30
        
    # 2. Geographic Proximity (Max 30 points)
    dist = haversine_distance(issue.lat, issue.lon, volunteer.lat, volunteer.lon)
    if dist < 2:
        score += 30
    elif dist < 5:
        score += 25
    elif dist < 10:
        score += 15
    elif dist < 20:
        score += 5
        
    # 3. Urgency Weight (Max 20 points)
    urgency_map = {"high": 20, "medium": 10, "low": 5}
    score += urgency_map.get(issue.urgency.lower(), 0)
    
    # 4. Availability Bonus (Max 10 points)
    # Simple check for 'Full-time' or high availability
    if "Full-time" in volunteer.availability or "Everyday" in volunteer.availability:
        score += 10
    elif "Weekends" in volunteer.availability and issue.urgency == "high":
        # Extra points if high urgency and weekend availability (often when needed)
        score += 5
        
    return min(100.0, score)

def match_volunteers_to_issues(issues, volunteers):
    """
    Returns a list of best matches. 
    Each match is a dict with issue_id, volunteer_id, and score.
    """
    matches = []
    # For a more sophisticated matching, we could use the Stable Marriage algorithm
    # or a maximum weight matching in a bipartite graph.
    # For this prototype, we'll use a greedy approach based on top scores.
    
    potential_matches = []
    for issue in issues:
        if issue.status != "open":
            continue
        for vol in volunteers:
            score = calculate_match_score(issue, vol)
            if score >= 40: # Threshold for a 'decent' match
                potential_matches.append({
                    "issue_id": issue.id,
                    "volunteer_id": vol.id,
                    "score": score
                })
    
    # Sort by score descending
    potential_matches.sort(key=lambda x: x['score'], reverse=True)
    
    # Greedy selection (ensure one volunteer per issue for now)
    assigned_vols = set()
    assigned_issues = set()
    
    for match in potential_matches:
        if match['issue_id'] not in assigned_issues and match['volunteer_id'] not in assigned_vols:
            matches.append(match)
            assigned_issues.add(match['issue_id'])
            # Note: We allow volunteers to be assigned to multiple issues in reality, 
            # but for this list we'll show unique primary assignments.
            assigned_vols.add(match['volunteer_id'])
            
    return matches
