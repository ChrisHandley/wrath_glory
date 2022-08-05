import dash
import dash_bootstrap_components as dbc
import base64
from dash import Output, Input, ctx, html, dcc
from factionKeywords import keywords_factions
from humanKeywords import keywords_humans_imperial, keywords_humans_imperial_sub, keywords_humans_chaos, keywords_humans_chaos_sub
from astartesKeywords import keywords_astartes_imperial, keywords_astartes_imperial_sub, keywords_primaris_imperial, keywords_primaris_imperial_sub
from astartesKeywords import keywords_astartes_chaos, keywords_astartes_chaos_sub 
from aeldariKeywords import keywords_aeldari, keywords_aeldari_sub, keywords_drukhari, keywords_drukhari_sub
from abhumanKeywords import keywords_abhumans_chaos, keywords_abhumans_chaos_sub, keywords_abhumans_imperial, keywords_abhumans_imperial_sub

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SLATE],
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
    {'label':'Adeptus Astartes', 'value':'Adeptus Astartes'},
    {'label':'Aeldari', 'value':'Aeldari'},
    {'label':'Drukhari', 'value':'Drukhari'},
    {'label':'Human', 'value':'Human'},
    {'label':'Kroot', 'value':'Kroot'},
    {'label':'Ogryn', 'value':'Ogryn'},
    {'label':'Ork', 'value':'Ork'},
    {'label':'Ratling', 'value':'Ratling'},
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
    "Ogryn": {
        "strength": 12,
        "toughness": 12,
        "agility": 7,
        "initiative": 4,
        "willpower": 8,
        "intellect": 1,
        "fellowship": 4,
        "speed": 8
    },
    "Ratling": {
        "strength": 6,
        "toughness": 6,
        "agility": 10,
        "initiative": 10,
        "willpower": 8,
        "intellect": 8,
        "fellowship": 10,
        "speed": 7
    },
    "Kroot": {
        "strength": 12,
        "toughness": 12,
        "agility": 12,
        "initiative": 12,
        "willpower": 10,
        "intellect": 6,
        "fellowship": 6,
        "speed": 10
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
    "Aeldari": {
        "strength": 8,
        "toughness": 8,
        "agility": 12,
        "initiative": 12,
        "willpower": 10,
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
    "Adeptus Astartes": "[Chapter], Adeptus Astartes",
    "Primaris Astartes": "[Chapter], Adeptus Astartes, Primaris",
    "Aeldari": None,
    "Drukhari": None,
    "Ork": "[Clan]",
    "Ogryn": "Abhuman",
    "Ratling": "Abhuman",
    "Kroot": None,
}

faction_list=keywords_factions
human_imperial_factions = keywords_humans_imperial


app.layout = dbc.Container([

    dbc.NavbarSimple(
    children=[
        dbc.Row([
            dbc.Col(html.Div("Total XP:"), width=3),
            dbc.Col(html.Div(id="totalCostnav", style={"textAlign": "right"},)),
        ])
    ],
    brand="Wrath and Glory Character Builder",
    color="primary",
    dark=True,
    sticky="top"
    ),

    dbc.Row(html.Img(src=app.get_asset_url('WrathGloryBanner.png')), style={"textAlign": "center"}),
    dbc.Row(dbc.Col(html.H1("Wrath and Glory Character Builder",
                            style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div("Total XP", style={"textAlign": "left"})),
                    dbc.Col(html.Div("Tier", style={"textAlign": "left"})),
                ]
            ),
            dbc.Row(
                [
                    # dbc.Col(html.Div(id="totalCost", style={"textAlign": "left"})),
                    dbc.Col(html.Div(id="totalCost", style={"textAlign": "left"},)),
                    dbc.Col(html.Div(id="tier_result", style={"textAlign": "left"})),
                    # dbc.Col(dcc.Input(
                    #     id="tier".format("number"),
                    #     type="number",
                    #     placeholder="input type {}".format("number"), min=1, max=5, value=1)),

                ]
            ),
            html.Hr(),

            
            dbc.Col([
                dbc.Row([
                        dbc.Col(
                        # html.Div(id='placeholder'),
                            html.H5("Tier",
                            style={"textAlign": "left"}), width=2),
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
                    dbc.Col(html.H5("NPC Threat Level", style={"textAlign": "left"}), width=2),
                    dbc.Col(html.H5(id="threat_level1", style={"textAlign": "center"}), width=2),
                    dbc.Col(html.H5(id="threat_level2", style={"textAlign": "center"}), width=2),
                    dbc.Col(html.H5(id="threat_level3", style={"textAlign": "center"}), width=2),
                    dbc.Col(html.H5(id="threat_level4", style={"textAlign": "center"}), width=2),
                    
                ])    
            ]),
            # dbc.Col(html.Button(id='run', children='PDF', n_clicks=0),)
        ], 
    ),   
    html.Hr(),
    dbc.Row(
        [
            dbc.Col([
                # dbc.Row([dbc.DropdownMenu(label="species dropdown", size="lg", children=species, className="mb-3")]),
                dbc.Row(
                    [
                        dbc.Col(html.H5("Species"), width=3),
                        dbc.Col(
                            dcc.Dropdown(options=species_list, id="species_selected",
                                multi=False, clearable=False, value="Human"
                                ),
                                width=3, style={"textAlign": "left"}
                            ),
                        dbc.Col(html.H5("Faction"), width=3),
                        dbc.Col(
                            dcc.Dropdown(id="faction_selected",
                                multi=False, clearable=False, #value="Imperium"
                                ),
                                width=3, style={"textAlign": "left"}
                            ),
                        # dbc.Col(html.Div(id="maximums"), width=2),
                    ]),
            ]),
        ]
    ),

    html.Hr(),
    dbc.Row([
        dbc.Col(html.H5("Species Keywords"), width=3),
        dbc.Col(html.Div(id="species_keywords"), width=6),
    ]),
    dbc.Row([
        dbc.Col(html.H5("Faction Keyword"), width=3),
        dbc.Col(dcc.Dropdown(id="faction_keyword_list", multi=False,
                clearable=True, placeholder="Select Keywords"), width=8),
    ]),
    dbc.Row([
        dbc.Col(html.H5("Sub Faction Keyword"), width=3),
        dbc.Col(dcc.Dropdown(id="subfaction_keyword_list", multi=True,
                clearable=True, placeholder="Select Keywords"), width=8),
    ]),
    dbc.Row([
        dbc.Col(html.H5("ANY Keyword"), width=3),
        dbc.Col(dcc.Dropdown(id="all_keywords", multi=True,
                clearable=True, placeholder="Any Keyword"), width=8)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.H5("Attributes",
                            style={"textAlign": "center"}), width=3),
        dbc.Col([
            # html.Div(id='placeholder'),
            html.Div(
                        id="attribute_check"),], width=7
        ),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("S", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="strength", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_strength', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_strength', n_clicks=0),),)
            ]),
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("A", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="agility", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_agility', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_agility', n_clicks=0),),)
            ]),
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("WIL", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="willpower", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_willpower', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_willpower', n_clicks=0),),)
            ]),
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("FEL", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="fellowship", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_fellowship', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_fellowship', n_clicks=0),),)
            ]),
        ]),
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("T", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="toughness", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_toughness', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_toughness', n_clicks=0),),)
            ]),
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("I", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="initiative", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_initiative', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_initiative', n_clicks=0),),)
            ]),
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("INT", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="intelligence", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_intelligence', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_intelligence', n_clicks=0),),)
            ]),
            dbc.Row([
                dbc.Col(dbc.Row(html.Div("ARM", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(html.Div(id="armour", style={"textAlign": "center"})),),
                dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_armour', n_clicks=0),),),
                dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_armour', n_clicks=0),),)
            ]),
        ]),
    ]),
    html.Hr(),
    dbc.Row(
        dbc.Col([
            
            
            dbc.Row(
                [
                    dbc.Col(
                        html.Div("Conviction", style={"textAlign": "left"}),
                    width=3),
                    dbc.Col(
                        html.Div("Size", style={"textAlign": "left"}),
                    width=3)
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(id="totalConviction"),width=3),
                    dbc.Col(html.Div(id="size", style={"textAlign": "left"}), width=1),
                    dbc.Col(dbc.Button("+1", className="me-md-2", color="success", id='up_size', n_clicks=0), width=2),
                    dbc.Col(dbc.Button("-1", className="me-md-2", color="danger", id='down_size', n_clicks=0), width=2),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div("Resolve", style={"textAlign": "left"}),
                    width=3),
                    dbc.Col(
                        html.Div("Speed", style={"textAlign": "left"}),
                    width=2)
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(id="totalResolve"), width=3),
                    dbc.Col(html.Div(id="speed", style={"textAlign": "left"}), width=1),
                    dbc.Col(dbc.Button("+1", className="me-md-2", color="success", id='up_speed', n_clicks=0), width=2),
                    dbc.Col(dbc.Button("-1", className="me-md-2", color="danger", id='down_speed', n_clicks=0), width=2),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div("Defence", style={"textAlign": "left"}),
                    width=3),
                    dbc.Col(
                        html.Div("Resilience", style={"textAlign": "left"}),
                    width=2)
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(id="totalDefence"), width=3),
                    dbc.Col(html.Div(id="totalResilience"), width=2),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div("Wounds", style={"textAlign": "left"}),
                    width=3),
                    dbc.Col(
                        html.Div("Shock", style={"textAlign": "left"}),
                    width=2)
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(id="totalWounds"),width=3),
                    dbc.Col(html.Div(id="totalShock"),),
                ]
            ),
        ]),
    ),
    html.Hr(),
    dbc.Row(dbc.Col(html.H3("Skills",
                            style={"textAlign": "center"}), width=4)),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Athletics (S)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Medicae (INT)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="athletics")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_athletics', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_athletics', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalAthletics", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="medicae")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_medicae', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_medicae', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalMedicae", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Awarness (INT)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Persuasion (FEL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="awareness")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_awareness', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_awareness', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalAwareness", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="persuasion")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_persuasion', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_persuasion', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalPersuasion", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),

    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Ballistic Skill (A)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Pilot (A)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="ballistic")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_ballistic', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_ballistic', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalBallistic", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="pilot")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_pilot', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_pilot', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalPilot", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),

    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Cunning (FEL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Psychic (WIL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="cunning")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_cunning', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_cunning', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalCunning", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="psychic")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_psychic', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_psychic', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalPsychic", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),

    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Deception (FEL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Scholar (INT)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="deception")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_deception', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_deception', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalDeception", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="scholar")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_scholar', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_scholar', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalScholar", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),

    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Insight (FEL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Stealth (A)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="insight")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_insight', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_insight', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalInsight", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="stealth")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_stealth', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_stealth', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalStealth", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),

    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Intimidation (WIL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Survival (WIL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="intimidation")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_intimidation', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_intimidation', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalIntimidation", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="survival")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_survival', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_survival', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalSurvival", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),


    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Investigation (INT)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Tech (INT)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="investigation")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_investigation', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_investigation', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalInvestigation", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="tech")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_tech', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_tech', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalTech", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),

    dbc.Row(
        [
            dbc.Col(dbc.Row(html.Div("Leadership (WIL)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
            dbc.Col(dbc.Row(html.Div("Weapon Skill (I)", style={"textAlign": "left"})), width=3),
            dbc.Col(dbc.Row(html.Div("Total", style={"textAlign": "right"})), width=3),
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Row(html.Div(id="leadership")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_leadership', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_leadership', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalLeadership", style={"textAlign": "right"})), width=1),
                    dbc.Col(dbc.Row(html.Div(id="weapon")), width=1),
                    dbc.Col(dbc.Row(dbc.Button("+1", className="me-1", color="success", id='up_weapon', n_clicks=0)), ),
                    dbc.Col(dbc.Row(dbc.Button("-1", className="me-1", color="danger", id='down_weapon', n_clicks=0)), ),
                    dbc.Col(dbc.Row(html.Div(id="totalWeapon", style={"textAlign": "right"})), width=1),
                ]),
            ],),
            
        ]
    ),
])



