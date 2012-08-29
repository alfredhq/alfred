from setuptools import setup, find_packages


setup(
    name='alfred',
    version='0.1.dev',
    license='ISC',
    description='Alfred web app',
    url='https://github.com/alfredhq/alfred',
    author='Alfred Developers',
    author_email='team@alfredhq.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'Flask-Alfred-DB',
        'argh',
        'PyYAML',
        'Flask-Login',
        'PyGithub',
        'requests-oauth2',
    ],
    entry_points={
        'console_scripts': [
            'alfred = alfred.__main__:main'
        ],
    }
)
