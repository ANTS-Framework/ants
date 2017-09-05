from setuptools import setup


setup(
    name='antsclient',
    version='1.0.0',
    description='ANTS Framework client',
    url='https://ants-framework.github.io/',
    author=['Balz Aschwanden', 'Jan Welker',
            'Client Services Team of the University of Basel IT Services'],
    author_email=['balz.aschwanden@unibas.ch', 'jan.welker@unibas.ch'],
    license='GPLv3',
    scripts=['bin/ants', 'bin/inventory_ad', 'bin/inventory_default'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='client antsFramework ansiblePull unibas',
    #packages=find_packages(),
    packages=['antslib'],
    install_requires=['ansible', 'ldap3'],
    data_files=[('/usr/local/ants/', ['etc/ants.cfg'])],
    #python_requires='>=2.7, <3'
)
