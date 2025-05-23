from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from transformers import pipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


#llm = ChatOpenAI(model="gpt-3.5-turbo")
#llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
llm = pipeline('text-generation', model = 'gpt2')
#response = llm.invoke("What is machine?")

# response = generator("What is machine?")
# print(response)
# print(response[0]['generated_text'])

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assisant that will help generate a research paper.
            Answer the user query and use neccessary tools.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools = [] 
)

agent_executor = AgentExecutor(agent = agent, tools=[], verbose=True)

raw_response = agent_executor.invoke({"query": "What is the capital of france?"})

print(raw_response)
