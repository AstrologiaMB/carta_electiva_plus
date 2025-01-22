from setuptools import setup, find_packages

setup(
    name="astro_package",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        'immanuel==1.3.2',
        'pandas==2.2.2',
        'numpy==1.26.4',
        'pyswisseph==2.10.3.2',
        'python-dateutil==2.9.0',
        'pytz==2024.1',
        'timezonefinder==5.2.0',
    ],
    author="AstrologiaMB",
    description="Análisis de cartas astrológicas y momentos óptimos",
    python_requires=">=3.11",
)
