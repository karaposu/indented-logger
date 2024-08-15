from setuptools import setup, find_packages

setup(
    name='indented_logger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    description='A custom logger with indentation support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/karaposu/indented_logger',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
