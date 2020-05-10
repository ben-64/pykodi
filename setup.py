from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='pykodi',
    version='0.64',
    description='Switch easily between subtitles/audios in a kodi video',
    long_description=long_description,
    author='ben64',
    author_email='ben64@time0ut.org',
    scripts=["pykodi.py"]
)
