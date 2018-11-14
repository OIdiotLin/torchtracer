import setuptools
import torchtracer

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name=torchtracer.__name__,
    version=torchtracer.__version__,
    author='OIdiotLin',
    author_email='oidiotlin@gmail.com',
    maintainer='OIdiotLin',
    maintainer_email='oidiotlin@gmail.com',
    description='A python package for visualization and storage management in a pytorch AI task.',
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/OIdiotLin/torchtracer',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'matplotlib',
        'numpy',
    ]
)
