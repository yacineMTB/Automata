import logging
from typing import List, Optional

from automata.core.agent.tools.agent_tool import AgentTool
from automata.core.base.tool import Tool
from automata.core.coding.py_coding.py_utils import NO_RESULT_FOUND_STR
from automata.core.coding.py_coding.retriever import PyCodeRetriever

logger = logging.getLogger(__name__)


class PyCodeRetrieverTool(AgentTool):
    """
    PyCodeRetrieverTool
    A class for interacting with the PythonIndexer API, which provides functionality to read
    the code state of a of local Python files.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes a PyCodeRetrieverTool object with the given inputs.

        Args:
        - py_retriever (PyCodeRetriever): A PyCodeRetriever object which allows inspecting of local code.

        Returns:
        - None
        """
        self.code_retriever: PyCodeRetriever = kwargs.get("py_retriever", PyCodeRetriever())
        self.model = kwargs.get("model") or "gpt-4"
        self.temperature = kwargs.get("temperature") or 0.7
        self.verbose = kwargs.get("verbose") or False
        self.stream = kwargs.get("stream") or True

    def build(self) -> List[Tool]:
        """
        Builds the tools associated with the python code retriever.

        Returns:
            List[Tool]: The list of built tools.
        """
        return [
            Tool(
                name="py-retriever-retrieve-code",
                func=lambda query: self._run_indexer_retrieve_code(*query),
                description=f"Returns the code of the python package, module, standalone function, class,"
                f" or method at the given python path, without docstrings."
                f' If no match is found, then "{NO_RESULT_FOUND_STR}" is returned.\n\n'
                f'For example - suppose the function "my_function" is defined in the file "my_file.py" located in the main working directory,'
                f"Then the correct tool input for the parser follows:\n"
                f"  - tool_args\n"
                f"    - my_file\n"
                f"    - None\n"
                f"    - my_function\n\n"
                f"Suppose instead the file is located in a subdirectory called my_directory,"
                f" then the correct tool input for the parser is:\n"
                f"  - tool_args\n    - my_directory.my_file\n    - my_function\n\n"
                f"Lastly, if the function is defined in a class, MyClass, then the correct tool input is:\n"
                f"  - tool_args\n    - my_directory.my_file\n    - MyClass.my_function\n\n",
                return_direct=True,
                verbose=True,
            ),
            Tool(
                name="py-retriever-retrieve-docstring",
                func=lambda query: self._run_indexer_retrieve_docstring(*query),
                description=f"Identical to py-retriever-retrieve-code, except returns the docstring instead of raw code.",
                return_direct=True,
                verbose=True,
            ),
            Tool(
                name="py-retriever-retrieve-raw-code",
                func=lambda query: self._run_indexer_retrieve_raw_code(*query),
                description=f"Identical to py-retriever-retrieve-code, except returns the raw text (e.g. code + docstrings) of the module.",
                return_direct=True,
                verbose=True,
            ),
        ]

    def _run_indexer_retrieve_code(
        self, module_path: str, object_path: Optional[str] = None
    ) -> str:
        """
        PythonIndexer retrieves the code of the python package,
         module, standalone function, class, or method at the given
         python path, without docstrings.

        Args:
            - module_path (str): The path to the module to retrieve code from.
            - object_path (Optional[str]): The path to the object to retrieve code from.

        Returns:
            - str: The code of the python package, module,
              standalone function, class, or method at the given
              python path, without docstrings.
        """
        try:
            return self.code_retriever.get_source_code_without_docstrings(module_path, object_path)
        except Exception as e:
            return "Failed to retrieve code with error - " + str(e)

    def _run_indexer_retrieve_docstring(
        self, module_path: str, object_path: Optional[str] = None
    ) -> str:
        """
        PythonIndexer retrieves the docstring of the python package,
         module, standalone function, class, or method at the given
         python path, without docstrings.

         Args:
            - module_path (str): The path to the module to retrieve code from.
            - object_path (Optional[str]): The path to the object to retrieve code from.

        Returns:
            - str: The docstring of the python package, module,
        """
        try:
            result = self.code_retriever.get_docstring(module_path, object_path)
            return result
        except Exception as e:
            return "Failed to retrieve docstring with error - " + str(e)

    def _run_indexer_retrieve_raw_code(
        self, module_path: str, object_path: Optional[str] = None
    ) -> str:
        """
        PythonIndexer retrieves the raw code of the python package,
         module, standalone function, class, or method at the given
         python path, with docstrings.

        Args:
            - module_path (str): The path to the module to retrieve code from.
            - object_path (Optional[str]): The path to the object to retrieve code from.

        Returns:
            - str: The raw code of the python package, module,
        """
        try:
            result = self.code_retriever.get_source_code(module_path, object_path)
            return result
        except Exception as e:
            return "Failed to retrieve raw code with error - " + str(e)