@app.callback(
    # outputs=dict(attr_out=[Output("{}".format(_), "children") for _ in Attributes]),
    # Output('placeholder', 'children'),
    Output("speed", "children"),
    inputs=dict(ups=Input("up_speed", "n_clicks"),
                downs=Input("down_speed", "n_clicks"),
                attr_values=Input("speed", "children")
    )
)
def button_attributes4(ups, downs, attr_values):
    attr_out = attr_values
    print("value ", attr_values)
    if attr_out == None:
        attr_out = 1
    if "up_speed" == ctx.triggered_id:
        attr_out +=1
        if attr_out > 12:
            attr_out = 12
    if "down_speed" == ctx.triggered_id:
        attr_out += -1
        if attr_out < 1:
            attr_out = 1
    # placeholder = "TEST"
    placeholder = attr_out
    return placeholder

@app.callback(
    # outputs=dict(attr_out=[Output("{}".format(_), "children") for _ in Attributes]),
    # Output('placeholder', 'children'),
    Output("size", "children"),
    inputs=dict(ups=Input("up_size", "n_clicks"),
                downs=Input("down_size", "n_clicks"),
                attr_values=Input("size", "children")
    )
)
def button_attributes3(ups, downs, attr_values):
    attr_out = attr_values
    print("value ", attr_values)
    if attr_out == None:
        attr_out = 1
    if "up_size" == ctx.triggered_id:
        attr_out +=1
        if attr_out > 12:
            attr_out = 12
    if "down_size" == ctx.triggered_id:
        attr_out += -1
        if attr_out < 1:
            attr_out = 1
    # placeholder = "TEST"
    placeholder = attr_out
    return placeholder


