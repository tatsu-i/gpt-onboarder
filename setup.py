from setuptools import setup

setup(
    name="onboarder",
    version="0.1",
    packages=["onboarder"],
    install_requires=["PyPDF2==2.12.1", "python-pptx", "python-docx", "pyyaml", "tiktoken", "click"],
    entry_points={
        "console_scripts": [
            "onboarder = onboarder.onboarder:main",
        ]
    },
)
