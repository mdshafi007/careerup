"""
Adzuna Job API integration for Indian jobs.
FREE tier: 100 requests/month with real apply links.
Sign up: https://developer.adzuna.com/signup
"""
import requests


def fetch_jobs_adzuna(skills, adzuna_app_id, adzuna_app_key, max_results=10, job_roles=None):
    """
    Fetch job listings AND internships from Adzuna API (India-focused).
    Returns real, direct apply links to company websites.
    
    Args:
        skills (list): List of skills to search for
        adzuna_app_id (str): Adzuna Application ID
        adzuna_app_key (str): Adzuna Application Key
        max_results (int): Maximum number of job results (will fetch jobs + internships)
        job_roles (list): Optional list of suitable job roles
        
    Returns:
        list: Job listings and internships with REAL apply links
    """
    all_jobs = []
    
    try:
        # Build search query
        if job_roles and len(job_roles) > 0:
            role = job_roles[0]
            # Clean prefixes
            for prefix in ["Junior", "Senior", "Mid-level", "Lead", "Principal", "Entry-level", "Entry Level"]:
                role = role.replace(prefix, "").strip()
            query = role
        else:
            query = skills[0] if skills else "software developer"
        
        print(f"🔍 Searching Adzuna for jobs and internships: '{query}'")
        
        # Search 1: Regular Jobs
        jobs_url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
        jobs_params = {
            "app_id": adzuna_app_id,
            "app_key": adzuna_app_key,
            "results_per_page": max_results,
            "what": query,
            "where": "india",
            "content-type": "application/json"
        }
        
        print(f"📡 Fetching regular jobs...")
        jobs_response = requests.get(jobs_url, params=jobs_params, timeout=10)
        print(f"   Status: {jobs_response.status_code}")
        jobs_response.raise_for_status()
        jobs_data = jobs_response.json()
        
        if "results" in jobs_data and len(jobs_data["results"]) > 0:
            print(f"✅ Found {len(jobs_data['results'])} jobs")
            for job in jobs_data["results"]:
                all_jobs.append({
                    "title": job.get("title", "N/A"),
                    "company": job.get("company", {}).get("display_name", "N/A"),
                    "location": job.get("location", {}).get("display_name", "India"),
                    "description": job.get("description", "No description available")[:300] + "...",
                    "apply_link": job.get("redirect_url", "#"),
                    "employment_type": job.get("contract_type", "Full-time")
                })
        
        # Search 2: Internships
        internship_url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
        internship_params = {
            "app_id": adzuna_app_id,
            "app_key": adzuna_app_key,
            "results_per_page": max_results // 2,  # Get fewer internships
            "what": f"{query} internship",
            "where": "india",
            "content-type": "application/json"
        }
        
        print(f"📡 Fetching internships...")
        internship_response = requests.get(internship_url, params=internship_params, timeout=10)
        print(f"   Status: {internship_response.status_code}")
        internship_response.raise_for_status()
        internship_data = internship_response.json()
        
        if "results" in internship_data and len(internship_data["results"]) > 0:
            print(f"✅ Found {len(internship_data['results'])} internships")
            for job in internship_data["results"]:
                all_jobs.append({
                    "title": job.get("title", "N/A"),
                    "company": job.get("company", {}).get("display_name", "N/A"),
                    "location": job.get("location", {}).get("display_name", "India"),
                    "description": job.get("description", "No description available")[:300] + "...",
                    "apply_link": job.get("redirect_url", "#"),
                    "employment_type": "Internship"
                })
        
        if len(all_jobs) == 0:
            print("⚠️  No jobs or internships found from Adzuna")
        else:
            print(f"🎉 Total results: {len(all_jobs)} (jobs + internships)")
        
        return all_jobs[:max_results]  # Limit to max_results
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Adzuna API error: {str(e)}")
        raise Exception(f"Error fetching jobs from Adzuna API: {str(e)}")
    
    except Exception as e:
        raise Exception(f"Error processing Adzuna data: {str(e)}")
