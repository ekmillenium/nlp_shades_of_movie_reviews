from setuptools import setup, find_packages
import os

with open('requirements.txt','r') as file:
  content = file.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='nlp_shades',
      version='0.0.1',
      install_requires=requirements,
      packages=find_packages(),
      )