@app.callback(
    # outputs=dict(attr_out=[Output("{}".format(_), "children") for _ in Attributes]),
    # Output('placeholder', 'children'),
    Output("armour", "children"),
    inputs=dict(ups=Input("up_armour", "n_clicks"),
                downs=Input("down_armour", "n_clicks"),
                attr_values=Input("armour", "children")
    )
)
def button_attributes2(ups, downs, attr_values):
    attr_out = attr_values
    print("value ", attr_values)
    if attr_out == None:
        attr_out = 1
    if "up_armour" == ctx.triggered_id:
        attr_out +=1
        if attr_out > 12:
            attr_out = 12
    if "down_armour" == ctx.triggered_id:
        attr_out += -1
        if attr_out < 1:
            attr_out = 1
    # placeholder = "TEST"
    placeholder = attr_out
    return placeholder


@app.callback(
    # outputs=dict(attr_out=[Output("{}".format(_), "children") for _ in Attributes]),
    # Output('placeholder', 'children'),
    output=[Output("{}".format(_), "children") for _ in Attributes],
    inputs=dict(ups=[Input("up_{}".format(_), "n_clicks") for _ in Attributes],
                downs=[Input("down_{}".format(_), "n_clicks") for _ in Attributes],
                attr_values=[Input("{}".format(_), "children") for _ in Attributes]
    )
)
def button_attributes(ups, downs, attr_values):
    attr_out = attr_values
    for i, attr in enumerate(attr_values):
        if attr == None:
            attr_out[i] = 1
    for i, attr in enumerate(Attributes):
        if "up_{}".format(attr) == ctx.triggered_id:
            msg = str(attr) + " Button Up was most recently clicked"
            attr_out[i] +=1
            if attr_out[i] > 12:
                attr_out[i] = 12
        if "down_{}".format(attr) == ctx.triggered_id:
            msg = str(attr) + " Button Down was most recently clicked"
            attr_out[i] += -1
            if attr_out[i] < 1:
                attr_out[i] = 1
            
    # placeholder = "TEST"
    placeholder = attr_out
    return placeholder

