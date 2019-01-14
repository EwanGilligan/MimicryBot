from setuptools import setup
from setuptools import find_packages

setup(name='mimicrybot',
      version='0.1',
      description='A discord bot that can generate a random sentence for a user, based on their previous messages.',
      url='https://github.com/EwanGilligan/MimicryBot',
      author='Ewan Gilligan',
      author_email='eg207@st-andrews.ac.uk',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'discord',
          'markovify',
      ],
      zip_safe=False)