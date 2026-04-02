from tools import ToolName

tool_definitions = [
    {
        "name": ToolName.SEARCH_WEB.value,
        "description": "Search the web for real-time information. Use this for current events, sports fixtures, news, weather, or anything that requires up to date information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "desrcription": "The search query to look up"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": ToolName.CONVERT_TIMEZONE.value,
        "description": "Convert a time from one timezone to another. Use this whenever the user asks for time conversion or wants a time in a specific timezone.",
        "input_schema": {
            "type": "object",
            "properties": {
                "time_str": {
                    "type": "string",
                    "description": "Time in HH:MM 24-hour format e.g. 19:00"
                },
                "from_tz": {
                    "type": "string",
                    "description": "Source timezone e.g. Europe/London"
                },
                "to_tz": {
                    "type": "string",
                    "description": "Target timezone e.g. America/Chicago"
                }
            },
            "required": ["time_str", "from_tz", "to_tz"]
        }
    },
    {
        "name": ToolName.CALCULATE.value,
        "description": "Perform mathematical calculations. Use this for any arithmetic, percentages, conversions or numerical computations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate e.g. '2 + 2' or '15 * 0.2'"
                }
            },
            "required": ["expression"]
        }
    }
]