from setuptools import setup, find_packages

setup(
    name="diet_workout_planning",
    version="0.1.0",
    description="A package for diet and workout planning",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here, e.g., 'numpy', 'pandas'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)