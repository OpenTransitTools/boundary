import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'ott.utils',
    'gtfsdb[postgresql]',

    'pyshp',

    'pyramid',
    'pyramid_tm',
    'pyramid_exclog',
    'waitress',
]

dev_extras = []

extras_require = dict(
    dev=dev_extras,
)

setup(
    name='ott.boundary',
    version='0.1.0',
    description='Open Transit Tools - Web API / Controller',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Open Transit Tools",
    author_email="info@opentransittools.org",

    dependency_links = [
        'git+https://github.com/OpenTransitTools/utils.git#egg=ott.utils-0.1.0',
        'git+https://github.com/OpenTransitTools/gtfsdb.git#egg=gtfsdb-0.1.7',
    ],

    license="Mozilla-derived (http://opentransittools.com)",
    url='http://opentransittools.com',
    keywords='ott, otp, services, transit',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=requires,
    test_suite="ott.boundary.tests",
    entry_points="""
        [paste.app_factory]
        main = ott.boundary.pyramid.app:main
        [console_scripts]
        load_db = ott.boundary.control.loader:load_db
    """,
)