@app.callback(
    # outputs=dict(attr_out=[Output("{}".format(_), "children") for _ in Attributes]),
    # Output('placeholder', 'children'),
    output=[Output("{}".format(_), "children") for _ in Skills],
    inputs=dict(ups=[Input("up_{}".format(_), "n_clicks") for _ in Skills],
                downs=[Input("down_{}".format(_), "n_clicks") for _ in Skills],
                attr_values=[Input("{}".format(_), "children") for _ in Skills]
    )
)
def button_skill(ups, downs, attr_values):
    attr_out = attr_values
    for i, attr in enumerate(attr_values):
        if attr == None:
            attr_out[i] = 0
    for i, attr in enumerate(Skills):
        if "up_{}".format(attr) == ctx.triggered_id:
            msg = str(attr) + " Button Up was most recently clicked"
            attr_out[i] +=1
            if attr_out[i] > 8:
                attr_out[i] = 8
        if "down_{}".format(attr) == ctx.triggered_id:
            msg = str(attr) + " Button Down was most recently clicked"
            attr_out[i] += -1
            if attr_out[i] < 0:
                attr_out[i] = 0
            
    # placeholder = "TEST"
    placeholder = attr_out
    return placeholder

@app.callback(
    Output("subfaction_keyword_list", "options"),
    Input("faction_keyword_list", "value"),
    Input("faction_selected", "value"),
    Input("species_selected", "value")
)
def subfaction_keyword_select(faction_keyword_list, faction_selected, species_selected):
    print(faction_selected, species_selected)
    print(faction_keyword_list)
    subfaction_keyword_list = [{'label': 'Unaligned', 'value': 'Unaligned'}]
    if faction_keyword_list == None:
        subfaction_keyword_list = [{'label': 'Unaligned', 'value': 'Unaligned'}]
    elif species_selected == "Aeldari":
        subfaction_keyword_list = keywords_aeldari_sub[faction_selected]
    elif species_selected == "Drukhari":
        subfaction_keyword_list = keywords_drukhari_sub[faction_selected]
    elif faction_selected == "Imperium":
        if species_selected == "Ogryn":
            subfaction_keyword_list = keywords_abhumans_imperial_sub[faction_keyword_list]
        elif species_selected == "Ratling":
            subfaction_keyword_list = keywords_abhumans_imperial_sub[faction_keyword_list]
        elif species_selected == "Human":
            subfaction_keyword_list = keywords_humans_imperial_sub[faction_keyword_list]
        elif species_selected == "Adeptus Astartes":
            subfaction_keyword_list = keywords_astartes_imperial_sub
        elif species_selected == "Primaris Astartes":
            subfaction_keyword_list = keywords_primaris_imperial_sub
    elif faction_selected == "Chaos":
        if species_selected == "Ogryn":
            subfaction_keyword_list = keywords_abhumans_chaos_sub[faction_keyword_list]
        elif species_selected == "Ratling":
            subfaction_keyword_list = keywords_abhumans_chaos_sub[faction_keyword_list]
        elif species_selected == "Human":
            subfaction_keyword_list = keywords_humans_chaos_sub[faction_keyword_list]
        elif species_selected == "Adeptus Astartes":
            subfaction_keyword_list = keywords_astartes_chaos_sub
    print(subfaction_keyword_list)
    return(subfaction_keyword_list)

