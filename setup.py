from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extensions = package_files('useTEM/extensions')

files = extensions+['*', '*/*', '*/*/*']

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='usetem',
    url='https://github.com/subangstrom/usetem',
    author='James LeBeau',
    author_email='lebeau@mit.edu',
    # Needed to actually package something
    packages=find_packages(),

    package_data={
        # If any package contains *.ui, include it:
        '':  files},

               #ext_modules=[Extension('extensions', ['*'])],
    # Needed for dependencies
    install_requires=['pyqt5', 'yapsy', 'bibtexparser', 'numpy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GPLv3',
    description='Universal Scripting Engine for TEM, a workflow gui.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),

)