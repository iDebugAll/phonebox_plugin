from setuptools import find_packages, setup

from os import path
top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='phonebox_plugin',
    version='v0.0.2-beta.1',
    url='https://github.com/iDebugAll/phonebox-plugin.git',
    download_url='https://github.com/iDebugAll/phonebox-plugin/archive/vv0.0.2-beta.1.tar.gz',
    description='A phone numbers management plugin for NetBox.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Igor Korotchenkov',
    author_email='iDebugAll@gmail.com',
    install_requires=[],
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
