from setuptools import find_packages, setup

setup(
    name='multi-video',
    version='0.5',
    python_requires='>=3.8',
    description='Tool to run many video at same time.',

    package_dir={'': 'lib'},
    packages=find_packages(exclude=("*test*",)),
    package_data={'': ['*.svg', '*.jpg']},
    entry_points={'console_scripts': ['multi-video = multi_video.__main__:main']},

    install_requires=[
        'PyQt5', 'decorator', 'boltons', 'python-mpv', 'more-itertools',
        'pyqt-settings @ git+https://github.com/ostr00000/pyqt-settings@master#egg=pyqt-settings',
    ],
    extras_require={'dev': ['matplotlib']},
)
