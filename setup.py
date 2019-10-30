import io
import re
from setuptools import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

with io.open('battenberg_gitlab/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


install_requires = [
    'battenberg>=0.2.0',
    'click>=1.6.0',
    'python-gitlab>=1.12.0',
    # You'll also need to install libgit2 to get this to work.
    # See instructions here: https://www.pygit2.org/install.html
    'pygit2>=0.28.0'
]

setup(
    name='battenberg-gitlab',
    version=version,
    description="Automatically running battenberg on a series of Gitlab repos.",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    author="Zillow",
    url='https://github.com/zillow/battenberg-gitlab',
    project_urls={
        "Documentation": "https://github.com/zillow/battenberg-gitlab/README.md",
        "Changelog": "https://github.com/zillow/battenberg-gitlab/HISTORY.md",
        "Code": "https://github.com/zillow/battenberg-gitlab",
        "Issue tracker": "https://github.com/zillow/battenberg-gitlab/issues",
    },
    packages=[
        'battenberg_gitlab',
    ],
    package_dir={'battenberg_gitlab': 'battenberg_gitlab'},
    include_package_data=True,
    install_requires=install_requires,
    license="Apache Software License 2.0",
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'battenberg_gitlab=battenberg_gitlab.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    python_requires=">=3.6*",
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'flake8', 'codecov']
    }
)
