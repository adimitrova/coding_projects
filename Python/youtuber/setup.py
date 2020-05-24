#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python setup.py sdist bdist_wheel
"""

import setuptools

setuptools.setup(
    name='youtuber',
    packages=setuptools.find_packages(),
    scripts=['main'],
    version=0.1,
    description="Download Youtube video and/or audio by scanning a whole Playlist and getting everything from it.",
    keywords=["API", "YouTube", "youtube", "download", "video"],
    author="Ani Dimitrova",
    author_email="a.dimmitrovaa@gmail.com",
    url="https://github.com/adimitrova/coding_projects/tree/development/Python/youtuber/",
    extras_require={
        'youtube-dl-backend': ["youtube-dl"],
        },
    package_data={"": ["LICENSE", "dummy_readme_todelete.rst", "CHANGELOG", "AUTHORS"]},
    include_package_data=True,
    license='LGPLv3',
    long_description=open("dummy_readme_todelete.rst").read()
)
