"""
Setup script untuk Modular Telegram Bot
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
if (this_directory / "requirements.txt").exists():
    with open(this_directory / "requirements.txt", "r", encoding="utf-8") as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="modular-telegram-bot",
    version="1.0.0",
    author="Modular Bot Team",
    author_email="your.email@example.com",
    description="A modular Telegram bot with plugin system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/modular-telegram-bot",
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
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
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "modular-bot=bot:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="telegram bot modular plugin python",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/modular-telegram-bot/issues",
        "Source": "https://github.com/YOUR_USERNAME/modular-telegram-bot",
        "Documentation": "https://github.com/YOUR_USERNAME/modular-telegram-bot/blob/main/README.md",
    },
)
