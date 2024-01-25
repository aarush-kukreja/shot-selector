from setuptools import setup, find_packages

setup(
    name="prompt-strategy-selector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pyyaml>=6.0',
        'scikit-learn>=1.0',
        'pandas>=1.3',
        'numpy>=1.21',
        'pytest>=7.0',
        'flask>=2.0',
        'joblib>=1.1',
        'nltk>=3.6',
        'spacy<3.7.0',  # Pin to a version known to work with Python 3.9
        'transformers>=4.0',
        'torch>=1.9'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=2.0',
            'black>=22.0',
            'flake8>=4.0',
        ],
    },
    python_requires='>=3.9,<3.10',
    entry_points={
        'console_scripts': [
            'prompt-selector=src.main:main',
        ],
    }
)
