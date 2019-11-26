from setuptools import setup, find_packages

setup(
    name='Suggest Taxonomy Group',
    author='Team Narwhal',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'elasticsearch', 'certifi'
    ]
)
