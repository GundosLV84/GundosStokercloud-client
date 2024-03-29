import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GundosStokercloud-client",
    version="0.1.2",
    author="GundosLV84",
    author_email="till84@gmail.com",
    description="Python stokercloud client modified",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GundosLV84/GundosStokercloud-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    tests_require=['pytest'],
)
