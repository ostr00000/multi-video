from setuptools import find_packages, setup

setup(
    name='multi-video',
    version=0.4,
    python_requires='>=3.8',
    description='Tool to run many video at same time.',
    packages=find_packages(exclude=("*test*",)),
    entry_points={'console_scripts': [
        'multi-video = multi_video.__main__:main',
    ]},
    package_dir={"": "lib"},
    install_requires=[
        'PyQt5', 'decorator', 'boltons', 'python-mpv', 'more-itertools',
        'pyqt-settings @ git+https://github.com/ostr00000/pyqt-settings@master#egg=pyqt-settings',
    ],
    extras_require={'dev': ['matplotlib']},
)
