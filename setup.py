from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Universal Scripting Engine for TEM (USETEM)',
    url='https://github.com/subangstrom/useTEM',
    author='James LeBeau',
    author_email='lebeau@mit.edu',
    # Needed to actually package something
    packages=['useTEM'],
    # Needed for dependencies
    install_requires=['pyqt5, comtypes, yapsy, bibtexparser, numpy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GPLv3',
    description='A framework and gui to simplify scripting for the transmission electron microscope.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)