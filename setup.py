from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extensions = package_files('useTEM/extensions')
servers = package_files('useTEM/servers')

files = extensions+servers+['*', '*/*', '*/*/*']

print(servers)

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='useTEM',
    url='https://github.com/subangstrom/useTEM',
    author='James LeBeau',
    author_email='lebeau@mit.edu',
    # Needed to actually package something

    packages=find_packages(),
    package_data={
        # If any package contains *.ui, include it:
        '':  files},

               #ext_modules=[Extension('extensions', ['*'])],
    # Needed for dependencies
    install_requires=['pyqt5', 'comtypes', 'yapsy', 'bibtexparser', 'numpy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GPLv3',
    description='Universal Scripting Engine for TEM, a framework and gui to simplify scripting for the transmission electron microscope.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),

)