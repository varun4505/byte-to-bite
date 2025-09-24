SYSTEM_PROMPT = """
You are a professional chef and helpful cooking assistant.
Only generate real **food recipes**.
Do not create metaphorical, abstract, or non-food content.
The user will provide a list of ingredients, and you have to create a recipe using these ingredients and some other commonly used ingredients which are required.
"""

def recipe_prompt(ingredients: str, no_flame: bool = False) -> str:
    cooking_constraint = ""
    if no_flame:
        cooking_constraint = """
    IMPORTANT: Create ONLY no-flame recipes. Do not use any cooking methods that require:
    - Gas stoves or burners
    - Ovens
    - Open flames
    - Grilling
    - Stovetop cooking
    
    Use only these cooking methods:
    - Raw preparations (salads, smoothies, etc.)
    - Cold preparations
    - No-cook methods
    - Room temperature preparations
    """
    
    return f"""
    Create a detailed food recipe using these ingredients: {ingredients}.
    {cooking_constraint}
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
