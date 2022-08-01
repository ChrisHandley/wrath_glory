from app import app
from app.forms import SlimSheet
from flask import render_template, request, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField


attributes = {
                'strength': 0,
                'toughness': 0,
                'agility': 0,
                'initiative': 0,
                'willpower': 0,
                'intelligence': 0,
                'fellowship': 0,
                'athletics': 0,
                'awareness': 0,
                'ballistic': 0,
                'cunning': 0,
                'deception': 0,
                'insight': 0,
                'intimidation': 0,
                'investigation': 0,
                'leadership': 0,
                'medicae': 0,
                'persuasion': 0,
                'pilot': 0,
                'psychic': 0,
                'scholar': 0,
                'stealth': 0,
                'survival': 0,
                'tech': 0,
                'weapon': 0,
                'armour': 0
}

attribute_label = ['strength',
                'toughness',
                'agility',
                'initiative',
                'willpower',
                'intelligence',
                'fellowship',
                'armour',
                'defence',
                'wounds',
                'shock',
                'resilience',
                'conviction',
                'determination',
                'resolve']

core_attribute_label = ['strength',
                'toughness',
                'agility',
                'initiative',
                'willpower',
                'intelligence',
                'fellowship']


attribute_cost = [0, 0, 4, 10, 20, 35, 55, 80 , 110, 145, 185, 230, 280]

skill_cost = [0, 2, 6, 12, 20, 30, 42, 56, 72]

skill_label = ['athletics',
                'awareness',
                'ballistic',
                'cunning',
                'deception',
                'insight',
                'intimidation',
                'investigation',
                'leadership',
                'medicae',
                'persuasion',
                'pilot',
                'psychic',
                'scholar',
                'stealth',
                'survival',
                'tech',
                'weapon'
]

skills_total = {'athletics': 0,
                'awareness': 0,
                'ballistic': 0,
                'cunning': 0,
                'deception': 0,
                'insight': 0,
                'intimidation': 0,
                'investigation': 0,
                'leadership': 0,
                'medicae': 0,
                'persuasion': 0,
                'pilot': 0,
                'psychic': 0,
                'scholar': 0,
                'stealth': 0,
                'survival': 0,
                'tech': 0,
                'weapon': 0
            }

derived = {
    'defence': 0,
    'wounds': 0,
    'shock': 0,
    'resilience': 0,
    'conviction': 0,
    'determination': 0,
    'resolve': 0,
    'speed': 0,
    'size': '-'
}

tier = 0

XP_Cost = 0





# default route, gets rendered when user goes to http://127.0.0.1:5000/ in a browser
@app.route("/")
def index():
    if 'attributes' in session:
        print('recall')
    else:
        session['attributes'] = attributes
        session['derived'] = derived
        session['tier'] = tier
        session['XP_Cost'] = XP_Cost
        session['skills_total'] = skills_total
        session['simulation'] = {}

    return render_template("index.html", attributes=session['attributes'], derived=session['derived'], tier=session['tier'], XP_Cost=session['XP_Cost'], skills_total=session['skills_total'], skill_label=skill_label,
                            attribute_label=attribute_label)

@app.route("/simulate", methods=["POST"])
def simulate():
    global attributes
    global derived
    weapons = {
        'lasgun': {
            'damage': 7,
            'extra damage': 1,
            'AP': 0
        },
        'boltgun': {
            'damage': 10,
            'extra damage': 1,
            'AP': 0
        },
        'plasma gun': {
            'damage': 15,
            'extra damage': 1,
            'AP': 3
        },
        'meltagun': {
            'damage': 16,
            'extra damage': 2,
            'AP': 4
        }
    }
    result = {}

    base_res = session['derived']['resilience'] - session['attributes']['armour']
    base_armour = session['attributes']['armour']

    for weapon in weapons:
        # print(weapon)
        # print(weapons[weapon]['AP'])
        # print(base_armour - weapons[weapon]['AP'])
        armour_remaining = max([(base_armour - weapons[weapon]['AP']), 0])
        resilience_remaining = armour_remaining + base_res
        wounds_dealt = max([(weapons[weapon]['damage']-resilience_remaining), 0])
        wounds_remaining = max([session['derived']['wounds']-wounds_dealt ,0])
        #print(base_armour, armour_remaining, base_res, resilience_remaining, wounds_dealt)
        result[weapon] = {'armour remaining': armour_remaining, 'resilience remaining': resilience_remaining,
                            'wounds dealt': wounds_dealt, 'wounds remaining': wounds_remaining}
        #print(result[weapon])
        session['simulation'] = result
    
    return jsonify(simulation=session['simulation'])

