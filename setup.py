from setuptools import setup

setup(
    name='xyy',
    author='Gabriel Montagné Láscaris-Comneno',
    author_email='gabriel@tibas.london',
    license='MIT',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'xyy = xyy.__main__:main'
        ]
    }
)
