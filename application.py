import dash
import dash_bootstrap_components as dbc
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
import base64
from dash.dependencies import Output, Input
from factionKeywords import keywords_factions
from test_list import test_list

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

application = app.server
app.config.suppress_callback_exceptions = True

app.title='Wrath & Glory Character Builder'

Attributes = (
    "strength", "toughness", "agility",
    "initiative", "willpower", "intelligence",
    "fellowship",
)

Skills = ('athletics',
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
)

attribute_cost = [0, 0, 4, 10, 20, 35, 55, 80 , 110, 145, 185, 230, 280]

skill_cost = [0, 2, 6, 12, 20, 30, 42, 56, 72]

XP_Cost = 0

species_list = [
    {'label':'Human', 'value':'Human'},
    {'label':'Ork', 'value':'Ork'},
    {'label':'Aeldari', 'value':'Aeldari'},
    {'label':'Adeptus Astartes', 'value':'Adeptus Astartes'},
    {'label':'Primaris Astartes', 'value':'Primaris Astartes'},
]

species = [dbc.DropdownMenuItem(i) for i in species_list]

maximums_attr = {
    "Human": {
        "strength": 8,
        "toughness": 8,
        "agility": 8,
        "initiative": 8,
        "willpower": 8,
        "intellect": 8,
        "fellowship": 8,
        "speed": 8
    },
    "Ork": {
        "strength": 12,
        "toughness": 12,
        "agility": 7,
        "initiative": 7,
        "willpower": 8,
        "intellect": 7,
        "fellowship": 7,
        "speed": 7
    },
    "Aeldari": {
        "strength": 7,
        "toughness": 7,
        "agility": 12,
        "initiative": 12,
        "willpower": 12,
        "intellect": 10,
        "fellowship": 6,
        "speed": 10
    },
    "Adeptus Astartes": {
        "strength": 10,
        "toughness": 10,
        "agility": 9,
        "initiative": 9,
        "willpower": 10,
        "intellect": 10,
        "fellowship": 8,
        "speed": 9
    },
    "Primaris Astartes": {
        "strength": 12,
        "toughness": 12,
        "agility": 9,
        "initiative": 9,
        "willpower": 10,
        "intellect": 10,
        "fellowship": 8,
        "speed": 9
    },

}

keywords_species={
    "Human": None,
    "Adeptus Astartes": "[Chapter]",
    "Primaris Astartes": "[Chapter], Imperium, Primaris",
    "Aeldari": None,
    "Ork": "[Clan]",
}

faction_list=keywords_factions


keyword_list_master = [
    {'label': 'UP', 'value': 'UP'},
    {'label': 'DOWN', 'value': 'DOWN'}
    ]




