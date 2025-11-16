# import json
# from langchain_core.prompts import PromptTemplate
# from langchain.chains.llm import LLMChain
# from langchain_community.chat_models import ChatOpenAI


# def generate_recommendations(mood, weather, region, food_data):
#     """
#     Calls LangChain LLM to get recommendations fresh each time.
#     """
#     llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)

#     prompt_template = PromptTemplate.from_template("""
#     You are a helpful food recommendation assistant.

#     Given:
#     - User mood: {mood}
#     - Weather: {weather}
#     - Region: {region}
#     - Food database snapshot: {food_data}

#     Recommend 5 dishes that best fit this context.

#     Return a JSON array like:
#     [
#       {{
#         "name": "Dish Name",
#         "reason": "Short reason for recommendation",
#         "tags": ["sweet", "comfort", "warm"]
#       }}
#     ]

#     Rules:
#     - Prefer foods suitable for the region.
#     - Match mood and weather to the food style.
#     - Vary cuisines for diversity.
#     """)

#     chain = prompt_template | llm

#     # Call the chain with our context
#     response = chain.invoke({
#         "mood": mood,
#         "weather": weather,
#         "region": region,
#         "food_data": json.dumps(food_data[:30])  # limit to 30 items for token cost
#     })

#     try:
#         data = json.loads(response)
#     except Exception:
#         # fallback JSON extraction
#         data = json.loads(response[response.find('['):response.rfind(']') + 1])

#     return data



import json
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

# Enable lightweight caching
set_llm_cache(SQLiteCache("llm_cache.db"))
print("LLM Caching Enabled.")

# Global model instance
llm = ChatGoogleGenerativeAI(api_key="Your API Key" ,model="gemini-2.5-flash-lite", temperature=0.5 , max_tokens=1000)
parser = JsonOutputParser()


# Prompt template
prompt = PromptTemplate.from_template("""
You are a food recommendation assistant.

Rules:
- Prefer foods suitable for the region.
- Match mood and weather.
- Vary cuisines for diversity.
- Output must be a JSON list of dish names only.
- Food Data is already displayed.you don't need to repeat it.
                                      
Constraints:
- Maximum 12 dishes.
- Items must not be from the provided Food Data.                                      

Inputs:
- Mood: {mood}
- Weather: {weather}
- Region: {region}
- Hunger Type: {hunger}
- Food Data: {food_data}
                                      
Task:
  Recommend 12 dishes that best fit this context.
                                      
Return a JSON array like:
    [
      {{
        "name": "Dish Name"
      }}
    ]

""")#

# Combined LCEL chain
chain = prompt | llm | parser

def generate_recommendations(mood, weather, region, hunger, food_data=None):#
    if food_data is None:
        food_data = []
    
    print("sdyusduoiddammmmmmmmm\n", food_data)
    food_json = json.dumps(food_data[: min(len(food_data), 36)])
    context = {"mood": mood, "weather": weather, "region": region, "hunger" : hunger, "food_data": food_json}#
    print("Context for LLM:", context)
    
    try:
        data = chain.invoke(context)
    except Exception as e:
        data = {"error": str(e)}
    
    return data
