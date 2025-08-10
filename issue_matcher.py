"""
GitHub issue matcher that finds relevant issues based on user skills.
"""
import asyncio
import logging
from typing import Dict, List, Optional, Set
import aiohttp
from github import Github
from github.GithubException import GithubException
import os
from datetime import datetime, timedelta

from models import UserSkills, GitHubIssue
from config import Config

logger = logging.getLogger(__name__)

class IssueMatcher:
    """Matches GitHub issues with user skills and preferences."""
    
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github = Github(self.github_token) if self.github_token else Github()
        
        # Popular repositories for different languages/technologies
        self.popular_repos = {
            "python": ["python/cpython", "pallets/flask", "django/django", "fastapi/fastapi"],
            "javascript": ["microsoft/vscode", "facebook/react", "vuejs/vue", "angular/angular"],
            "java": ["spring-projects/spring-boot", "elastic/elasticsearch", "apache/kafka"],
            "go": ["kubernetes/kubernetes", "golang/go", "docker/docker", "prometheus/prometheus"],
            "rust": ["rust-lang/rust", "actix/actix-web", "tokio-rs/tokio"],
            "typescript": ["microsoft/TypeScript", "nestjs/nest", "typeorm/typeorm"],
            "c++": ["microsoft/calculator", "opencv/opencv", "tensorflow/tensorflow"],
            "ruby": ["rails/rails", "jekyll/jekyll", "github/gitignore"],
            "php": ["laravel/laravel", "symfony/symfony", "composer/composer"],
            "swift": ["apple/swift", "vapor/vapor", "Alamofire/Alamofire"],
            "kotlin": ["JetBrains/kotlin", "square/okhttp", "InsertKoinIO/koin"]
        }
    
    async def find_matching_issues(
        self, 
        user_skills: UserSkills, 
        issue_types: Optional[List[str]] = None,
        max_results: int = 20
    ) -> List[GitHubIssue]:
        """
        Find GitHub issues that match user's skills.
        
        Args:
            user_skills: User's programming skills and experience
            issue_types: Types of issues to search for (e.g., "good first issue")
            max_results: Maximum number of issues to return
            
        Returns:
            List of matching GitHub issues with relevance scores
        """
        if issue_types is None:
            issue_types = ["good first issue", "help wanted", "bug", "enhancement"]
        
        all_issues = []
        
        try:
            # Search by languages
            for language in user_skills.languages[:5]:  # Limit to top 5 languages
                language_issues = await self._search_issues_by_language(
                    language, issue_types, max_results // len(user_skills.languages[:5])
                )
                all_issues.extend(language_issues)
            
            # Search by technologies
            for tech in user_skills.technologies[:3]:  # Limit to top 3 technologies
                tech_issues = await self._search_issues_by_technology(
                    tech, issue_types, max_results // max(len(user_skills.technologies[:3]), 1)
                )
                all_issues.extend(tech_issues)
            
            # Remove duplicates and score issues
            unique_issues = self._remove_duplicates(all_issues)
            scored_issues = self._score_issues(unique_issues, user_skills)
            
            # Sort by relevance score and return top results
            scored_issues.sort(key=lambda x: x.relevance_score, reverse=True)
            return scored_issues[:max_results]
            
        except Exception as e:
            logger.error(f"Error finding matching issues: {e}")
            return []
    
    async def _search_issues_by_language(
        self, 
        language: str, 
        issue_types: List[str], 
        limit: int
    ) -> List[GitHubIssue]:
        """Search for issues in repositories that use a specific language."""
        issues = []
        
        try:
            # Search in popular repositories for this language
            repos_to_search = self.popular_repos.get(language.lower(), [])
            
            # Also search generally by language
            query_parts = [f"language:{language}"]
            
            for issue_type in issue_types:
                query_parts.append(f'label:"{issue_type}"')
            
            query = " ".join(query_parts) + " state:open"
            
            search_results = self.github.search_issues(
                query=query,
                sort="updated",
                order="desc"
            )
            
            count = 0
            for issue in search_results:
                if count >= limit:
                    break
                
                try:
                    github_issue = await self._convert_to_github_issue(issue, language)
                    if github_issue:
                        issues.append(github_issue)
                        count += 1
                except Exception as e:
                    logger.debug(f"Error processing issue {issue.number}: {e}")
                    continue
            
            # Search in specific popular repositories
            for repo_name in repos_to_search[:3]:  # Limit to 3 popular repos
                try:
                    repo = self.github.get_repo(repo_name)
                    repo_issues = repo.get_issues(
                        state="open",
                        labels=[label for label in issue_types if label in ["good first issue", "help wanted", "bug"]]
                    )
                    
                    repo_count = 0
                    for issue in repo_issues:
                        if repo_count >= 5:  # Limit per repository
                            break
                        
                        github_issue = await self._convert_to_github_issue(issue, language)
                        if github_issue:
                            issues.append(github_issue)
                            repo_count += 1
                            
                except Exception as e:
                    logger.debug(f"Error searching repo {repo_name}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error searching issues by language {language}: {e}")
        
        return issues
    
    async def _search_issues_by_technology(
        self, 
        technology: str, 
        issue_types: List[str], 
        limit: int
    ) -> List[GitHubIssue]:
        """Search for issues related to a specific technology or framework."""
        issues = []
        
        try:
            # Build search query
            query_parts = [f'"{technology}" in:title,body']
            
            for issue_type in issue_types:
                query_parts.append(f'label:"{issue_type}"')
            
            query = " ".join(query_parts) + " state:open"
            
            search_results = self.github.search_issues(
                query=query,
                sort="updated",
                order="desc"
            )
            
            count = 0
            for issue in search_results:
                if count >= limit:
                    break
                
                try:
                    github_issue = await self._convert_to_github_issue(issue, technology)
                    if github_issue:
                        issues.append(github_issue)
                        count += 1
                except Exception as e:
                    logger.debug(f"Error processing issue {issue.number}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching issues by technology {technology}: {e}")
        
        return issues
    
    async def _convert_to_github_issue(self, issue, matched_skill: str) -> Optional[GitHubIssue]:
        """Convert GitHub API issue to our GitHubIssue model."""
        try:
            # Skip pull requests
            if hasattr(issue, 'pull_request') and issue.pull_request:
                return None
            
            # Get labels
            labels = [label.name for label in issue.labels] if hasattr(issue, 'labels') else []
            
            # Determine difficulty
            difficulty = self._determine_difficulty(labels, issue.body or "")
            
            # Get repository info
            repo = issue.repository
            
            return GitHubIssue(
                id=issue.id,
                number=issue.number,
                title=issue.title,
                body=issue.body or "",
                url=issue.html_url,
                repository_name=repo.full_name,
                repository_url=repo.html_url,
                labels=labels,
                created_at=issue.created_at.isoformat(),
                updated_at=issue.updated_at.isoformat(),
                difficulty=difficulty,
                matched_skills=[matched_skill],
                relevance_score=0.0  # Will be calculated later
            )
            
        except Exception as e:
            logger.debug(f"Error converting issue: {e}")
            return None
    
    def _determine_difficulty(self, labels: List[str], body: str) -> str:
        """Determine issue difficulty based on labels and content."""
        labels_lower = [label.lower() for label in labels]
        body_lower = body.lower()
        
        # Check for explicit difficulty labels
        if any(label in labels_lower for label in ["good first issue", "beginner", "easy", "starter"]):
            return "beginner"
        elif any(label in labels_lower for label in ["intermediate", "medium"]):
            return "intermediate"
        elif any(label in labels_lower for label in ["hard", "expert", "complex", "difficult"]):
            return "expert"
        elif any(label in labels_lower for label in ["help wanted"]):
            return "intermediate"
        elif any(label in labels_lower for label in ["bug"]):
            return "intermediate"
        elif any(label in labels_lower for label in ["enhancement", "feature"]):
            return "intermediate"
        
        # Analyze body content for complexity indicators
        complexity_indicators = {
            "beginner": ["simple", "easy", "basic", "straightforward", "minor"],
            "expert": ["complex", "advanced", "architecture", "performance", "optimization", "refactor"]
        }
        
        for difficulty, indicators in complexity_indicators.items():
            if any(indicator in body_lower for indicator in indicators):
                return difficulty
        
        return "intermediate"  # Default
    
    def _remove_duplicates(self, issues: List[GitHubIssue]) -> List[GitHubIssue]:
        """Remove duplicate issues from the list."""
        seen_ids = set()
        unique_issues = []
        
        for issue in issues:
            if issue.id not in seen_ids:
                seen_ids.add(issue.id)
                unique_issues.append(issue)
        
        return unique_issues
    
    def _score_issues(self, issues: List[GitHubIssue], user_skills: UserSkills) -> List[GitHubIssue]:
        """Score issues based on relevance to user skills."""
        for issue in issues:
            score = 0.0
            
            # Skill matching score
            matched_skills = set()
            
            # Check title and body for skill mentions
            content = (issue.title + " " + issue.body).lower()
            
            for language in user_skills.languages:
                if language.lower() in content:
                    score += 2.0
                    matched_skills.add(language)
            
            for tech in user_skills.technologies:
                if tech.lower() in content:
                    score += 1.5
                    matched_skills.add(tech)
            
            # Label-based scoring
            for label in issue.labels:
                label_lower = label.lower()
                if "good first issue" in label_lower and user_skills.experience_level in ["beginner", "intermediate"]:
                    score += 3.0
                elif "help wanted" in label_lower:
                    score += 2.0
                elif "bug" in label_lower:
                    score += 1.0
                elif "enhancement" in label_lower or "feature" in label_lower:
                    score += 1.5
            
            # Difficulty matching
            if issue.difficulty == user_skills.experience_level:
                score += 2.0
            elif (issue.difficulty == "beginner" and user_skills.experience_level in ["intermediate", "advanced"]) or \
                 (issue.difficulty == "intermediate" and user_skills.experience_level in ["advanced", "expert"]):
                score += 1.0
            
            # Recency bonus
            try:
                updated_date = datetime.fromisoformat(issue.updated_at.replace('Z', '+00:00'))
                days_old = (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days
                if days_old <= 7:
                    score += 1.0
                elif days_old <= 30:
                    score += 0.5
            except:
                pass
            
            issue.relevance_score = score
            issue.matched_skills = list(matched_skills)
        
        return issues
