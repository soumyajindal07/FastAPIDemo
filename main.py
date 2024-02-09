from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ItemPayload
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from langchain import OpenAI
from sqlalchemy import create_engine
from pydantic import BaseModel
from sqlalchemy import text
import os
#import streamlit

app = FastAPI()
origins = ["*"]

api_key = os.getenv('OPENAI_API_KEY')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    
)

#grocery_list: dict[int, ItemPayload] = {}

@app.get("/test")
def root():
    if 'OPENAI_API_KEY' in os.environ:
        return("Environment variable is set.")
        value = os.environ['OPENAI_API_KEY']
        return("Value:", value)
    else:
        print("Environment variable is not set.")
    #DB_NAME = "Test"
    #cnx = create_engine('mysql+pymysql://root:focus123@localhost:3306/focus') 
    #list =[]
   # with cnx.connect() as conn:
       # q="SELECT castforename FROM msacast LIMIT 0,10"
       # my_cursor=conn.execute(text(q))
        #my_data=my_cursor.fetchall()
        #for row in my_data:
           # list.append(row[0])
            #print (row)            
        #return list
# Route to add a item

@app.get("/items/{item_id}")
def list_item(item_id: int) -> dict[str, int]:    
   

    #st.set_page_config(page_title="AI APP TO CHAT WITH SQL DB")
    #st.header="ASK ANYTHING ABOUT YOUR DB"
    #query=st.text_input("ask question here")

    cs="mysql+pymysql://root:focus123@localhost:3306/focus"
    db_engine=create_engine(cs)
    db=SQLDatabase(db_engine)

    llm=OpenAI(temperature=0.0,verbose = True, openai_api_key=os.environ['OPENAI_API_KEY'])

    agent=create_sql_agent(llm=llm,toolkit=SQLDatabaseToolkit(db=db, llm=llm),agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)
    testData = agent.run('How many programmes are there?')
    #raise HTTPException(status_code=404, detail= testData)
    
    return {"item": testData}

# Route to add an item
@app.get("/data")
def add_item(item_name: str):
    cs="mysql+pymysql://root:focus123@localhost:3306/focus"
    db_engine=create_engine(cs)
    db=SQLDatabase(db_engine)

    llm=OpenAI(temperature=0.0,verbose = True, openai_api_key=api_key)

    agent=create_sql_agent(llm=llm,toolkit=SQLDatabaseToolkit(db=db, llm=llm),agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)
    testData = agent.run(item_name)
    #raise HTTPException(status_code=404, detail= testData)
    
    return testData


@app.post("/convert")
def convert(input:ItemPayload):
    cs="mysql+pymysql://root:focus123@localhost:3306/focus"
    db_engine=create_engine(cs)
    db=SQLDatabase(db_engine)

    llm=OpenAI(temperature=0.0,verbose = True, openai_api_key=api_key)

    agent=create_sql_agent(llm=llm,toolkit=SQLDatabaseToolkit(db=db, llm=llm),agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)
    testData = agent.run(input.item_name)
    #raise HTTPException(status_code=404, detail= testData)
    
    return testData
