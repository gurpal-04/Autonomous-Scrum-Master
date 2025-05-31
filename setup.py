from setuptools import setup, find_packages

setup(
    name="autonomous-scrum-master",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-cloud-firestore",
        "python-dotenv",
    ],
) 