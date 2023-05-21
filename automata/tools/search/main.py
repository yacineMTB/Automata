import os
from argparse import ArgumentParser
from typing import Dict, cast

# from automata.tools.search.call_graph import CallGraph
# from automata.tools.search.local_types import Descriptor
from automata.tools.search.symbol_converter import SymbolConverter
from automata.tools.search.symbol_graph import SymbolGraph
from automata.tools.search.symbol_parser import parse_uri_to_symbol
from automata.tools.search.symbol_searcher import SymbolSearcher

if __name__ == "__main__":
    symbol_prefix = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065"
    test_path = "automata.configs.automata_agent_configs"
    test_symbol = parse_uri_to_symbol("%s `%s`/AutomataAgentConfig#" % (symbol_prefix, test_path))

    argparse = ArgumentParser()
    argparse.add_argument("-i", type=str, dest="index", help="path to index file", required=True)
    args = argparse.parse_args()

    file_dir = os.path.dirname(os.path.abspath(__file__))

    symbol_converter = SymbolConverter()
    symbol_graph = SymbolGraph(os.path.join(file_dir, args.index), symbol_converter)
    symbol_searcher = SymbolSearcher(symbol_converter, symbol_graph)

    # Dump all available files in the symbol graph
    print("-" * 200)
    print("Fetching all available files in SymbolGraph")
    files = symbol_graph.get_all_files()
    for file in files:
        print("File Path >> %s" % (file.path))
    print("-" * 200)

    # Dump all available symbols defined along test path
    print("-" * 200)
    print("Fetching all defined symbols along %s" % (test_path))
    available_symbols = symbol_graph.get_defined_symbols_along_path(test_path)
    for symbol in available_symbols:
        print("Defined Symbol >> %s" % (symbol))

    print("-" * 200)

    # Get the context for the test symbol
    print("-" * 200)
    print("Dumping symbol context for %s" % (test_symbol))
    print(symbol_graph.get_symbol_context(test_symbol))
    print("-" * 200)

    # Find references of the test symbol
    print("-" * 200)
    print("Searching for references of the symbol %s" % (test_symbol))
    search_result_0: Dict = cast(
        Dict, symbol_searcher.process_query("type:symbol %s" % (test_symbol.uri))
    )
    for file_path in search_result_0.keys():
        print("File Path >> %s" % (file_path))
        for reference in search_result_0[file_path]:
            print("Reference >> %s" % (reference))
    print("-" * 200)

    # Find source code for the test symbol
    print("-" * 200)
    print("Searching for source code for symbol %s" % (test_symbol))
    search_result_1: str = cast(
        str, symbol_searcher.process_query("type:source %s" % (test_symbol.uri))
    )
    print("Source Code: ", search_result_1)
    print("-" * 200)

    # Find exact matches for abbrievated test symbol
    print("-" * 200)
    abbv_test_symbol = "AutomataAgentConfig"
    print("Searching for exact matches of the filter %s" % (abbv_test_symbol))
    search_result_2 = symbol_searcher.process_query("type:exact %s" % (abbv_test_symbol))
    print("Search result: ", search_result_2)
    print("-" * 200)

    # Perform a find and replace on the test find symbol below
    print("-" * 200)
    test_find = "AutomataAgentConfigFactory"
    test_replace = "__Automata__Agent__Config__Factory__"
    print("Performing find on %s and replacing with %s" % (test_find, test_replace))
    do_write = False
    counts = symbol_searcher.process_query(
        "type:replace %s %s %s" % (test_find, test_replace, do_write)
    )
    print("In Mem Replacements: ", counts)
    print("-" * 200)
