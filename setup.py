from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read

setup(
    name='antsclient',
    version='1.0.0',
    description='ANTS Framework client',
    url='https://ants-framework.github.io/',
    author='Client Services Team of the University of Basel IT Services',
    license='GPLv3',
    scripts=['ants.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='client antsFramework ansiblePull unibas',
    packages=find_packages(exclude=['*.pyc', 'linux', 'macos']),
    install_requires=['ansilbe', 'ldap3', 'subprocess', 'argparse', 'logging',
                      'ssl', 'datetime'],
    python_requires='>=2.7.*'
)
