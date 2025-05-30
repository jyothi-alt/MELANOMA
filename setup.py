from setuptools import setup, find_packages

setup(
    name="research_capstone",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "python-dotenv",
        "Werkzeug",
        # Add other dependencies here
    ],
)