from setuptools import setup, find_packages


setup(
    name='lanutils',
    version='0.1',
    packages=find_packages(),
    description='A handy tool that make your day to day programming much easier. ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='rlan',
    author_email='brianlanbo@gmail.com',
    url='https://gitlab.com/rlan/lanutils',
    install_requires=[
        "numpy",
        "scipy",
        "tqdm",
        "matplotlib",
        "pytest",
    ],
)