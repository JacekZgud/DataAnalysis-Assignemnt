import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Final_Assignment",
    version="0.0.1",
    author="Jacek Zgud",
    author_email="jacek.zgud2@gmail.com",
    description="Assignment package for Python in data science course",
    url="https://github.com/JacekZgud/Final_Assignment.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
    )
