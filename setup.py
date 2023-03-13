""" setup.py """

from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='shared_diary',
    version='0.1.0',
    description='SharedGasMileageDiary-project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/morriskrr/A-Shared-Gas-Mileage-Diary-System',
    packages=find_packages(include=['shared_diary', 'shared_diary.*']),
    install_requires=[
        'confluent-kafka==2.0.2',
        'pyqt5==5.15.9',
        'pytest'
    ],
    setup_requires=['wheel']
)