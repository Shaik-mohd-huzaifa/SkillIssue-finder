# MCP GitHub Issue Matcher

## Overview

The MCP GitHub Issue Matcher is a FastAPI-based service that matches developers with relevant GitHub issues based on their programming skills and experience level. The application analyzes GitHub user profiles to extract skills from repositories and activity, then recommends appropriate open source issues for contribution. It supports both skill-based matching (where users provide their skills directly) and GitHub username analysis (where skills are automatically extracted from the user's repositories).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: FastAPI with async/await pattern for high-performance HTTP API
- **MCP Server Pattern**: Implements Model Context Protocol (MCP) server architecture for structured AI agent interactions
- **Modular Design**: Separated concerns across distinct modules:
  - `github_analyzer.py`: Extracts user skills from GitHub profiles
  - `issue_matcher.py`: Finds and scores relevant issues based on skills
  - `skill_extractor.py`: Categorizes programming languages and technologies
  - `mcp_server.py`: FastAPI server implementation with MCP endpoints

### Data Models
- **Pydantic Models**: Type-safe data validation using Pydantic BaseModel
- **Skill Representation**: Structured skill categorization including languages, frameworks, databases, and cloud platforms
- **Issue Scoring**: Relevance scoring system that matches user skills to issue requirements
- **Request/Response Models**: Standardized API contracts for skill matching and username analysis

### GitHub Integration
- **PyGithub Library**: Official GitHub API client for repository and issue access
- **Rate Limiting**: Built-in respect for GitHub API rate limits (5000 requests/hour with token)
- **Async HTTP**: aiohttp for concurrent API calls to improve performance
- **Skill Extraction**: Automated analysis of repository languages, technologies, and contribution patterns

### Configuration Management
- **Environment-based Config**: Centralized configuration using environment variables
- **Flexible Settings**: Configurable rate limits, search parameters, and filtering options
- **Security**: GitHub token management through environment variables

### Issue Matching Algorithm
- **Multi-criteria Scoring**: Combines language matching, repository popularity, and issue characteristics
- **Difficulty Classification**: Automatic difficulty assessment based on issue labels and repository metrics
- **Popular Repository Database**: Curated lists of high-quality repositories per programming language
- **Flexible Filtering**: Support for various issue types (good first issue, help wanted, bug fixes, etc.)

## External Dependencies

### GitHub API
- **Primary Data Source**: GitHub REST API v3 for user profiles, repositories, and issues
- **Authentication**: GitHub personal access token for increased rate limits
- **Rate Limiting**: Respects GitHub's API rate limits (60 requests/hour without token, 5000 with token)

### Third-party Libraries
- **PyGithub**: Official GitHub API client library for Python
- **FastAPI**: Modern async web framework for building APIs
- **Pydantic**: Data validation and serialization using Python type hints
- **aiohttp**: Async HTTP client for concurrent API requests
- **uvicorn**: ASGI server for running the FastAPI application

### Runtime Environment
- **Python 3.7+**: Minimum Python version requirement
- **Async Runtime**: Asyncio-based architecture for handling concurrent operations
- **Environment Variables**: Configuration through environment variables (GITHUB_TOKEN, DEBUG, etc.)
- **Logging**: Python's built-in logging framework for debugging and monitoring

### Optional Integrations
- **Database**: Architecture supports future database integration for caching user skills and issue data
- **Monitoring**: Logging infrastructure ready for integration with monitoring services
- **Deployment**: Configured for containerized deployment with configurable host/port settings