app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.Img(src=app.get_asset_url('WrathGloryBanner.png')), style={"textAlign": "center"}, width=12)),
    dbc.Row(dbc.Col(html.H1("Wrath and Glory Character Builder",
                            style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(html.H3("Attributes",
                            style={"textAlign": "center"}), width=3),
            dbc.Col([
                # html.Div(id='placeholder'),
                html.Div(
                            id="attribute_check"),], width=3
            ),
            dbc.Col([
                dbc.Row([
                        dbc.Col(
                        # html.Div(id='placeholder'),
                            html.H5("Tier",
                            style={"textAlign": "left"}), width=3),
                        dbc.Col(
                        # html.Div(id='placeholder'),
                            html.H5("1:",
                            style={"textAlign": "center"}), width=2),
                        dbc.Col(
                        # html.Div(id='placeholder'),
                            html.H5("2:",
                            style={"textAlign": "center"}), width=2),
                        dbc.Col(
                        # html.Div(id='placeholder'),
                            html.H5("3:",
                            style={"textAlign": "center"}), width=2),
                        dbc.Col(
                        # html.Div(id='placeholder'),
                            html.H5("4:",
                            style={"textAlign": "center"}), width=2),
                ]),
                dbc.Row([
                    dbc.Col(html.H5("NPC Threat Level", style={"textAlign": "left"}), width=3),
                    dbc.Col(html.H5(id="threat_level1", style={"textAlign": "center"}), width=2),
                    dbc.Col(html.H5(id="threat_level2", style={"textAlign": "center"}), width=2),
                    dbc.Col(html.H5(id="threat_level3", style={"textAlign": "center"}), width=2),
                    dbc.Col(html.H5(id="threat_level4", style={"textAlign": "center"}), width=2),

                ])    
            ])
        ]
    ),   
    html.Hr(),
    dbc.Row(
        [
            dbc.Col([
                        html.H5("S", style={"textAlign": "center"}),
                        dcc.Input(
                            id="strength".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=1, max=12, value=1),
                        html.H5("A", style={"textAlign": "center"}),
                        dcc.Input(
                            id="agility".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=1, max=12, value=1),
                        html.H5("WIL", style={"textAlign": "center"}),
                        dcc.Input(
                            id="willpower".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=1, max=12, value=1),
                        html.H5("FEL", style={"textAlign": "center"}),
                        dcc.Input(
                            id="fellowship".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=1, max=12, value=1),   
                    ], width=2),
            dbc.Col([
                        html.H5("T", style={"textAlign": "center"}),
                        dcc.Input(
                            id="toughness".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=1, max=12, value=1),
                        html.H5("I", style={"textAlign": "center"}),
                        dcc.Input(
                            id="initiative".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=1, max=12, value=1),
                        html.H5("INT", style={"textAlign": "center"}),
                        dcc.Input(
                            id="intelligence".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=1, max=12, value=1),
                        html.H5("ARM", style={"textAlign": "center"}),
                        dcc.Input(
                            id="armour".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=0, max=12, value=0),
                    ], width=2),
            dbc.Col([
                # dbc.Row([dbc.DropdownMenu(label="species dropdown", size="lg", children=species, className="mb-3")]),
                dbc.Row(
                    [
                        dbc.Col(html.H5("Species"), width=2),
                        dbc.Col(
                            dcc.Dropdown(options=species_list, id="species_selected",
                                multi=False, clearable=False, value="Human"
                                ),
                                width=3, style={"textAlign": "left"}
                            ),
                        dbc.Col(html.H5("Faction")),
                        dbc.Col(
                            dcc.Dropdown(id="faction_selected",
                                multi=False, clearable=False, value="Imperium"
                                ),
                                width=3, style={"textAlign": "left"}
                            ),
                        # dbc.Col(html.Div(id="maximums"), width=2),
                    ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.H5("Keywords"), width=2),
                ]),
                dbc.Row([
                    dbc.Col(html.H5(id="species_keywords"), width=2),
                    dbc.Col(dcc.Dropdown(options=keyword_list_master, id="keyword_list", multi=True,
                            clearable=True, placeholder="Select Keywords"))
                ]),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(html.H5("Total XP", style={"textAlign": "left"})),
                        dbc.Col(html.H5("Tier", style={"textAlign": "left"})),
                    ]
                ),
                dbc.Row(
                    [
                        # dbc.Col(html.Div(id="totalCost", style={"textAlign": "left"})),
                        dbc.Col(html.Div(id="totalCost", style={"textAlign": "left"})),
                        dbc.Col(html.Div(id="tier_result", style={"textAlign": "left"})),
                        # dbc.Col(dcc.Input(
                        #     id="tier".format("number"),
                        #     type="number",
                        #     placeholder="input type {}".format("number"), min=1, max=5, value=1)),

                    ]
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5("Conviction", style={"textAlign": "left"}),
                        ),
                        dbc.Col(
                            html.H5("Size", style={"textAlign": "left"}),
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(id="totalConviction"),),
                        dbc.Col(dcc.Input(
                            id="size".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=0, max=8, value=0)),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5("Resolve", style={"textAlign": "left"}),
                        ),
                        dbc.Col(
                            html.H5("Speed", style={"textAlign": "left"}),
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(id="totalResolve"),),
                        dbc.Col(dcc.Input(
                            id="speed".format("number"),
                            type="number",
                            placeholder="input type {}".format("number"), min=0, max=12, value=0)),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5("Defence", style={"textAlign": "left"}),
                        ),
                        dbc.Col(
                            html.H5("Resilience", style={"textAlign": "left"}),
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(id="totalDefence"),),
                        dbc.Col(html.Div(id="totalResilience"),),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5("Wounds", style={"textAlign": "left"}),
                        ),
                        dbc.Col(
                            html.H5("Shock", style={"textAlign": "left"}),
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(id="totalWounds"),),
                        dbc.Col(html.Div(id="totalShock"),),
                    ]
                ),
            ])
        ],
    ),
    html.Hr(),
    dbc.Row(dbc.Col(html.H3("Skills",
                            style={"textAlign": "center"}), width=4)),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(html.H5("Athletics (S)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Medicae (INT)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="athletics".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalAthletics"),),
            dbc.Col(dcc.Input(
                    id="medicae".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
             dbc.Col(html.Div(id="totalMedicae"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Awareness (INT)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Persuasion (FEL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ],
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="awareness".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalAwareness"),),
            dbc.Col(dcc.Input(
                    id="persuasion".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalPersuasion"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Ballistic Skill (A)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Pilot (A)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ],
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="ballistic".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalBallistic"),),
            dbc.Col(dcc.Input(
                    id="pilot".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalPilot"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Cunning (FEL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Psychic (WIL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ],
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="cunning".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalCunning"),),
            dbc.Col(dcc.Input(
                    id="psychic".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalPsychic"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Deception (FEL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Scholar (INT)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ],
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="deception".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalDeception"),),
            dbc.Col(dcc.Input(
                    id="scholar".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalScholar"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Insight (FEL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Stealth (A)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ],
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="insight".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalInsight"),),
            dbc.Col(dcc.Input(
                    id="stealth".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalStealth"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Intimidation (WIL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Survival (WIL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ],
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="intimidation".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalIntimidation"),),
            dbc.Col(dcc.Input(
                    id="survival".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalSurvival"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Investigation (INT)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Tech (INT)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ],
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="investigation".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalInvestigation"),),
            dbc.Col(dcc.Input(
                    id="tech".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalTech"),),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(html.H5("Leadership (WIL)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
            dbc.Col(html.H5("Weapon Skill (I)", style={"textAlign": "left"})),
            dbc.Col(html.H5("Total", style={"textAlign": "center"})),
        ]
    ),
        dbc.Row(
        [
            dbc.Col(dcc.Input(
                    id="leadership".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalLeadership"),),
            dbc.Col(dcc.Input(
                    id="weapon".format("number"),
                    type="number",
                    placeholder="input type {}".format("number"), min=0, max=8, value=0)),
            dbc.Col(html.Div(id="totalWeapon"),),
        ]
    ),

])


@app.callback(
    Output("faction_selected", "options"),
    Input("species_selected", "value")
)
def faction_select(species_selected):
    print("species ", species_selected)
    # print(faction_list)
    faction_selected = faction_list[species_selected]
    if faction_selected == None:
        faction_selected = {'label': 'Ork', 'value': 'Ork'}
    print(faction_selected)
    # faction_selected = [{'label': 'Anhrathe', 'value': 'Anhrathe'},
    #                     {'label': 'Asuryani', 'value': 'Asuryani'}]
    return(faction_selected)


@app.callback(
    Output("attribute_check", "children"),
    Output('species_keywords', 'children'),
    inputs=dict(attr=[Input("{}".format(_), "value") for _ in Attributes],
    # species_selected=Input("placeholder", "value"),
    speed=[Input('speed', 'value')],
    species_selected=[Input('species_selected', 'value')]
    )
)
def attribute_checks(attr, speed, species_selected):
    # print(attr)
    # print(species_selected)
    # print(maximums_attr[species_selected[0]])
    # print(speed)
    attributes_max = list(maximums_attr[species_selected[0]].values())
    attribute_check = "Attributes Conform to Species Maximum"
    for i, value in enumerate(attr):
        # print("attribute: ", value) 
        # print(attributes_max[i])
        if (value > attributes_max[i]):
        #     print("Attribute Exceeded")
            attribute_check=html.H5(children="Attributes Not Legal", style={"color": "red"})
            # attribute_check="Attributes Not Legal"
        # else:
        #     attribute_check="Attributes Meet Species Limits"
    max_speed = attributes_max[-1]
    if speed[0] > max_speed:
        attribute_check=html.H5(children="Attributes Not Legal", style={"color": "red"})
    
    species_keywords = keywords_species[species_selected[0]]
    return(attribute_check, species_keywords)
    

@app.callback(
    Output("totalAthletics", "children"),
    Input("strength", "value"),
    Input("athletics", "value"),
)
def computeStrength(strength, athletics):
    if strength == None:
        value = 1
    else:
        value = strength
    if athletics == None:
        athletics = 0
    totalAthletics = value + athletics
    return totalAthletics

@app.callback(
    Output("totalWeapon", "children"),
    Input("initiative", "value"),
    Input("weapon", "value"),
)
def computeInitiative(initiative, weapon):
    if initiative == None:
        value = 1
    else:
        value = initiative

    totalWeapon = value + weapon
    return totalWeapon

@app.callback(
    Output("totalBallistic", "children"),
    Output("totalPilot", "children"),
    Output("totalStealth", "children"),
    Input("agility", "value"),
    Input("ballistic", "value"),
    Input("pilot", "value"),
    Input("stealth", "value"),
)
def computeAgility(agility, ballistic, pilot, stealth):
    if agility == None:
        value = 1
    else:
        value = agility
  
    totalBallistic = value + ballistic
    totalPilot = value + pilot
    totalStealth = value + stealth

    return totalBallistic, totalPilot, totalStealth



@app.callback(
    Output("totalIntimidation", "children"),
    Output("totalLeadership", "children"),
    Output("totalPsychic", "children"),
    Output("totalSurvival", "children"),
    Input("willpower", "value"),
    Input("intimidation", "value"),
    Input("leadership", "value"),
    Input("psychic", "value"),
    Input("survival", "value"),
)
def computeWillpower(willpower, intimidation, leadership, psychic, survival):
    if willpower == None:
        value = 1
    else:
        value = willpower

  
    totalIntimidation = value + intimidation
    totalLeadership = value + leadership
    totalPsychic = value + psychic
    totalSurvival = value + survival

    return totalIntimidation, totalLeadership, totalPsychic, totalSurvival

@app.callback(
    Output("totalAwareness", "children"),
    Output("totalTech", "children"),
    Output("totalScholar", "children"),
    Output("totalInvestigation", "children"),
    Output("totalMedicae", "children"),
    Input("intelligence", "value"),
    Input("awareness", "value"),
    Input("scholar", "value"),
    Input("tech", "value"),
    Input("medicae", "value"),
    Input("investigation", "value"),
)
def computeIntelligence(intelligence, awareness, investigation, medicae, scholar, tech):
    if intelligence == None:
        value = 1
    else:
        value = intelligence
  
    totalAwareness = value + awareness
    totalTech = value + tech
    totalScholar = value + scholar
    totalInvestigation = value + investigation
    totalMedicae = value + medicae

    return totalAwareness, totalTech, totalScholar, totalInvestigation, totalMedicae

@app.callback(
    Output("totalCunning", "children"),
    Output("totalDeception", "children"),
    Output("totalInsight", "children"),
    Output("totalPersuasion", "children"),
    Input("fellowship", "value"),
    Input("cunning", "value"),
    Input("deception", "value"),
    Input("insight", "value"),
    Input("persuasion", "value"),
)
def computeFellowship(fellowship, cunning, deception, insight, persuasion):
    if fellowship == None:
        value = 1
    else:
        value = fellowship
  
    totalCunning = value + cunning
    totalDeception = value + deception
    totalInsight = value + insight
    totalPersuasion = value + persuasion

    return totalCunning, totalDeception, totalInsight, totalPersuasion

@app.callback(
    Output("totalCost", "children"),
    Output("tier_result", "children"),
    Output("totalResilience", "children"),
    Output("totalDefence", "children"),
    Output("totalWounds", "children"),
    Output("totalShock", "children"),
    Output("totalConviction", "children"),
    Output("totalResolve", "children"),
    Output("threat_level1", "children"),
    Output("threat_level2", "children"),
    Output("threat_level3", "children"),
    Output("threat_level4", "children"),
    inputs=dict(attr=[Input("{}".format(_), "value") for _ in Attributes],
    skill=[Input("{}".format(_), "value") for _ in Skills],
    armour=Input("armour", "value")
    )
)
def xpcost(attr ,skill, armour):
    totalCost = 0
    totalDefence = 0
    totalResilience = 0
    totalWounds = 0
    totalShock = 0
    totalConviction = 0
    totalResolve = 0
    tier_result = 0
    # print(attr)
    # print(skill)
    
    for val in attr:
        # print(val)
        totalCost = totalCost + attribute_cost[val]

    
    for val in skill:
        # print(val)
        totalCost = totalCost + skill_cost[val]

    if totalCost == None:
        value = 0
    else:
        value = totalCost

    if value < 200:
        tier_result = 1
    elif value < 300:
        tier_result  = 2
    elif value < 400:
        tier_result  = 3
    elif value < 500:
        tier_result  = 4
    else:
        tier_result  = 5

    threat_level1 = 'T'
    if value > 75: threat_level1 = 'E'
    if value > 150: threat_level1 = 'A'   

    threat_level2 = 'T'
    if value > 150: threat_level2 = 'E'
    if value > 250: threat_level2 = 'A'

    threat_level3 = 'T'
    if value > 250: threat_level3 = 'E'
    if value > 350: threat_level3 = 'A'

    threat_level4 = 'T'
    if value > 300: threat_level4 = 'E'
    if value > 500: threat_level4 = 'A'

    toughness = attr[1]
    initiative = attr[3]
    willpower = attr[4]

    if toughness == None:
        toughness = 1
    if initiative == None:
        initiative = 1
    if willpower == None:
        willpower = 1
    
    totalDefence = toughness - 1
    totalResilience = toughness + 1 + armour
    totalWounds = toughness + tier_result*2
    totalShock = willpower + tier_result
    totalConviction = willpower
    totalResolve = willpower - 1

    
    return(totalCost, tier_result, totalResilience, totalDefence, totalWounds, totalShock,
            totalConviction, totalResolve, threat_level1, threat_level2, threat_level3, threat_level4)


if __name__ == '__main__':
    application.run(debug=True, port=8080)