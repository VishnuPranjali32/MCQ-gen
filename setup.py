from setuptools import find_packages, setup

setup(
    name="mcq_generator",
    version="0.0.1",
    author="S.Vishnu",
    author_email="vishnu.pranjali@gmail.com",
    description="Automated MCQ generator using LangChain and Hugging Face",
    install_requires=[
        "langchain==0.3.4",
        "langchain-community==0.3.3",
        "streamlit==1.39.0",
        "python-dotenv==1.0.1",
        "huggingface_hub==0.26.0",
    ],
    packages=find_packages(),
)