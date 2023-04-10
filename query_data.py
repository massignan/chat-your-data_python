from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain


_template = """Given the following conversation and a follow up question, reprhase the follow up question to be a standalone question. You can assume the question about world economy.

Chat History: {chat_history}
Follow Up Input: {question}
Standalone question: """

CONDENSATE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are an AI assitant for answering question about world economy.
You are given the following extracted parts of a long document and a question. Provide conversational answer.
If you don't know the answer, just say "Hmm, I am not sure." Don't try make up an answer.
If the question is not about the world economy, politely inform them that you are tuned to only answer questions about world economy.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""

#QA = Question Answer
QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])

def get_chain(vectorstore):
    llm = OpenAI(temperature=0,model_name="gpt-3.5-turbo")
    qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSATE_QUESTION_PROMPT
    )
    return qa_chain


