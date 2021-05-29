import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lolite",
    version="0.0.2",
    author="Nathan Kewley",
    author_email="nathan.kewley@gmail.com",
    description="Azure Bicep Deployment Orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NathanKewley/lolite",
    project_urls={
        "Bug Tracker": "https://github.com/NathanKewley/lolite/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'lolite = lolite:lolite',
        ],
    },    
)