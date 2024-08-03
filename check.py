#!/usr/bin/env python3

import yaml
import subprocess
import requests
import os
import sys

clang_format = "clang-format"
exit_code = 0

if len(sys.argv) == 3 and sys.argv[1] == "--clang-format-version":
    clang_format = "./bin/clang-format"
    use_version = sys.argv[2]
    print(f"Will use version: {use_version}")
    dl = f"https://github.com/muttleyxd/clang-tools-static-binaries/releases/download/master-f7f02c1d/clang-format-{use_version}_linux-amd64"

    try:
        os.mkdir("bin")
    except:
        pass

    print("Downloading clang-format")
    resp = requests.get(dl)
    if resp.status_code != 200:
        raise Exception(f"Non-200 status code received: {resp.status_code}")
    with open(clang_format, "wb") as f:
        f.write(resp.content)
    os.chmod(clang_format, 0o755)
elif len(sys.argv) == 2 and sys.argv[1] == "--use-docker":
    # clang-format version on my machine is 14. Use Docker.
    clang_format = ["docker", "run", "--rm", "xianpengshen/clang-tools:18", "clang-format"]

if not isinstance(clang_format, list):
    clang_format = [clang_format]

# --style LLVM is specified, as LLVM is the default style.
output = subprocess.check_output(clang_format + ["--style", "LLVM", "--dump-config"])
latest_format = yaml.safe_load(output)

with open(".clang-format", "r") as f:
    curr_format = yaml.safe_load(f)

ignore = [
    # clang-format version 14 doesn't support thiese options.
    # TODO: When clang-format version gets increased, stop ignoring these.
    "AlignConsecutiveShortCaseStatements",
    "AllowBreakBeforeNoexceptSpecifier",
    "AllowShortCompoundRequirementOnASingleLine",
    "BreakAdjacentStringLiterals",
    "BreakAfterAttributes",
    "BreakBeforeConceptDeclarations",
    "BreakBeforeInlineASMColon",
    "IndentRequiresClause",
    "InsertBraces",
    "InsertNewlineAtEOF",
    "IntegerLiteralSeparator",
    "KeepEmptyLinesAtEOF",
    "LineEnding",
    "PenaltyBreakScopeResolution",
    "RemoveParentheses",
    "RemoveSemicolon",
    "RequiresClausePosition",
    "SkipMacroDefinitionBody",
    "RequiresExpressionIndentation",
    "SpaceBeforeParensOptions.AfterPlacementOperator",
    "SpaceBeforeParensOptions.AfterRequiresInClause",
    "SpaceBeforeParensOptions.AfterRequiresInExpression",
    "SpacesInParens",
    "SpacesInParensOptions",
    # Default style is already LLVM.
    "BasedOnStyle",
    # Not used
    "IncludeCategories",
    # Skip Java, JavaScript, JSON and Verilog. This .clang-format is for C++.
    "BreakArrays",
    "BreakAfterJavaFieldAnnotations",
    "JavaScriptQuotes",
    "JavaScriptWrapImports",
    "SortJavaStaticImport",
    "SpaceBeforeJsonColon",
    "VerilogBreakBetweenInstancePorts",
]

def browse_dict(key: str, latest: dict, curr: dict):
    global exit_code
    global ignore

    for latest_key, latest_value in latest.items():
        sub_key = key
        if sub_key != "":
            sub_key += "."
        sub_key += latest_key

        if sub_key in ignore:
            continue
        
        if latest_key not in curr:    
            print(f"New config option: {sub_key}")
            exit_code = 1
            continue
        
        curr_value = curr[latest_key]
        if isinstance(latest_value, dict) and isinstance(curr_value, dict):
            browse_dict(sub_key, latest_value, curr_value)
        elif isinstance(latest_value, list) and isinstance(curr_value, list):
            for el_latest in latest_value:
                if el_latest not in curr_value:
                    print(f"New element: {el_latest} in array {sub_key}")
                    exit_code = 1


browse_dict("", latest_format, curr_format)
exit(exit_code)
