from setuptools import setup, find_packages

setup(
    name="jokes",
    version="1.0.0",
    description="The Joke REST API",
    url="https://github.com/iservak/jokes",
    author="iservak",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],

    packages=find_packages(),

    install_requires=["Flask==1.1.2", "flask-restplus==0.13.0", "Flask-SQLAlchemy==2.5.1", "requests"],
)