@app.route("/reset", methods=["POST"])
def reset():
    global attribute_label
    for att in session['attributes']:
        session['attributes'][att] = 0
    session['XP_Cost'] = 0
    session['tier'] = 0
    for dev in session['derived']:
        session['derived'][dev] = 0
    for skill in session['skills_total']:
        session['skills_total'][skill] = 0
    
    return jsonify(attributes = session['attributes'], derived = session['derived'], tier = session['tier'], XP_Cost = session['XP_Cost'], skills_total = session['skills_total'], attribute_label = attribute_label)

# POST request to this endpoint(route) results in the number of votes after upvoting
@app.route("/button/<updown>/<name>", methods=["POST"])
def updownbutton(name,updown):
    downup = updown.split('-')[1]
    if downup == 'up':
        session['attributes'][name] += 1
    elif downup == 'down':
        if session['attributes'][name] >= 1:
            session['attributes'][name] -= 1
    session['XP_Cost'] = derive_attributes()
    
    return jsonify(attributes = session['attributes'], derived = session['derived'], tier = session['tier'], XP_Cost = session['XP_Cost'], skills_total = session['skills_total'])

def derive_attributes():
    
    XP_Cost = derive_cost()
    
    if session['XP_Cost'] < 200:
        session['tier'] = 1
    elif session['XP_Cost'] < 300:
        session['tier']  = 2
    elif session['XP_Cost'] < 400:
        session['tier']  = 3
    elif session['XP_Cost'] < 500:
        session['tier']  = 4
    else:
        session['tier']  = 5
    
    session['derived']['defence'] =  session['attributes']['initiative'] - 1
    if session['derived']['defence'] < 0: session['derived']['defence'] = 0
    session['derived']['resilience'] =  session['attributes']['toughness'] + 1 +  session['attributes']['armour']
    session['derived']['wounds'] =  session['attributes']['toughness'] + session['tier']*2
    session['derived']['shock'] =  session['attributes']['willpower'] + session['tier']
    session['derived']['determination'] =  session['attributes']['toughness']
    session['derived']['conviction'] =  session['attributes']['willpower']
    session['derived']['resolve'] =  session['attributes']['willpower'] - 1
    if session['derived']['resolve'] < 0: session['derived']['resolve'] = 0

    for att in attribute_label:
        if att == 'strength':
            session['skills_total']['athletics'] =  session['attributes']['athletics'] +  session['attributes']['strength']
        if att == 'agility':
            session['skills_total']['ballistic'] =  session['attributes']['ballistic'] +  session['attributes']['agility']
            session['skills_total']['pilot'] =  session['attributes']['pilot'] +  session['attributes']['agility']
            session['skills_total']['stealth'] =  session['attributes']['stealth'] +  session['attributes']['agility']
        if att == 'initiative':
            session['skills_total']['weapon'] =  session['attributes']['weapon'] +  session['attributes']['initiative']
        if att == 'willpower':
            session['skills_total']['intimidation'] =  session['attributes']['intimidation'] +  session['attributes']['willpower']
            session['skills_total']['leadership'] =  session['attributes']['leadership'] +  session['attributes']['willpower']
            session['skills_total']['psychic'] =  session['attributes']['psychic'] +  session['attributes']['willpower']
            session['skills_total']['survival'] =  session['attributes']['survival'] +  session['attributes']['willpower']
        if att == 'intelligence':
            session['skills_total']['awareness'] =  session['attributes']['awareness'] +  session['attributes']['intelligence']
            session['skills_total']['tech'] =  session['attributes']['tech'] +  session['attributes']['intelligence']
            session['skills_total']['scholar'] =  session['attributes']['scholar'] +  session['attributes']['intelligence']
            session['skills_total']['investigation'] =  session['attributes']['investigation'] +  session['attributes']['intelligence']
            session['skills_total']['medicae'] =  session['attributes']['medicae'] +  session['attributes']['intelligence']
        if att == 'fellowship':
            session['skills_total']['cunning'] =  session['attributes']['cunning'] +  session['attributes']['fellowship']
            session['skills_total']['deception'] =  session['attributes']['deception'] +  session['attributes']['fellowship']
            session['skills_total']['insight'] =  session['attributes']['insight'] +  session['attributes']['fellowship']
            session['skills_total']['persuasion'] =  session['attributes']['persuasion'] +  session['attributes']['fellowship']


    return XP_Cost

def derive_cost():
    global core_attribute_label
    global skill_label
    global attribute_cost
    '''
    Let's compute the cost of the attributes
    '''
    XP_Cost = 0
    for att in core_attribute_label:
        att_value = session['attributes'][att]
        XP_Cost = XP_Cost + attribute_cost[att_value]

    for skill in skill_label:
        skill_value = session['attributes'][skill]
        XP_Cost = XP_Cost + skill_cost[skill_value]
    
    return XP_Cost



