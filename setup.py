from setuptools import setup, find_packages

long_description = ""

setup(
    name='piper_web',
    version='0.11',
    description='Piper CI web interface using REST api',
    long_description=long_description,
    packages=find_packages(),
    package_dir={'piper_web': 'piper_web'},
    author='Martin Franc',
    author_email='francma6@fit.cvut.cz',
    keywords='lxd,ci,runner',
    license='Public Domain',
    url='https://github.com/francma/piper-ci-web',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
          'piper_lxd = piper_lxd.run:run'
        ]
    },
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'flask',
        'requests',
    ],
    # tests_require=[
    # ],
)