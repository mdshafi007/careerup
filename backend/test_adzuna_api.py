"""
Test script to verify Adzuna API integration
Tests fetching Indian jobs and internships with real apply links
"""
from job_fetcher_adzuna import fetch_jobs_adzuna
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.getenv('ADZUNA_APP_KEY')

def test_adzuna_api():
    print("=" * 70)
    print("🧪 Testing Adzuna API Integration")
    print("=" * 70)
    print(f"\n📋 App ID: {ADZUNA_APP_ID}")
    print(f"🔑 App Key: {ADZUNA_APP_KEY[:10]}..." if ADZUNA_APP_KEY else "❌ Not set")
    print()
    
    # Test 1: Python Developer
    print("\n" + "─" * 70)
    print("TEST 1: Python Developer")
    print("─" * 70)
    try:
        jobs = fetch_jobs_adzuna(
            skills=["Python", "Django", "Flask"],
            adzuna_app_id=ADZUNA_APP_ID,
            adzuna_app_key=ADZUNA_APP_KEY,
            max_results=5,
            job_roles=["Python Developer"]
        )
        
        print(f"\n✅ Retrieved {len(jobs)} results:")
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Type: {job['employment_type']}")
            print(f"   Apply: {job['apply_link'][:80]}...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    # Test 2: Full Stack Developer
    print("\n" + "─" * 70)
    print("TEST 2: Full Stack Developer (Internships included)")
    print("─" * 70)
    try:
        jobs = fetch_jobs_adzuna(
            skills=["React", "Node.js", "JavaScript"],
            adzuna_app_id=ADZUNA_APP_ID,
            adzuna_app_key=ADZUNA_APP_KEY,
            max_results=5,
            job_roles=["Full Stack Developer"]
        )
        
        print(f"\n✅ Retrieved {len(jobs)} results:")
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Type: {job['employment_type']}")
            print(f"   Apply: {job['apply_link'][:80]}...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Adzuna API Test Complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_adzuna_api()
