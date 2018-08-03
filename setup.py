import setuptools
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.rst')) as f:
    long_description = f.read()

with open('bin/ants', 'r') as f:
    for line in f:
        if '__version__ =' in line:
            version = line.split(' ')[2].rstrip().replace("'", "")

setuptools.setup(
    name='ants_client',


    # Versions should comply with PEP440. For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,


    description='ANTS Framework client',
    long_description=long_description,
    url='https://ants-framework.github.io/',
    author=['Balz Aschwanden', 'Jan Welker',
            'Client Services Team of the University of Basel IT Services'],
    author_email='balz.aschwanden@unibas.ch, jan.welker@unibas.ch',
    license='GPLv3',
    scripts=['bin/ants'],
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: Documentation :: Sphinx',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='client antsFramework ansible ansiblePull unibas',
    packages=['antslib', 'antslib.inventory'],
    install_requires=[
        'ansible==2.6.1',
        'ldap3==2.5',
        'logstash==0.1.dev0',
    ],
    package_data={
        'antslib': ['etc/ants.cfg'],
        'antslib.inventory': ['inventory_default', 'inventory_ad'],
    },
    python_requires='>=2.7, <3'
)
