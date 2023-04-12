import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lts-mqemailnotifier",
    version="0.0.1",
    author="Valdeva Crema",
    author_email="valdeva_crema@harvard.edu",
    description="A set of utilities for placing a message onto a queue for an emailer listener to receive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.huit.harvard.edu/harvard-lts/mq_email_notifier",
    packages=setuptools.find_packages(),
    install_requires=[
        'stomp.py==8.0.1',
        'pytest'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        # Include all *.json files in any package
        "": ["*.json"],
    }
)
