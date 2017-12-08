from setuptools import setup, find_packages

long_description = ""

setup(
    name='piper-web',
    version='0.11',
    description='Piper CI web interface using REST api',
    long_description=long_description,
    packages=find_packages(),
    package_dir={'piper_web': 'piper_web'},
    author='Martin Franc',
    author_email='francma6@fit.cvut.cz',
    keywords='ci,piper',
    license='MIT',
    url='https://github.com/francma/piper-ci-web',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
          'piper-web = piper_web.run:main'
        ]
    },
    install_requires=[
        'flask>=0.12',
        'requests',
        'pyyaml',
    ],
)