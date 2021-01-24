from setuptools import setup, find_packages


setup(
    name='mailbankdata',
    version='0.0.1',
    author='Rodrigo Mendez',
    author_email='rodmendezp@gmail.com',
    description='Retrieve bank transactions data from mails',
    url='https://github.com/rodmendezp/mail-bank-audit',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-api-python-client'
    ]
)
