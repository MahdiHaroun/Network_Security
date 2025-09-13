from setuptools import setup, find_packages
from typing import List



requirement_lst: List[str] = []

def get_requirements() -> List[str]:
    try:
        with open("requirements.txt" , 'r') as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirement_lst


setup(
    name="Network_Security",
    version="0.0.1",
    author="Mahdi Haroun" , 
    author_email="mhd0228222@ju.edu.jo",
    packages=find_packages(),
    install_requires=get_requirements(),
)
