
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser




# Global model instance
llm = ChatGoogleGenerativeAI(api_key="AIzaSyDbpWap96tJpC9CGBaqfo3XZf2Fm1IYzPk" ,model="gemini-2.5-flash-lite", temperature=0.5 , max_tokens=1000)
parser = JsonOutputParser()


# Prompt template
prompt = PromptTemplate.from_template(
"""
You are a chef.
Given a food name, provide a recipe including ingredients and step-by-step instructions.
Food Name: {food_name}

Output the recipe in JSON format with the following structure:
{{
  "title": "Dish Name",
  "ingredients": [
    "Ingredient 1",
    "Ingredient 2",
    ...
  ],
  "instructions": [
    "Step 1",
    "Step 2",
    ...
  ]
}}

                                      
""")#- Food Data: {food_data}

# Combined LCEL chain
chain = prompt | llm | parser

def recipefromai(food_name):#, food_data
    # food_json = json.dumps(food_data[: min(len(food_data), 30)])
    # context = {"mood": mood, "weather": weather, "region": region, "hunger" : hunger}#, "food_data": food_json
    context = {"food_name": food_name}
    print("Generating Recipe for:", food_name)
    try:
        data = chain.invoke(context)
        print("Generated Recipe:", data)
    except Exception as e:
        print("Error generating recipe:", str(e))
        data = {"error": str(e)}
    
    return data

