import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lolite-test", # Replace with your own username
    version="0.0.1",
    author="Nathan Kewley",
    # author_email="author@example.com",
    description="For making deploying into Azure easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NathanKewley/lolite",
    project_urls={
        "Bug Tracker": "https://github.com/NathanKewley/lolite/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="lib"),
    python_requires=">=3.6",
)