from setuptools import setup, find_packages

try:
    # only build rst docs for pypi when pypandoc is installed (when deploying)
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = ''

install_requires = [
    'python-telegram-bot==6.1.0',
]

extras_require = {
    'amcrest': ['amcrest==1.2.0'],
}

try:
    import configparser  # noqa: F401
except ImportError:
    install_requires.append('configparser==3.5.0')

setup(
    name='thief-snapshot',
    version='0.1.0',
    description='Detects motion with a camera and sends snapshots using a '
                'telegram chatbot if your phone is not on wifi.',
    url='https://github.com/pawl/thief-snapshot',
    author='Paul Brown',
    author_email='paul90brown+pypi@gmail.com',
    long_description=long_description,
    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'thief_snapshot = thief_snapshot.__main__:main',
            'thief_snapshot_generate_settings = thief_snapshot.copy_settings:copy_settings',
        ]
    }
)