@app.callback(
    Output("faction_keyword_list", "options"),
    Input("faction_selected", "value"),
    Input("species_selected", "value")
)
def faction_keyword_select(faction_selected, species_selected):
    # print(faction_selected, species_selected)
    faction_keyword_list = [{'label': 'Unaligned', 'value': 'Unaligned'}]
    if faction_selected == "Aeldari":
        faction_keyword_list = keywords_aeldari
    if faction_selected == "Drukhari":
        faction_keyword_list = keywords_drukhari
    if faction_selected == "Imperium":
        if species_selected == "Ogryn":
            faction_keyword_list = keywords_abhumans_imperial
        elif species_selected == "Ratling":
            faction_keyword_list = keywords_abhumans_imperial
        elif species_selected == "Human":
            faction_keyword_list = human_imperial_factions
        elif species_selected == "Adeptus Astartes":
            faction_keyword_list = keywords_astartes_imperial
        elif species_selected == "Primaris Astartes":
            faction_keyword_list = keywords_primaris_imperial
    elif faction_selected == "Chaos":
        if species_selected == "Ogryn":
            faction_keyword_list = keywords_abhumans_chaos
        elif species_selected == "Ratling":
            faction_keyword_list = keywords_abhumans_chaos
        elif species_selected == "Human":
            faction_keyword_list = keywords_humans_chaos
        elif species_selected == "Adeptus Astartes":
            faction_keyword_list = keywords_astartes_chaos
    else:
        faction_keyword_list = [{'label': 'Unaligned', 'value': 'Unaligned'}]
    return(faction_keyword_list)

