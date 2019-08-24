import codecs
import os
import re

from setuptools import find_packages, setup

#: Holds a list of packages to install with the binary distribution
PACKAGES = find_packages(where="src")
META_FILE = os.path.abspath("src/maya/__init__.py")
KEYWORDS = ["datetime", "timezone", "scrape", "web"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

#: Holds the runtime requirements for the end user
INSTALL_REQUIRES = [
    "humanize",
    "pytz",
    "dateparser>=0.7.0",
    "tzlocal",
    "pendulum>=2.0.2",
    "snaptime",
]
#: Holds runtime requirements and development requirements
EXTRAS_REQUIRES = {
    # extras for contributors
    "docs": ["sphinx"],
    "tests": ["freezegun", "coverage", "pytest", "pytest-mock"],
}
EXTRAS_REQUIRES["dev"] = (
    EXTRAS_REQUIRES["tests"] + EXTRAS_REQUIRES["docs"] + ["pre-commit"]
)

#: Holds the contents of the README file
with codecs.open("README.rst", encoding="utf-8") as readme:
    __README_CONTENTS__ = readme.read()


def read(metafile):
    """
    Return the contents of the given meta data file assuming UTF-8 encoding.
    """
    with codecs.open(str(metafile), encoding="utf-8") as f:
        return f.read()


def get_meta(meta, metafile):
    """
    Extract __*meta*__ from the given metafile.
    """
    contents = read(metafile)
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), contents, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


setup(
    name="maya",
    version=get_meta("version", META_FILE),
    license=get_meta("license", META_FILE),
    description=get_meta("description", META_FILE),
    long_description=__README_CONTENTS__,
    author=get_meta("author", META_FILE),
    author_email=get_meta("author_email", META_FILE),
    maintainer=get_meta("author", META_FILE),
    maintainer_email=get_meta("author_email", META_FILE),
    platforms=["Linux", "Windows", "MAC OS X"],
    url=get_meta("url", META_FILE),
    download_url=get_meta("download_url", META_FILE),
    bugtrack_url=get_meta("bugtrack_url", META_FILE),
    packages=PACKAGES,
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
)
