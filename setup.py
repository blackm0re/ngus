import setuptools

import ngus

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='ngus',
    version=ngus.__version__,
    author=ngus.__author__,
    author_email='sgs@pichove.org',
    description='A simple HTTP server for handleing file uploads',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blackm0re/ngus',
    packages=setuptools.find_packages(),
    exclude_package_data={'': ['.gitignore']},
    entry_points={
        'console_scripts': [
            'ngus=ngus.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        ('License :: OSI Approved :: GNU General Public License v3 or later '
         '(GPLv3+)'),
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers'
    ],
    keywords='upload http httpd',
    project_urls={
        'Bug Reports': 'https://github.com/blackm0re/ngus/issues',
        'Source': 'https://github.com/blackm0re/ngus'
    },
    python_requires='>=3.6',
)
