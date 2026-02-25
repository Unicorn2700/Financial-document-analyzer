## Importing libraries and files
from langchain_community.document_loaders import PyPDFLoader


## Creating custom pdf reader tool
class FinancialDocumentTool:

    @staticmethod
    def read_data_tool(path: str):
        """
        Reads and extracts text from a PDF file.
        """

        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            content = data.page_content

            # Clean extra newlines
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report