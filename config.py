"""
Configuration settings for the MCP GitHub Issue Matcher.
"""
import os
from typing import List, Dict

class Config:
    """Configuration class for the application."""
    
    # GitHub API settings
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_API_BASE_URL = "https://api.github.com"
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 60
    GITHUB_API_RATE_LIMIT = 5000  # Per hour with token, 60 without
    
    # Search settings
    DEFAULT_MAX_RESULTS = 20
    MAX_REPOS_PER_LANGUAGE = 5
    MAX_ISSUES_PER_REPO = 10
    
    # Skill extraction settings
    MIN_REPO_STARS = 0  # Minimum stars for repositories to consider
    MAX_REPOS_TO_ANALYZE = 50  # Maximum repositories to analyze per user
    
    # Issue filtering
    SUPPORTED_ISSUE_TYPES = [
        "good first issue",
        "help wanted", 
        "bug",
        "enhancement",
        "feature",
        "documentation",
        "question",
        "beginner-friendly"
    ]
    
    DIFFICULTY_LEVELS = [
        "beginner",
        "intermediate", 
        "advanced",
        "expert"
    ]
    
    # Experience level thresholds
    EXPERIENCE_THRESHOLDS = {
        "beginner": {
            "min_account_age_months": 0,
            "min_repos": 0,
            "min_followers": 0
        },
        "intermediate": {
            "min_account_age_months": 6,
            "min_repos": 5,
            "min_followers": 5
        },
        "advanced": {
            "min_account_age_months": 24,
            "min_repos": 20,
            "min_followers": 20
        },
        "expert": {
            "min_account_age_months": 60,
            "min_repos": 50,
            "min_followers": 100
        }
    }
    
    # Popular repositories by language (for issue searching)
    POPULAR_REPOSITORIES = {
        "python": [
            "python/cpython",
            "pallets/flask", 
            "django/django",
            "fastapi/fastapi",
            "requests/requests",
            "psf/black",
            "pytorch/pytorch",
            "scikit-learn/scikit-learn",
            "pandas-dev/pandas",
            "numpy/numpy"
        ],
        "javascript": [
            "microsoft/vscode",
            "facebook/react",
            "vuejs/vue",
            "angular/angular", 
            "nodejs/node",
            "expressjs/express",
            "webpack/webpack",
            "babel/babel",
            "prettier/prettier",
            "eslint/eslint"
        ],
        "typescript": [
            "microsoft/TypeScript",
            "nestjs/nest",
            "typeorm/typeorm",
            "angular/angular",
            "ionic-team/ionic-framework",
            "grafana/grafana",
            "apollographql/apollo-server",
            "typestack/class-validator"
        ],
        "java": [
            "spring-projects/spring-boot",
            "elastic/elasticsearch", 
            "apache/kafka",
            "google/guava",
            "square/retrofit",
            "ReactiveX/RxJava",
            "junit-team/junit5",
            "mockito/mockito"
        ],
        "go": [
            "kubernetes/kubernetes",
            "golang/go",
            "docker/docker",
            "prometheus/prometheus",
            "helm/helm",
            "hashicorp/terraform",
            "gin-gonic/gin",
            "gorilla/mux"
        ],
        "rust": [
            "rust-lang/rust",
            "actix/actix-web",
            "tokio-rs/tokio",
            "serde-rs/serde",
            "clap-rs/clap",
            "diesel-rs/diesel",
            "hyperium/hyper",
            "rustls/rustls"
        ],
        "swift": [
            "apple/swift",
            "vapor/vapor", 
            "Alamofire/Alamofire",
            "SwiftyJSON/SwiftyJSON",
            "realm/realm-swift",
            "onevcat/Kingfisher",
            "apple/swift-package-manager"
        ],
        "kotlin": [
            "JetBrains/kotlin",
            "square/okhttp",
            "InsertKoinIO/koin",
            "google/accompanist",
            "detekt/detekt",
            "mockk/mockk",
            "kotest/kotest"
        ],
        "ruby": [
            "rails/rails",
            "jekyll/jekyll",
            "github/gitignore",
            "rubocop/rubocop",
            "rspec/rspec",
            "sinatra/sinatra",
            "capistrano/capistrano"
        ],
        "php": [
            "laravel/laravel",
            "symfony/symfony",
            "composer/composer",
            "PHPUnit/phpunit",
            "guzzle/guzzle",
            "doctrine/orm",
            "phpstan/phpstan"
        ],
        "c++": [
            "microsoft/calculator",
            "opencv/opencv",
            "tensorflow/tensorflow",
            "facebook/folly",
            "google/googletest",
            "nlohmann/json",
            "fmtlib/fmt"
        ],
        "c#": [
            "dotnet/core",
            "aspnet/AspNetCore",
            "NUnit/nunit",
            "AutoMapper/AutoMapper",
            "StackExchange/Dapper",
            "JamesNK/Newtonsoft.Json",
            "serilog/serilog"
        ]
    }
    
    @classmethod
    def get_popular_repos_for_skill(cls, skill: str) -> List[str]:
        """Get popular repositories for a given skill/language."""
        return cls.POPULAR_REPOSITORIES.get(skill.lower(), [])
    
    @classmethod
    def is_valid_issue_type(cls, issue_type: str) -> bool:
        """Check if an issue type is supported."""
        return issue_type.lower() in cls.SUPPORTED_ISSUE_TYPES
    
    @classmethod
    def is_valid_difficulty(cls, difficulty: str) -> bool:
        """Check if a difficulty level is valid."""
        return difficulty.lower() in cls.DIFFICULTY_LEVELS
