"""Conservative source parsing. Never infer missing amounts, timing, or yield."""
import re
from fractions import Fraction
WORDS={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12}
UNITS={'gram':'g','grams':'g','g':'g','kilogram':'kg','kilograms':'kg','kg':'kg','ounce':'oz','ounces':'oz','oz':'oz','pound':'lb','pounds':'lb','lb':'lb','lbs':'lb','milliliter':'ml','milliliters':'ml','millilitre':'ml','millilitres':'ml','ml':'ml','liter':'l','liters':'l','litre':'l','litres':'l','l':'l','cup':'cup','cups':'cup','tablespoon':'tbsp','tablespoons':'tbsp','tbsp':'tbsp','teaspoon':'tsp','teaspoons':'tsp','tsp':'tsp'}
def ingredient(text,n):
    original={'key':f'source-{n}','amount':None,'unit':'','name':text,'substitution':'','sourceText':text}
    # Ranges, compound quantities, package sizes and alternative amounts need review.
    match=re.match(r'^(\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?|'+ '|'.join(WORDS)+r')\s+([A-Za-z]+)\.?\s+(?:of\s+)?(.+)$',text,re.I)
    if not match:return original
    q,u,name=match.groups();unit=UNITS.get(u.lower())
    if not unit or re.match(r'^(?:and|or|to|plus|minus|a\s+half|half|\d)\b',name,re.I):return original
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
