"""
GitHub profile analyzer for extracting user skills and experience.
"""
import asyncio
import logging
from typing import Dict, List, Optional, Set
import aiohttp
from github import Github
from github.GithubException import GithubException
import os

from models import UserSkills
from skill_extractor import SkillExtractor
from config import Config

logger = logging.getLogger(__name__)

class GitHubAnalyzer:
    """Analyzes GitHub profiles to extract user skills and experience."""
    
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            logger.warning("No GitHub token provided. API rate limits will be severely restricted.")
        
        self.github = Github(self.github_token) if self.github_token else Github()
        self.skill_extractor = SkillExtractor()
    
    async def analyze_user_skills(self, username: str) -> Optional[UserSkills]:
        """
        Analyze a GitHub user's skills based on their repositories and activity.
        
        Args:
            username: GitHub username to analyze
            
        Returns:
            UserSkills object with extracted skills or None if analysis fails
        """
        try:
            user = self.github.get_user(username)
            
            # Get user's repositories
            repos = list(user.get_repos(type="owner", sort="updated"))[:50]  # Limit to recent 50 repos
            
            if not repos:
                logger.warning(f"No repositories found for user {username}")
                return None
            
            # Extract skills from repositories
            languages = await self._extract_languages(repos)
            technologies = await self._extract_technologies(repos)
            experience_level = await self._estimate_experience_level(user, repos)
            
            # Get additional context from profile
            bio_skills = self._extract_skills_from_bio(user.bio or "")
            
            # Combine all skills
            all_languages = languages.union(bio_skills.get("languages", set()))
            all_technologies = technologies.union(bio_skills.get("technologies", set()))
            
            return UserSkills(
                languages=list(all_languages),
                technologies=list(all_technologies),
                experience_level=experience_level,
                github_stats={
                    "public_repos": user.public_repos,
                    "followers": user.followers,
                    "following": user.following,
                    "account_age_years": (user.updated_at - user.created_at).days / 365.25
                }
            )
            
        except GithubException as e:
            logger.error(f"GitHub API error for user {username}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error analyzing user {username}: {e}")
            return None
    
    async def _extract_languages(self, repos) -> Set[str]:
        """Extract programming languages from repositories."""
        languages = set()
        
        for repo in repos:
            try:
                repo_languages = repo.get_languages()
                for lang in repo_languages.keys():
                    if lang and lang.lower() not in ["html", "css"]:  # Filter out markup languages
                        languages.add(lang.lower())
            except Exception as e:
                logger.debug(f"Error getting languages for repo {repo.name}: {e}")
                continue
        
        return languages
    
    async def _extract_technologies(self, repos) -> Set[str]:
        """Extract technologies and frameworks from repository names, descriptions, and topics."""
        technologies = set()
        
        for repo in repos:
            try:
                # Extract from repository name
                repo_techs = self.skill_extractor.extract_from_text(repo.name or "")
                technologies.update(repo_techs)
                
                # Extract from description
                if repo.description:
                    desc_techs = self.skill_extractor.extract_from_text(repo.description)
                    technologies.update(desc_techs)
                
                # Extract from topics
                if hasattr(repo, 'get_topics'):
                    topics = repo.get_topics()
                    for topic in topics:
                        if self.skill_extractor.is_technology(topic):
                            technologies.add(topic.lower())
                            
            except Exception as e:
                logger.debug(f"Error extracting technologies from repo {repo.name}: {e}")
                continue
        
        return technologies
    
    async def _estimate_experience_level(self, user, repos) -> str:
        """Estimate user's experience level based on GitHub activity."""
        try:
            account_age = (user.updated_at - user.created_at).days / 365.25
            total_repos = user.public_repos
            followers = user.followers
            
            # Calculate a simple experience score
            score = 0
            
            # Account age factor
            if account_age >= 5:
                score += 3
            elif account_age >= 2:
                score += 2
            elif account_age >= 1:
                score += 1
            
            # Repository count factor
            if total_repos >= 50:
                score += 3
            elif total_repos >= 20:
                score += 2
            elif total_repos >= 5:
                score += 1
            
            # Followers factor (social proof)
            if followers >= 100:
                score += 2
            elif followers >= 20:
                score += 1
            
            # Repository activity analysis
            active_repos = [repo for repo in repos[:10] if repo.updated_at and 
                          (user.updated_at - repo.updated_at).days <= 365]
            
            if len(active_repos) >= 5:
                score += 2
            elif len(active_repos) >= 2:
                score += 1
            
            # Determine experience level
            if score >= 8:
                return "expert"
            elif score >= 5:
                return "advanced"
            elif score >= 2:
                return "intermediate"
            else:
                return "beginner"
                
        except Exception as e:
            logger.debug(f"Error estimating experience level: {e}")
            return "intermediate"
    
    def _extract_skills_from_bio(self, bio: str) -> Dict[str, Set[str]]:
        """Extract skills mentioned in user's bio."""
        if not bio:
            return {"languages": set(), "technologies": set()}
        
        bio_lower = bio.lower()
        extracted_techs = self.skill_extractor.extract_from_text(bio)
        
        # Separate languages from technologies
        languages = set()
        technologies = set()
        
        for tech in extracted_techs:
            if self.skill_extractor.is_programming_language(tech):
                languages.add(tech)
            else:
                technologies.add(tech)
        
        return {
            "languages": languages,
            "technologies": technologies
        }
