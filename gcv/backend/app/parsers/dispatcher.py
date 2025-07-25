from app.parsers import burpsuite_parser

PARSERS = {
    "burpsuite": burpsuite_parser,
}

def get_parser(tool: str):
    """
    Get the parser for a given tool.
    """
    parser = PARSERS.get(tool)
    if not parser:
        raise ValueError(f"Tool not supported: {tool}")
    return parser
