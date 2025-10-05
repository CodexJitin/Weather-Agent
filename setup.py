"""
Setup configuration for codex-weather-agent PyPI package.
"""

from setuptools import setup, find_packages
import os

# Read long description from README
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Conversational weather agent with LangGraph and configurable LLMs"

# Core dependencies required for basic functionality
core_requirements = [
    "requests>=2.31.0",
    "langchain-core>=0.3.0", 
    "langgraph>=0.2.0",
    "typing-extensions>=4.7.0",
]

# Optional LLM provider dependencies
google_requirements = ["langchain-google-genai>=2.0.0"]
openai_requirements = ["langchain-openai>=0.2.0"]
anthropic_requirements = ["langchain-anthropic>=0.2.0"]

# Development dependencies
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
]

setup(
    name="codex-weather-agent",
    version="1.0.5",
    author="CodexJitin",
    author_email="contact@codexjitin.com",
    description="Conversational weather agent with LangGraph and configurable LLMs",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/CodexJitin/codex-weather-agent",
    project_urls={
        "Bug Tracker": "https://github.com/CodexJitin/codex-weather-agent/issues",
        "Documentation": "https://github.com/CodexJitin/codex-weather-agent#readme",
        "Source Code": "https://github.com/your-username/codex-weather-agent",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=core_requirements,
    extras_require={
        "google": google_requirements,
        "openai": openai_requirements,
        "anthropic": anthropic_requirements,
        "all": google_requirements + openai_requirements + anthropic_requirements,
        "dev": dev_requirements,
    },
    keywords="weather, ai, chatbot, langchain, langgraph, llm, conversation, climate",
    include_package_data=True,
    package_data={
        "codex_weather_agent": ["py.typed"],
    },
    zip_safe=False,
)