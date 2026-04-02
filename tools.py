import os
import pytz
from models import Success, Error
from enum import Enum
from tavily import TavilyClient
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

class ToolName(Enum):
    SEARCH_WEB = "search_web"
    CONVERT_TIMEZONE = "convert_timezone"
    CALCULATE = "calculate"

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY").strip())

def search_web(query):
    try:
        results = tavily.search(query=query, max_results=3)
        output = []

        for result in results["results"]:
            output.append({
                "title": result["title"],
                "content": result["content"],
                "url": result["url"]
            })
        
        return Success(data=output, tool_name = ToolName.SEARCH_WEB.value)
    except Exception as e:
        return Error(message=str(e), tool_name=ToolName.SEARCH_WEB.value)

def convert_timezone(time_str, from_tz, to_tz):
    """Convert time between timezones.
    time_str format: 'HH:MM' (24hr)
    tz format: 'Europe/London', 'America/Chicago' etc
    """
    try:
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
        
        today = datetime.now().strftime("%Y-%m-%d")
        dt = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M")
        
        dt_from = from_zone.localize(dt)
        dt_to = dt_from.astimezone(to_zone)
        
        return Success(
            data = {
            "original": f"{time_str} {from_tz}",
            "converted": dt_to.strftime("%I:%M %p"),
            "timezone": to_tz
            },
            tool_name=ToolName.CONVERT_TIMEZONE.value
        )
    except Exception as e:
        return Error(message=str(e), tool_name=ToolName.CONVERT_TIMEZONE.value)

def calculate(expression):
    try:
        result = eval(expression)
        return Success(
            data = {"expression": expression, "result": result},
            tool_name=ToolName.CALCULATE.value
        )
    except Exception as e:
        return Error(message=str(e), tool_name=ToolName.CALCULATE.value)