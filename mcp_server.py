"""
MCP Server implementation for GitHub issue matching.
"""
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from github_analyzer import GitHubAnalyzer
from issue_matcher import IssueMatcher
from models import SkillMatchRequest, IssueMatchResponse, UserSkills
from config import Config

logger = logging.getLogger(__name__)

class MCPGitHubIssueServer:
    """MCP server for matching GitHub issues with user skills."""
    
    def __init__(self):
        self.app = FastAPI(
            title="MCP GitHub Issue Matcher",
            description="Match users with relevant GitHub issues based on skills",
            version="1.0.0"
        )
        self.github_analyzer = GitHubAnalyzer()
        self.issue_matcher = IssueMatcher()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes for the MCP server."""
        
        @self.app.get("/")
        async def root():
            return {
                "name": "MCP GitHub Issue Matcher",
                "version": "1.0.0",
                "description": "Match users with relevant GitHub issues based on skills"
            }
        
        @self.app.post("/match-issues-by-skills", response_model=IssueMatchResponse)
        async def match_issues_by_skills(request: SkillMatchRequest):
            """Match issues based on provided skills."""
            try:
                if not request.skills:
                    raise HTTPException(status_code=400, detail="Skills list cannot be empty")
                
                user_skills = UserSkills(
                    languages=request.skills,
                    technologies=[],
                    experience_level=request.experience_level or "intermediate"
                )
                
                issues = await self.issue_matcher.find_matching_issues(
                    user_skills=user_skills,
                    issue_types=request.issue_types or ["good first issue", "help wanted"],
                    max_results=request.max_results or 20
                )
                
                return IssueMatchResponse(
                    success=True,
                    issues=issues,
                    total_found=len(issues),
                    message=f"Found {len(issues)} matching issues"
                )
                
            except Exception as e:
                logger.error(f"Error matching issues by skills: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/match-issues-by-username", response_model=IssueMatchResponse)
        async def match_issues_by_username(request: Dict[str, Any]):
            """Match issues based on GitHub username analysis."""
            try:
                username = request.get("username")
                if not username:
                    raise HTTPException(status_code=400, detail="Username is required")
                
                # Analyze user's GitHub profile
                user_skills = await self.github_analyzer.analyze_user_skills(username)
                if not user_skills:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Could not analyze skills for user '{username}'"
                    )
                
                # Find matching issues
                issues = await self.issue_matcher.find_matching_issues(
                    user_skills=user_skills,
                    issue_types=request.get("issue_types", ["good first issue", "help wanted"]),
                    max_results=request.get("max_results", 20)
                )
                
                return IssueMatchResponse(
                    success=True,
                    issues=issues,
                    total_found=len(issues),
                    user_skills=user_skills,
                    message=f"Found {len(issues)} matching issues for @{username}"
                )
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error matching issues by username: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/analyze-user/{username}")
        async def analyze_user_skills(username: str):
            """Analyze a GitHub user's skills without matching issues."""
            try:
                user_skills = await self.github_analyzer.analyze_user_skills(username)
                if not user_skills:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Could not find or analyze user '{username}'"
                    )
                
                return {
                    "success": True,
                    "username": username,
                    "skills": user_skills.dict(),
                    "message": f"Successfully analyzed skills for @{username}"
                }
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error analyzing user skills: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "mcp-github-issue-matcher"}
    
    async def run(self):
        """Run the MCP server."""
        config = uvicorn.Config(
            app=self.app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
