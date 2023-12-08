from setuptools import setup, find_packages

setup(
    name='Flux Player',
    version='2.0.0',
    packages=find_packages(),
    description='The official engine for playing Flux cartridges in code-running LLMs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Adam Grant',
    author_email='hello@adamgrant.me',
    url='https://github.com/adamjgrant/fluxplayer',
    install_requires=[
        'pyyaml',
        'sys',
        'os',
        'importlib.util',
    ],
    classifiers=[
        # Choose classifiers from: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
