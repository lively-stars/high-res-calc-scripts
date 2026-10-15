import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hra", # Replace with your own username
    version="0.1",
    author="Valeriy Vasilyev, Dusan Vukadinovic",
    # author_email="vukadinovic@mps.mpg.de",
    description="Python package for high-resolution spectral line analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://gitlab.gwdg.de/dusan.vukadinovic01/atoms_invert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix based",
    ],
    python_requires='>=3.10',
)