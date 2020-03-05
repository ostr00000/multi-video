from setuptools import find_packages, setup

setup(
    name='multi-vlc',
    version=0.3,
    python_requires='>=3.8',
    description='Tool to run many vlc at same time on early prepared position.',
    packages=find_packages(exclude=("*test*",)),
    entry_points={'console_scripts': [
        'multi-vlc = multi_vlc.__main__:main',
    ]},
    package_dir={"": "lib"},
    install_requires=['PyQt5', 'decorator', 'boltons'],
    extras_require={'dev': ['matplotlib']},
)
