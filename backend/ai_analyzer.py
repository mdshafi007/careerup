"""
AI Resume Analyzer using LangChain + Google Gemini API.
Extracts skills, weaknesses, and suitable job roles from resume text.
"""
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def analyze_resume(resume_text, gemini_api_key):
    """
    Analyze resume text using Gemini AI via LangChain.
    
    Args:
        resume_text (str): Extracted text from resume
        gemini_api_key (str): Google Gemini API key
        
    Returns:
        dict: Analysis containing skills, weaknesses, and job roles
    """
    try:
        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.3
        )
        
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["resume_text"],
            template="""
You are an expert career counselor and resume analyst. Analyze the following resume and provide a structured JSON response.

Resume Text:
{resume_text}

Provide your analysis in the following strict JSON format (no additional text outside JSON):
{{
    "skills": ["skill1", "skill2", "skill3", ...],
    "weaknesses": ["weakness1", "weakness2", ...],
    "suitable_roles": ["role1", "role2", "role3", ...],
    "experience_level": "entry/mid/senior"
}}

Instructions:
- Extract technical and soft skills mentioned or implied
- Identify 2-4 areas for improvement (gaps in skills, missing keywords, etc.)
- Suggest 3-5 suitable job roles based on the profile
- Determine experience level based on work history

Return ONLY valid JSON, no markdown or explanations.
"""
        )
        
        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        
        # Run analysis
        response = chain.run(resume_text=resume_text)
        
        # Parse JSON response
        # Remove markdown code blocks if present
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        
        analysis = json.loads(response.strip())
        
        return analysis
    
    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        return {
            "skills": ["Unable to parse skills - review resume format"],
            "weaknesses": ["Resume format may need improvement"],
            "suitable_roles": ["General positions"],
            "experience_level": "unknown",
            "error": f"JSON parsing error: {str(e)}"
        }
    
    except Exception as e:
        raise Exception(f"Error analyzing resume: {str(e)}")
