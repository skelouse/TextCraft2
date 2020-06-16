try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'DESC',
    'author': 'Skelouse',
    'url': 'www.skelouse.com',
    'download_url': 'www.skelouse.com',
    'author_email': 'stoltenberg.works@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'NAME'
}

setup(**config)
