from setuptools import setup
from setuptools import find_packages
from dotenv import load_dotenv

load_dotenv()

setup(
    name='gratitude',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
