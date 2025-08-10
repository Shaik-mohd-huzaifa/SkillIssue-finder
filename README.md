# MCP GitHub Issue Matcher

A FastAPI-based service that matches developers with relevant GitHub issues based on their programming skills and experience level. The application analyzes GitHub user profiles to extract skills from repositories and activity, then recommends appropriate open source issues for contribution.

## 🚀 Features

- **Skill-Based Matching**: Find issues based on programming languages and technologies you specify
- **GitHub Profile Analysis**: Automatically extract skills from your GitHub repositories and activity
- **Experience Level Matching**: Get issues appropriate for your skill level (beginner to expert)
- **Multiple Issue Types**: Support for "good first issue", "help wanted", "bug", "enhancement", and more
- **Relevance Scoring**: Issues are ranked by relevance to your skills and preferences
- **RESTful API**: Clean API endpoints with comprehensive documentation

## 🏗️ Architecture

The application follows a modular design with separated concerns:

- **FastAPI Server** (`mcp_server.py`): Main API server with MCP endpoint implementations
- **GitHub Analyzer** (`github_analyzer.py`): Extracts user skills from GitHub profiles
- **Issue Matcher** (`issue_matcher.py`): Finds and scores relevant issues based on skills
- **Skill Extractor** (`skill_extractor.py`): Categorizes programming languages and technologies
- **Data Models** (`models.py`): Pydantic models for type-safe data validation
- **Configuration** (`config.py`): Centralized configuration management

## 📋 Prerequisites

- Python 3.7 or higher
- GitHub personal access token (optional but recommended for higher rate limits)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-github-issue-matcher
```

2. Install dependencies:
```bash
pip install fastapi uvicorn pydantic aiohttp PyGithub python-multipart
```

3. (Optional) Set up environment variables:
```bash
export GITHUB_TOKEN=your_github_personal_access_token
export DEBUG=true  # For development
```

## 🚀 Running the Server

Start the server:
```bash
python main.py
```

The server will start on `http://localhost:5000`

Visit `http://localhost:5000/docs` for interactive API documentation.

## 📚 API Endpoints

### Base URL: `http://localhost:5000`

### 1. Service Information
```http
GET /
```
Returns basic service information.

### 2. Match Issues by Skills
```http
POST /match-issues-by-skills
```

**Request Body:**
```json
{
  "skills": ["python", "javascript", "react"],
  "experience_level": "intermediate",
  "issue_types": ["good first issue", "help wanted"],
  "max_results": 20
}
```

### 3. Match Issues by GitHub Username
```http
POST /match-issues-by-username
```

**Request Body:**
```json
{
  "username": "octocat",
  "issue_types": ["good first issue", "help wanted", "bug"],
  "max_results": 15
}
```

### 4. Analyze User Skills
```http
GET /analyze-user/{username}
```

Analyzes a GitHub user's skills without matching issues.

### 5. Health Check
```http
GET /health
```

## 📝 Usage Examples

### Example 1: Find Issues by Skills

```bash
curl -X POST "http://localhost:5000/match-issues-by-skills" \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["python", "django", "rest-api"],
    "experience_level": "intermediate",
    "issue_types": ["good first issue", "help wanted"],
    "max_results": 10
  }'
```

### Example 2: Analyze GitHub Profile and Find Issues

```bash
curl -X POST "http://localhost:5000/match-issues-by-username" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "octocat",
    "issue_types": ["good first issue"],
    "max_results": 5
  }'
```

### Example 3: Just Analyze Skills

```bash
curl -X GET "http://localhost:5000/analyze-user/octocat"
```

## 🔧 Configuration

### Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token (increases rate limits from 60 to 5000 requests/hour)
- `DEBUG`: Set to "true" for debug logging
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

### Supported Programming Languages

The system recognizes these programming languages:
- Python, JavaScript, TypeScript, Java, Go, Rust, Swift, Kotlin
- C++, C#, C, Ruby, PHP, Scala, Clojure, Elixir, Haskell
- And many more...

### Supported Technologies

- **Frameworks**: React, Angular, Vue, Django, Flask, FastAPI, Express, Spring Boot
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch
- **Cloud**: AWS, Azure, GCP, Docker, Kubernetes
- **Tools**: Git, Jenkins, GitHub Actions, and more

### Experience Levels

- **Beginner**: New to programming or the technology
- **Intermediate**: Some experience, comfortable with basics
- **Advanced**: Experienced, can handle complex tasks
- **Expert**: Deep expertise, can handle architecture and optimization

## 📊 Response Format

All endpoints return JSON responses with this structure:

```json
{
  "success": true,
  "issues": [
    {
      "id": 123456,
      "number": 42,
      "title": "Add authentication feature",
      "body": "We need to implement user authentication...",
      "url": "https://github.com/owner/repo/issues/42",
      "repository_name": "owner/repo",
      "repository_url": "https://github.com/owner/repo",
      "labels": ["good first issue", "python", "authentication"],
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-02T12:00:00Z",
      "difficulty": "intermediate",
      "matched_skills": ["python", "authentication"],
      "relevance_score": 8.5
    }
  ],
  "total_found": 15,
  "user_skills": {
    "languages": ["python", "javascript"],
    "technologies": ["django", "react", "postgresql"],
    "experience_level": "intermediate",
    "github_stats": {
      "public_repos": 25,
      "followers": 15,
      "following": 30,
      "account_age_years": 2.5
    }
  },
  "message": "Found 15 matching issues for @username"
}
```

## 🔍 How It Works

1. **Skill Extraction**: The system analyzes GitHub repositories to extract:
   - Programming languages from repository languages
   - Technologies from repository names, descriptions, and topics
   - Experience level from account age, repository count, and activity

2. **Issue Matching**: Issues are found by:
   - Searching GitHub for issues with relevant labels
   - Filtering by programming languages and technologies
   - Checking popular repositories for each skill

3. **Relevance Scoring**: Issues are scored based on:
   - Skill matching (languages and technologies)
   - Difficulty level alignment
   - Issue recency and activity
   - Repository popularity and quality

## 🚨 Rate Limits

- **Without GitHub Token**: 60 requests per hour
- **With GitHub Token**: 5000 requests per hour

To avoid rate limiting, provide a GitHub personal access token via the `GITHUB_TOKEN` environment variable.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- [GitHub REST API](https://docs.github.com/en/rest)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyGithub](https://github.com/PyGithub/PyGithub)

## 📞 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:5000/docs) when the server is running
2. Review the logs for error messages
3. Ensure your GitHub token (if provided) has the necessary permissions
4. Open an issue in this repository

---

**Made with ❤️ for the open source community**