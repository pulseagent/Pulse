from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


async def ai_search_agent(query: str):
    model = ChatOpenAI(model="gpt-4o", temperature=0.01)
    tools = [

    ]
    graph = create_react_agent(model, tools=tools)
    return graph.astream({"query": query})
