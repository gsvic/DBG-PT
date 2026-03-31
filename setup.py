from setuptools import setup, find_packages

setup(
    name="dbgpt",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "dbgpt": ["resources/config.ini"],
        "dbgpt.benchmarks": ["resources/queries/tpch/*.sql", "resources/queries/job/*.sql"],
    },
    install_requires=[
        "openai>=1.0.0",
        "psycopg2",
        "mysql-connector-python",
        "streamlit>=1.35.0",
        "pandas",
        "langchain-core",
        "langchain-openai",
        "langgraph",
        "tiktoken",
        "pydantic",
    ],
)
