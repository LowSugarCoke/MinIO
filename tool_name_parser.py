import re

class ToolNameParser:
    def __init__(self, tool_names):
        """
        Initializes a ToolNameParser object with a list of tool names and compiles a regular expression pattern
        that matches any string containing any of the tool names in the list.
        
        Args:
        - tool_names: a list of tool names
        
        Returns:
        None
        """
        self.tool_names = tool_names
        self.regex = re.compile(".*(%s).*" % "|".join(tool_names))

    def parser_file(self, file_name):
        """
        Parses a file name to extract the tool name using the regular expression pattern.
        
        Args:
        - file_name: a string representing the file name
        
        Returns:
        - If the file name contains a tool name, the tool name is returned.
        - If the file name does not contain a tool name, "No Tool Name" is returned.
        """
        match = re.match(self.regex, file_name)
        if match:
            tool_name = match.group(1)
            return tool_name
        else:
            print(f"{file_name} has no tool name {tool_name}")
            return "No Tool Name"
