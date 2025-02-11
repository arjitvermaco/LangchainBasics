from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.tools import StructuredTool
from pydantic import BaseModel
from langchain_core.tools import Tool
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from dotenv import load_dotenv
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor,create_openai_functions_agent,create_tool_calling_agent

load_dotenv()


def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime  # Import datetime module to get current time

    now = datetime.datetime.now()  # Get current time
    return now.strftime("%I:%M %p") 


def write_report(filename: str, html: str):
    """Write an HTML report to disk."""
    with open(filename, "w") as f:
        f.write(html)
        
class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str
        
write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool whenever someone asks for a report.",
    func=write_report,
    args_schema=WriteReportArgsSchema
)


tools = [
    Tool(
        name="Time",
        func=get_current_time,
        description="Useful when you need to know the current time"
    ),
    write_report_tool
]
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's question with your tools"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# Initialize the Language Model using Groq
# temperature=0.7 provides a good balance between creativity and accuracy
# llm = ChatGroq(
#     model="llama3-8b-8192",
#     temperature=0.7,
# )

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

agent_executor.invoke({"input": "What is the current time and write a report to disk?"})