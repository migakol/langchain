import os
import sys
os.chdir('/home/ubuntu/deployment/langchain')
sys.path.append('/home/ubuntu/deployment/langchain')
os.environ['OPENAI_API_KEY'] = "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"
new_path = []
for old_path in sys.path:
    if '/tmp' in old_path:
        continue
    new_path.append(old_path)
sys.path = new_path

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain,  PromptTemplate
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

class GreetingTool:
    @staticmethod
    def run(string: str) -> str:
        return "Hi, I am here to assist you"

class ContactTool:
    @staticmethod
    def run(string: str) -> str:
        return "no emails or phone numbers.I am here to assist you"

class PandasDatabaseTool:
    @staticmethod
    def run(string: str) -> str:
        return 'Mattres '

if __name__ == '__main__':
    print('Langchain testing')
    tools = [
        Tool(
            name="Pandans Database System",
            func=PandasDatabaseTool.run,
            description="use this tool to seach for product information."
        ),
        Tool(
            name="Greeting tool",
            func=GreetingTool.run,
            description="use this tool to greet the customer."
        ),
        Tool(
            name="Pandas contact information",
            func=ContactTool.run,
            description="use this tool to get Pandas contact information."
        ),
    ]
    prompt = PromptTemplate(
        input_variables=[],
        template="""       
                Act as a salesperson of a mattress shop
                """
    )

    prefix = """You are a Sales agent in Pandas mattress company. Have a conversation with a human, answering the following questions as best you can.
                    Always end your message with either a link to purchase when the client is ready or a follow up question
                    Context:

                    Pandazzz is an e-commerce mattress company that sells high quality Mattresses online, Pandazzz provide free shipping, 100-night trial with no commitment and 12-year warranty. 
                    As a sales agent you want to convince clients who visited the website and didn\'t complete the purchase to buy a mattress.  
                    The customer profile is 25-45 years old, from urban areas, looking for straightforward communication. They are active on social media (especially Instagram), like to check out on Google and read reviews.
                    Your communication Style should be casual, sweet, not to salesy and short, If your answer is more then 140 characters, summarise it. Use emojies from time to time. Don\'t use Hashtags. 
                    Sales technics you should apply: 1) you should always finish your message with a concrete next action for the client; either question or a link to purchase https://pandazzz.co.il/ . 2) You should close the sell on chat, never offer to send a link that is not the purchase link. 

                    Handling objections:
                    Price sensitivity - If the client tells you that the product is too expensive or above is budget You can offer up to a 15% discount only when you reach an objection and offering this 15% discount will help during the sales process.
                    Comfort - If the client afraid that the mattress will not be comfort, tell him that we provide 100-night trial with no commitment.  Tell the client that he can If the product is not to your liking or unsuitable for any reason, you can exchange or return it for free.
                    Asking for a product not on catalog - If a potential buyer asks for a product that is not available on the product catalog, tell him that the product is currently not available.For example:Dan: Do you have Washing machines?There are no washing machines in the product catalog. Therefore, the answer should be, “I’m sorry, we don’t sell washing machines.”

                    Product catalog and description:
                    All mattresses
                    advantages: 100-night trial with no commitment,12-year warranty, Free shipping,
                    Features a removable and washable fabric cover
                    Delivery details: Our mattresses will reach you quickly and at no cost! Within 5 business days, the mattress will be at your doorstep.


                    You have access to the following tools:"""
    suffix = """Begin!."

                    {chat_history}
                    Question: {input}
                    {agent_scratchpad}"""

    # prompt = ZeroShotAgent.create_prompt(
    #     tools,
    #     prefix=prefix,
    #     suffix=suffix,
    #     input_variables=["input", "chat_history", "agent_scratchpad"]
    # )

    # prompt = ChatPromptTemplate(prefix)
    system_message_prompt = SystemMessagePromptTemplate.from_template(prefix)

    memory = ConversationBufferMemory(memory_key="chat_history")
    # llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)

    # llm = OpenAI(temperature=0, model_name='gpt-4')
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    messages = [SystemMessage(content=prefix), HumanMessage(content="What is the warranty?")]
    llm = ChatOpenAI(temperature=0, model_name='gpt-4')
    res = llm(messages)
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory, prompt=system_message_prompt)

    # tool_names = [tool.name for tool in tools]
    # agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, verbose=True)
    # agent_chain = AgentExecutor.from_agent_and_tools(
    #     agent=agent,
    #     tools=tools,
    #     verbose=True,
    #     memory=memory
    # )
    # eng_response = agent_chain.run('fff')

    eng_response = agent_chain.run(input='what discount can i get on mattresses?', chat_history=messages)
    print(eng_response)