@app.callback(
    Output("faction_selected", "options"),
    Input("species_selected", "value")
)
def faction_select(species_selected):
    # print("species ", species_selected)
    # print(faction_list)
    faction_selected = faction_list[species_selected]
    if faction_selected == None:
        faction_selected = {'label': 'None', 'value': 'none'}
    # faction_selected = [{'label': 'Anhrathe', 'value': 'Anhrathe'},
    #                     {'label': 'Asuryani', 'value': 'Asuryani'}]
    return(faction_selected)


@app.callback(
    Output("attribute_check", "children"),
    Output('species_keywords', 'children'),
    inputs=dict(attr=[Input("{}".format(_), "children") for _ in Attributes],
    # species_selected=Input("placeholder", "value"),
    speed=[Input('speed', 'children')],
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
    Input("strength", "children"),
    Input("athletics", "children"),
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
    Input("initiative", "children"),
    Input("weapon", "children"),
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
    Input("agility", "children"),
    Input("ballistic", "children"),
    Input("pilot", "children"),
    Input("stealth", "children"),
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
    Input("willpower", "children"),
    Input("intimidation", "children"),
    Input("leadership", "children"),
    Input("psychic", "children"),
    Input("survival", "children"),
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
    Input("intelligence", "children"),
    Input("awareness", "children"),
    Input("scholar", "children"),
    Input("tech", "children"),
    Input("medicae", "children"),
    Input("investigation", "children"),
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
    Input("fellowship", "children"),
    Input("cunning", "children"),
    Input("deception", "children"),
    Input("insight", "children"),
    Input("persuasion", "children"),
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
    Output("totalCostnav", "children"),
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
    inputs=dict(attr=[Input("{}".format(_), "children") for _ in Attributes],
    skill=[Input("{}".format(_), "children") for _ in Skills],
    armour=Input("armour", "children")
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
    totalResilience = toughness + 1 #+ armour
    totalWounds = toughness + tier_result*2
    totalShock = willpower + tier_result
    totalConviction = willpower
    totalResolve = willpower - 1

    
    return(totalCost, totalCost, tier_result, totalResilience, totalDefence, totalWounds, totalShock,
            totalConviction, totalResolve, threat_level1, threat_level2, threat_level3, threat_level4)


if __name__ == '__main__':
    application.run(debug=True, port=8080)