from setuptools import setup, find_packages

setup(
    name="dev-assistant-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'dev-assistant=dev_assistant.assistant:main',
        ],
    },
    author="Your Name",
    description="CLI assistant inspired by Hitesh Sir & Piyush Garg for structured thinking",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
