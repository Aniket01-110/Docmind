from dotenv import load_dotenv #load_dotenv  is funciton inside the dotenv package
import os

load_dotenv()  #finds .env file, opens it, and reads every line, and loads each variable into system environment memory --So that python can access them
                                                                                             
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "") #access the Anthropic api key, os.getenv a function that reads one specific variable from the environment and it takes two arguments, os.getenv("variable_name", "default_name"), if api key not found return empty string, better than None
APP_NAME = os.getenv("APP_NAME", "Docmind") #reads APP_NAME from .env if not found then Docmind
DEBUG = os.getenv("DEBUG", "True")=="True"

print(f"App Name: {APP_NAME}")
print(f"Debug Mode: {DEBUG}")
print(f"API Key loaded:{bool(ANTHROPIC_API_KEY)}")

