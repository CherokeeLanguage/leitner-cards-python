import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
        name="leitner_cards",
        version="2021.11.07.01",
        description="Basic Leitner Cards Implementation",
        long_description=README,
        long_description_content_type="text/markdown",
        author="Michael Conrad",
        author_email="m.conrad.202@gmail.com",
        license="MIT",
        classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python"
        ],
        packages=setuptools.find_packages(),
        python_requires=">=3.9"
)
