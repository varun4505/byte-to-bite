SYSTEM_PROMPT = """
You are a professional chef and helpful cooking assistant.
Only generate real **food recipes**.
Do not create metaphorical, abstract, or non-food content.
The user will provide a list of ingredients, and you have to create a recipe using these ingredients and some other commonly used ingredients which are required.
"""

def recipe_prompt(ingredients: str) -> str:
    return f"""
    Create a detailed food recipe using these ingredients: {ingredients}.
    Include:
    - Recipe name
    - A brief description of the dish
    - Ingredients list with quantities
    - Step-by-step cooking instructions
    - Cooking time
    - Serving size
    Format the recipe clearly and concisely.
    If the ingredients do not seem like food items, respond with:
    "⚠️ These ingredients do not seem like typical food items. Please enter real culinary ingredients."
    """
