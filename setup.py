"""Setup script for Instruction Analysis AI Assistant."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="instruction-analysis-ai-assistant",
    version="1.0.0",
    author="Instruction Analysis AI Assistant Contributors",
    description="A comprehensive system for analyzing and decomposing complex task instructions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewnyc2/Instruction-Analysis-AI-Assistant",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "instruction-analysis=run_analysis:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["prompts/**/*.md"],
    },
)
