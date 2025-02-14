from setuptools import setup, find_packages

setup(
    name="my_processor",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'script_runner=script_runner.cli:main',
            'sr=script_runner.cli:main',
        ],
    },
)
