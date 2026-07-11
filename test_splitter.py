from src.loader import load_pdf
from src.splitter import split_documents


documents = load_pdf(
    "data/handbook.pdf"
)

chunks = split_documents(documents)


print("Total pages:", len(documents))
print("Total chunks:", len(chunks))


print("\nFirst chunk:")
print(chunks[0].page_content)