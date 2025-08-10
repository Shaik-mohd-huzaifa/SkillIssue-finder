"""
Data models for the MCP GitHub Issue Matcher.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class UserSkills(BaseModel):
    """User's programming skills and experience."""
    languages: List[str] = Field(description="Programming languages the user knows")
    technologies: List[str] = Field(description="Technologies, frameworks, and tools")
    experience_level: str = Field(description="beginner, intermediate, advanced, or expert")
    github_stats: Optional[Dict[str, Any]] = Field(default=None, description="GitHub profile statistics")

class GitHubIssue(BaseModel):
    """GitHub issue with relevance scoring."""
    id: int = Field(description="GitHub issue ID")
    number: int = Field(description="Issue number in repository")
    title: str = Field(description="Issue title")
    body: str = Field(description="Issue description/body")
    url: str = Field(description="Issue URL")
    repository_name: str = Field(description="Full repository name (owner/repo)")
    repository_url: str = Field(description="Repository URL")
    labels: List[str] = Field(description="Issue labels")
    created_at: str = Field(description="Issue creation timestamp")
    updated_at: str = Field(description="Issue last update timestamp")
    difficulty: str = Field(description="Estimated difficulty level")
    matched_skills: List[str] = Field(description="Skills that matched this issue")
    relevance_score: float = Field(description="Relevance score based on user skills")

class SkillMatchRequest(BaseModel):
    """Request model for matching issues by skills."""
    skills: List[str] = Field(description="List of programming skills/languages")
    experience_level: Optional[str] = Field(default="intermediate", description="Experience level")
    issue_types: Optional[List[str]] = Field(
        default=["good first issue", "help wanted"],
        description="Types of issues to search for"
    )
    max_results: Optional[int] = Field(default=20, description="Maximum number of results")

class UsernameMatchRequest(BaseModel):
    """Request model for matching issues by GitHub username."""
    username: str = Field(description="GitHub username to analyze")
    issue_types: Optional[List[str]] = Field(
        default=["good first issue", "help wanted"],
        description="Types of issues to search for"
    )
    max_results: Optional[int] = Field(default=20, description="Maximum number of results")

class IssueMatchResponse(BaseModel):
    """Response model for issue matching results."""
    success: bool = Field(description="Whether the operation was successful")
    issues: List[GitHubIssue] = Field(description="List of matching issues")
    total_found: int = Field(description="Total number of issues found")
    user_skills: Optional[UserSkills] = Field(default=None, description="Analyzed user skills")
    message: str = Field(description="Response message")
    error: Optional[str] = Field(default=None, description="Error message if any")

class MCPToolCall(BaseModel):
    """MCP tool call structure."""
    name: str = Field(description="Tool name")
    arguments: Dict[str, Any] = Field(description="Tool arguments")

class MCPToolResult(BaseModel):
    """MCP tool result structure."""
    content: List[Dict[str, Any]] = Field(description="Tool result content")
    isError: Optional[bool] = Field(default=False, description="Whether this is an error result")
