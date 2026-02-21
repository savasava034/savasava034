#!/usr/bin/env python3
"""
Osmanlıca Tesseract OCR - Paket Kurulum Dosyası

Bu dosya, paketi pip ile kurulabilir hale getirir.
"""

from setuptools import setup, find_packages
import os

# README'yi oku
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Gereksinimleri oku
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='osmanlica-tesseract-ocr',
    version='1.0.0',
    author='savasava034',
    author_email='',
    description='Osmanlıca (Arap harfli Türkçe) metinler için Tesseract OCR sistemi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/savasava034/savasava034',
    packages=find_packages(exclude=['tests', 'docs', 'examples']),
    py_modules=['scripts.osmanlica_ocr', 'scripts.preprocess', 'scripts.train_tesseract', 'scripts.evaluate'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'osmanlica-ocr=scripts.osmanlica_ocr:main',
            'osmanlica-preprocess=scripts.preprocess:main',
            'osmanlica-train=scripts.train_tesseract:main',
            'osmanlica-evaluate=scripts.evaluate:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt', '*.sh'],
    },
    keywords='ocr tesseract ottoman turkish arabic osmanlica',
    project_urls={
        'Bug Reports': 'https://github.com/savasava034/savasava034/issues',
        'Source': 'https://github.com/savasava034/savasava034',
        'Documentation': 'https://github.com/savasava034/savasava034/tree/main/osmanlica-tesseract',
    },
)
