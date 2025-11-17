# In setup.py

from setuptools import setup, find_packages

setup(
    name='raspy-format',  # The name users will type: pip install raspy-format
    version='0.1.0',
    description='A simple, lightweight data format parser based on custom RAS rules.',
    author='Your Name',
    url='https://github.com/YourUsername/raspy-format', # Link to your GitHub repo
    packages=find_packages(), # Automatically finds the 'rasp' directory
    install_requires=[
        # List any external libraries needed (for RAS, it only needs standard libraries)
    ],
    classifiers=[
        # Standard metadata for PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

