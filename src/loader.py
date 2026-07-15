from langchain_community.document_loaders import PyMuPDFLoader
import os


def load_pdf(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    loader = PyMuPDFLoader(file_path)

    documents = loader.load()

    return documents