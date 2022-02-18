from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='wwshc',
    version='0.0.11',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='JoJoJux',
    author_email="wwshc@jojojux.de",
    url="https://wwshc.jojojux.de/",
    project_urls={
        "Bug Tracker": "https://wwshc.jojoux.de/bugs",
    },
    package_dir={'': '.'},
    packages=["wwshc"],
    py_modules=[],
    python_requires='>=3.7, <4'
)
