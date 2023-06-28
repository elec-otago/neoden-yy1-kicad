from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(name='neoden_kicad',
    version='1.0.0a2',
    description='Converter for Neoden Pick and Place machine',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='http://github.com/elec-otago/neoden-yy1-kicad',
    author='Tim Molteno, Phill Brown',
    author_email='tim@elec.ac.nz',
    license='GPLv3',
    install_requires=[],
    packages=['neoden_kicad'],
    scripts=['bin/neoden_kicad'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Programming Language :: Python :: 3',
        "Intended Audience :: End Users/Desktop",  ])
