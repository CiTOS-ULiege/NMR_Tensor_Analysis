<<<<<<< HEAD
from setuptools import setup, find_packages

setup(
    name='nmr_tensor_analysis',
    version='0.1.0',
    description='NMR tensor decomposition and analysis tools',
    authors='Claire Muzyka (Main Developer)' and 'Jean-Christophe M. Monbaliu (Principal Investigator)',
    author_email='cmuzyka@uliege.be',
    packages=find_packages(),
    python_requires='>=3.10',
    entry_points={
    'console_scripts': [
        'nmr-kinetic-analysis = main:main'
    ]
},
    include_package_data=True,
    package_data={
        'nmr_tensor_analysis': ['data/*.xlsx']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
=======
from setuptools import setup, find_packages

setup(
    name='nmr_tensor_analysis',
    version='0.1.0',
    description='NMR tensor decomposition and analysis tools',
    authors='Claire Muzyka (Main Developer)' and 'Jean-Christophe M. Monbaliu (Principal Investigator)',
    author_email='cmuzyka@uliege.be',
    packages=find_packages(),
    python_requires='>=3.10',
    entry_points={
    'console_scripts': [
        'nmr-kinetic-analysis = main:main'
    ]
},
    include_package_data=True,
    package_data={
        'nmr_tensor_analysis': ['data/*.xlsx']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
>>>>>>> 3ba84e62b0f35f5867a08fc7304572a01fd8909d
