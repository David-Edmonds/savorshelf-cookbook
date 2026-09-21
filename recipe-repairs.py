"""Conservative source parsing. Never infer missing amounts, timing, or yield."""
import re
from fractions import Fraction
WORDS={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12}
UNITS={'gram':'g','grams':'g','g':'g','kilogram':'kg','kilograms':'kg','kg':'kg','ounce':'oz','ounces':'oz','oz':'oz','pound':'lb','pounds':'lb','lb':'lb','lbs':'lb','milliliter':'ml','milliliters':'ml','millilitre':'ml','millilitres':'ml','ml':'ml','liter':'l','liters':'l','litre':'l','litres':'l','l':'l','cup':'cup','cups':'cup','tablespoon':'tbsp','tablespoons':'tbsp','tbsp':'tbsp','teaspoon':'tsp','teaspoons':'tsp','tsp':'tsp'}
# Preserve regional/obsolete units as named units, without assigning modern volumes.
UNITS.update({'teaspoonful':'tsp','teaspoonfuls':'tsp','tablespoonful':'tbsp','tablespoonfuls':'tbsp','cupful':'cup','cupfuls':'cup','pint':'pint','pints':'pint','quart':'quart','quarts':'quart','gallon':'gallon','gallons':'gallon','gill':'gill','gills':'gill'})
FRACTIONS={'¼':'1/4','½':'1/2','¾':'3/4','⅓':'1/3','⅔':'2/3','⅛':'1/8','⅜':'3/8','⅝':'5/8','⅞':'7/8'}
NUMBER=r'(?:\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?|'+ '|'.join(WORDS)+r')'
# Count only explicit, familiar whole ingredients. Unknown nouns remain source text.
COUNT=r'(?:eggs?|egg yolks?|egg whites?|onions?|potatoes?|tomatoes?|lemons?|limes?|oranges?|apples?|pears?|peaches?|carrots?|bay leaves|bay leaf|garlic cloves?)'
def normalized_quantity_text(text):
    value=text.strip().replace('\u00a0',' ')
    for glyph,fraction in FRACTIONS.items():
        value=re.sub(r'(\d)'+glyph,r'\1 '+fraction,value)
        value=value.replace(glyph,fraction)
    value=re.sub(r'^(?:three[- ]quarters(?: of)?(?: a)?|three fourths(?: of)?(?: a)?)\s+', '3/4 ',value,flags=re.I)
    value=re.sub(r'^(?:a quarter(?: of)?(?: a)?|one quarter(?: of)?(?: a)?|one[- ]fourth(?: of)?(?: a)?)\s+', '1/4 ',value,flags=re.I)
    value=re.sub(r'^(?:half(?: of)?(?: a)?|one[- ]half(?: of)?(?: a)?)\s+', '1/2 ',value,flags=re.I)
    value=re.sub(r'^(a|an)\s+(?=(?:'+ '|'.join(UNITS)+r')\b)', '1 ',value,flags=re.I)
    return value

def ingredient(text,n):
    original={'key':f'source-{n}','amount':None,'unit':'','name':text,'substitution':'','sourceText':text}
    value=normalized_quantity_text(text)
    match=re.match(r'^('+NUMBER+r')\s*([A-Za-z]+)\.?\s+(?:of\s+)?(.+)$',value,re.I)
    unit=None
    if match:
        q,u,name=match.groups();unit=UNITS.get(u.lower())
    if not unit:
        match=re.match(r'^('+NUMBER+r')\s+((?:(?:small|medium|large|whole|fresh)\s+)?'+COUNT+r'(?:\s*,.*)?)$',value,re.I)
        if not match:return original
        q,name=match.groups();unit=''
    if re.match(r'^(?:and|or|to|plus|minus|a\s+half|half|\d)\b',name,re.I):return original
    if re.search(r'\b(?:fluid|heaped|heaping|rounded|scant|troy|apothecar|avoirdupois)\b',text,re.I):return original
    if unit=='oz' and re.search(r'\b(?:milk|water|juice|wine|brandy|rum|vinegar|oil|cream|extract|syrup|stock|broth|beer|liqueur)\b',name,re.I):return original
    try:amount=WORDS[q.lower()] if q.lower() in WORDS else float(sum(Fraction(x) for x in q.split()))
    except (ValueError,ZeroDivisionError):return original
    if not 0<amount<=1000000:return original
    return {**original,'amount':amount,'unit':unit,'name':name}

def repair(row):
    ingredients=[ingredient(s,n) for n,s in enumerate(row['originalIngredients'])]
    steps=list(row['originalSteps']);linked=[]
    for i in ingredients:
        if i['amount'] is None:continue
        # Replace a full source ingredient phrase only if it occurs once in the method.
        # Partial/divided additions and bare ingredient names are never expanded by guessing.
        pattern=re.compile(r'(?<!\w)'+re.escape(i['sourceText'])+r'(?!\w)',re.I)
        if sum(len(pattern.findall(s)) for s in steps)==1:
            steps=[pattern.sub('{{'+i['key']+'}}',s) for s in steps];linked.append(i['key'])
    return ingredients,steps,linked
