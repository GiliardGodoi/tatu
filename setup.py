from setuptools import setup, find_packages

setup(
    name='tatu',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyPDF2',
        'requests',
        'rich', 'click'
    ],
    entry_points={
        'console_scripts': [
            'tatu = src.main:cli',
        ],
    },
)