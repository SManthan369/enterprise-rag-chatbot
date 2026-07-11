from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):

    pdf = Path(file_path)

    if not pdf.exists():
        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    if pdf.stat().st_size == 0:
        raise ValueError(
            f"PDF is empty: {file_path}"
        )

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents