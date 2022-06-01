import os
from setuptools import setup
import re


# A handful of variables that are used a couple of times.
github_url = 'https://github.com/TeamMsgExtractor/msg-explorer'
main_module = 'msg_explorer'

# Read in the description from README.
with open('README.rst', 'rb') as stream:
    long_description = stream.read().decode('utf-8').replace('\r', '')

# Get the version this way to avoid import issues.
version_re = re.compile("__version__ = '(?P<version>[0-9\\.]*)'")
with open('msg_explorer/__init__.py', 'r') as stream:
    contents = stream.read()
match = version_re.search(contents)
version = match.groupdict()['version']

# Read in the dependencies from the virtualenv requirements file.
dependencies = []
filename = os.path.join('requirements.txt')
with open(filename, 'r') as stream:
    for line in stream:
        package = line.strip().split('#')[0]
        if package:
            dependencies.append(package)

setup(
    name=main_module,
    version=version,
    description="A GUI program to allow for exploring MSG files using extract-msg.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=github_url,
    download_url='%s/archives/master' % github_url,
    author='Destiny Peterson',
    author_email='arceusthe@gmail.com',
    license='GPL',
    packages=[main_module],
    py_modules=[main_module],
    entry_points={'console_scripts': ['msg_explorer = msg_explorer.main:mainRunner',]},
    include_package_data=True,
    install_requires=dependencies,
)
