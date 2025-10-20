"""
Job/Internship Fetcher using JSearch API (RapidAPI).
Searches for jobs based on skills extracted from resume.
"""
import requests


def fetch_jobs_by_skills(skills, jsearch_api_key, max_results=10, job_roles=None):
    """
    Fetch job listings from JSearch API based on skills and roles.
    
    Args:
        skills (list): List of skills to search for
        jsearch_api_key (str): RapidAPI JSearch API key
        max_results (int): Maximum number of job results to return
        job_roles (list): Optional list of suitable job roles
        
    Returns:
        list: Job listings with title, company, location, description, apply_link
    """
    try:
        # JSearch API endpoint
        url = "https://jsearch.p.rapidapi.com/search"
        
        # Build a wide search query
        if job_roles and len(job_roles) > 0:
            # Take first role and clean it - remove Junior/Senior/etc.
            role = job_roles[0]
            for prefix in ["Junior", "Senior", "Mid-level", "Lead", "Principal", "Entry-level", "Entry Level"]:
                role = role.replace(prefix, "").strip()
            
            # Extract key technology from skills for broader search
            tech_keywords = []
            for skill in skills[:5]:  # Check top 5 skills
                if skill.lower() in ['python', 'java', 'javascript', 'react', 'node', 'nodejs', 'angular', 'vue']:
                    tech_keywords.append(skill)
            
            # Combine role + tech for wide search
            if tech_keywords:
                query = f"{role} {tech_keywords[0]}"
            else:
                query = role
        else:
            # Fallback: use top skill
            query = skills[0] if skills else "software developer"
        
        print(f"🔍 Searching jobs with query: '{query}'")
        
        headers = {
            "X-RapidAPI-Key": jsearch_api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        params = {
            "query": f"{query} India",  # Add India to search
            "page": "1",
            "num_pages": "1",
            "date_posted": "all",
            "remote_jobs_only": "false",
            "country": "in"  # Filter for India
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"📡 JSearch API Response Status: {response.status_code}")
        
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✅ JSearch API returned {len(data.get('data', []))} jobs")
        
        # Extract relevant job information
        jobs = []
        if "data" in data and len(data["data"]) > 0:
            for job in data["data"][:max_results]:
                jobs.append({
                    "title": job.get("job_title", "N/A"),
                    "company": job.get("employer_name", "N/A"),
                    "location": job.get("job_city", "Remote") + ", " + job.get("job_country", ""),
                    "description": job.get("job_description", "No description available")[:300] + "...",
                    "apply_link": job.get("job_apply_link", "#"),
                    "employment_type": job.get("job_employment_type", "N/A")
                })
        
        return jobs
    
    except requests.exceptions.RequestException as e:
        # If API fails, return sample jobs as fallback
        if "403" in str(e) or "401" in str(e):
            print("⚠️  JSearch API key issue - returning sample jobs")
            return _get_sample_jobs(query)
        raise Exception(f"Error fetching jobs from JSearch API: {str(e)}")
    
    except Exception as e:
        raise Exception(f"Error processing job data: {str(e)}")


def _get_sample_jobs(query):
    """Return sample job listings when API is unavailable (India-focused)."""
    # Create search-friendly query
    search_query = query.replace(" ", "-").lower()
    
    return [
        {
            "title": f"{query}",
            "company": "Tech Mahindra",
            "location": "Bangalore, India",
            "description": f"We are looking for a talented {query} to join our team. This role involves working on cutting-edge projects with modern technologies. Great benefits, competitive salary, and growth opportunities...",
            "apply_link": f"https://www.naukri.com/{search_query}-jobs-in-bangalore",
            "employment_type": "Full-time"
        },
        {
            "title": f"Software Developer",
            "company": "Infosys",
            "location": "Hyderabad, India",
            "description": "Join our dynamic team building scalable applications for global clients. We value creativity, problem-solving, and continuous learning. Work with cutting-edge technologies...",
            "apply_link": "https://www.naukri.com/software-developer-jobs-in-hyderabad",
            "employment_type": "Full-time"
        },
        {
            "title": f"{query} - Intern",
            "company": "Flipkart",
            "location": "Bangalore, India",
            "description": "Amazing internship opportunity for students to learn and grow. Work with experienced mentors on real-world e-commerce projects. Stipend provided. PPO opportunity available...",
            "apply_link": f"https://www.internshala.com/internships/{search_query}-internship-in-bangalore/",
            "employment_type": "Internship"
        },
        {
            "title": "Backend Engineer",
            "company": "Paytm",
            "location": "Noida, India",
            "description": "Build robust backend systems and APIs for India's leading fintech platform. Experience with databases, cloud platforms, and microservices architecture preferred. Exciting startup culture...",
            "apply_link": "https://www.naukri.com/backend-engineer-jobs-in-noida",
            "employment_type": "Full-time"
        },
        {
            "title": "Full Stack Developer",
            "company": "Zomato",
            "location": "Gurugram, India",
            "description": "Create amazing food-tech experiences that millions use daily. Strong knowledge of modern JavaScript frameworks, Node.js, and databases required. Fast-paced environment...",
            "apply_link": "https://www.naukri.com/full-stack-developer-jobs-in-gurgaon",
            "employment_type": "Full-time"
        },
        {
            "title": f"{query} Trainee",
            "company": "TCS",
            "location": "Pune, India",
            "description": "Entry-level position for fresh graduates in India's leading IT company. Comprehensive training program with opportunities to work on global projects. Industry-best learning experience...",
            "apply_link": f"https://www.naukri.com/{search_query}-trainee-jobs-in-pune",
            "employment_type": "Full-time"
        }
    ]
