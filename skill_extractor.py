"""
Skill extraction utilities for identifying programming languages and technologies.
"""
import re
from typing import List, Set
import logging

logger = logging.getLogger(__name__)

class SkillExtractor:
    """Extract and categorize programming skills from text."""
    
    def __init__(self):
        self.programming_languages = {
            "python", "javascript", "java", "c++", "c#", "c", "go", "rust", "swift",
            "kotlin", "scala", "ruby", "php", "typescript", "dart", "r", "matlab",
            "perl", "lua", "haskell", "clojure", "elixir", "erlang", "f#", "pascal",
            "cobol", "fortran", "assembly", "bash", "shell", "powershell", "sql",
            "html", "css", "xml", "json", "yaml", "toml"
        }
        
        self.frameworks_libraries = {
            "react", "angular", "vue", "svelte", "django", "flask", "fastapi", "express",
            "spring", "laravel", "rails", "asp.net", "blazor", "gatsby", "next.js",
            "nuxt.js", "electron", "react-native", "flutter", "ionic", "cordova",
            "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
            "opencv", "matplotlib", "seaborn", "plotly", "d3.js", "three.js",
            "bootstrap", "tailwind", "material-ui", "ant-design", "chakra-ui",
            "jquery", "lodash", "moment.js", "axios", "redux", "mobx", "rxjs"
        }
        
        self.databases = {
            "mysql", "postgresql", "sqlite", "mongodb", "redis", "elasticsearch",
            "cassandra", "neo4j", "dynamodb", "firebase", "supabase", "prisma",
            "sequelize", "mongoose", "sqlalchemy", "hibernate", "entity-framework"
        }
        
        self.cloud_platforms = {
            "aws", "azure", "gcp", "google-cloud", "heroku", "netlify", "vercel",
            "digitalocean", "linode", "kubernetes", "docker", "jenkins", "gitlab-ci",
            "github-actions", "travis-ci", "circleci"
        }
        
        self.tools_technologies = {
            "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack",
            "discord", "figma", "sketch", "adobe", "photoshop", "illustrator",
            "webpack", "vite", "parcel", "babel", "eslint", "prettier", "jest",
            "cypress", "selenium", "postman", "insomnia", "swagger", "graphql",
            "rest", "api", "microservices", "serverless", "jamstack", "pwa",
            "spa", "ssr", "ssg", "cms", "headless", "blockchain", "web3", "nft",
            "defi", "smart-contracts", "solidity", "ethereum", "bitcoin"
        }
        
        # Combine all technology sets
        self.all_technologies = (
            self.frameworks_libraries | self.databases | 
            self.cloud_platforms | self.tools_technologies
        )
    
    def extract_from_text(self, text: str) -> Set[str]:
        """
        Extract technology keywords from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Set of identified technologies
        """
        if not text:
            return set()
        
        text_lower = text.lower()
        
        # Remove special characters and split into words
        words = re.findall(r'\b\w+(?:[.-]\w+)*\b', text_lower)
        
        # Also check for common compound terms
        compound_terms = [
            "react-native", "next.js", "vue.js", "node.js", "asp.net",
            "material-ui", "ant-design", "chakra-ui", "github-actions",
            "gitlab-ci", "travis-ci", "google-cloud"
        ]
        
        found_technologies = set()
        
        # Check individual words
        for word in words:
            if word in self.all_technologies or word in self.programming_languages:
                found_technologies.add(word)
        
        # Check compound terms
        for term in compound_terms:
            if term in text_lower:
                found_technologies.add(term)
        
        # Special handling for common abbreviations and variations
        text_variations = {
            "js": "javascript",
            "ts": "typescript",
            "py": "python",
            "cpp": "c++",
            "csharp": "c#",
            "postgres": "postgresql",
            "mongo": "mongodb",
            "k8s": "kubernetes",
            "tf": "tensorflow",
            "ml": "machine-learning",
            "ai": "artificial-intelligence",
            "nlp": "natural-language-processing",
            "cv": "computer-vision"
        }
        
        for word in words:
            if word in text_variations:
                found_technologies.add(text_variations[word])
        
        return found_technologies
    
    def is_programming_language(self, tech: str) -> bool:
        """Check if a technology is a programming language."""
        return tech.lower() in self.programming_languages
    
    def is_technology(self, tech: str) -> bool:
        """Check if a string represents a known technology."""
        return (tech.lower() in self.all_technologies or 
                tech.lower() in self.programming_languages)
    
    def categorize_skills(self, skills: List[str]) -> dict:
        """
        Categorize a list of skills into different types.
        
        Args:
            skills: List of skill strings
            
        Returns:
            Dictionary with categorized skills
        """
        categorized = {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "cloud": [],
            "tools": []
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            
            if skill_lower in self.programming_languages:
                categorized["languages"].append(skill)
            elif skill_lower in self.frameworks_libraries:
                categorized["frameworks"].append(skill)
            elif skill_lower in self.databases:
                categorized["databases"].append(skill)
            elif skill_lower in self.cloud_platforms:
                categorized["cloud"].append(skill)
            elif skill_lower in self.tools_technologies:
                categorized["tools"].append(skill)
        
        return categorized
