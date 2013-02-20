from setuptools import setup
setup(
    name = "boreas",
    version = "0.1",
    package_dir = {'': 'src'},
    packages = [
        'boreas',
        'boreas.api',
        'boreas.client',
        'boreas.utils',
        'boreas.ws',
    ],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        'requests>=1.1.0',
        'simplejson>=3.0.7',
        'tornado>=2.4.1',
    ],

    package_data = {},

    author = "Karol Majta",
    author_email = "karol@karolmajta.com",
    description = "Websocket pub/sub server for python",
    license = "JSON License",
    keywords = "websocket pub sub pubsub",
    url = "http://boreas.readthedocs.org/",
    
    entry_points = {
        'console_scripts': [
            'boreas = boreas.commands:boreas',
        ],
    }
)