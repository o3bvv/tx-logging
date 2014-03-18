from setuptools import setup, find_packages

setup(
    name='tx-logging',
    version='1.0.0',
    description='Extends Twisted log facilities.',
    license='GPL v2',
    url='https://github.com/oblalex/tx-logging',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[i.strip() for i in open("requirements.pip").readlines()],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Free for non-commercial use',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Framework :: Twisted',
    ],
)
