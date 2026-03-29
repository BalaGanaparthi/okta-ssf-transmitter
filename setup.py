"""
Setup configuration for SSF Transmitter
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ssf-transmitter",
    version="1.0.0",
    author="SSF Transmitter Team",
    author_email="support@example.com",
    description="Shared Signals Framework Transmitter for Okta",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ssf-transmitter",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "ssf_transmitter": [
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js",
        ],
    },
    entry_points={
        "console_scripts": [
            "ssf-transmitter=src.ssf_transmitter.app:create_app",
        ],
    },
)
