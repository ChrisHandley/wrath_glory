import random
import pandas as pd
import plotly.io as pio
import numpy as np
import plotly.express as px


# pio.renderers.default = 'svg'

d6 = [1, 2, 3, 4, 5, 6]

wg_icons = {
    '1': 'miss',
    '2': 'miss',
    '3': 'miss',
    '4': 'icon',
    '5': 'icon',
    '6': 'exalted',
}

def combat_simulator(attackpool, base_damage, base_extra_damage, ap,
                     defence, resilience, wounds, armour):

    wound_spread = []
    
    # print(defence, resilience, wounds, armour)
    if defence == None: defence = 1
    if resilience == None: resilience = 1
    if wounds == None: wounds = 1
    if armour == None: armour = 0

    for a in range(500):

        results = []

        for i in range(attackpool):
            results.append(random.choice(d6))

        results.sort()
        # print("Dice Roll: ", results)
        successes = 0

        for i, score in reversed(list(enumerate(results))):
            # print(i, score)
            if score < 4:
                results.pop(i)

        for i, score in reversed(list(enumerate(results))):
            # print(i, score)
            if score < 6:
                successes += 1
                results.pop(i)

        shifted=0

        if successes >= defence:
            shifted = shifted + len(results)
        else:
            for i, score in reversed(list(enumerate(results))):
                if successes >= defence:
                    # print("Shifting")
                    shifted = shifted + len(results)
                    break
                else:
                    if score == 6:
                        successes += 2
                        results.pop(i)

        # print("Successes: ", successes)
        # print("Shifted: ", shifted)

        ### Damage 

        damage = base_damage

        extra_damage_dice = base_extra_damage + shifted

        results = []

        for i in range(extra_damage_dice):
            results.append(random.choice(d6))

        # print("Damage Results: ", results)

        for i, val in enumerate(results):
            if val == 6:
                damage = damage + 2
            elif val >= 4:
                damage = damage + 1

        # print("Damage Dealt: ", damage)

        ### Armour



        base_resilience = resilience - armour

        wounds_remaining = 0

        armour_remaining = armour - ap

        if armour_remaining < 0: armour_remaining = 0

        base_resilience = base_resilience + armour_remaining

        wounds_dealt = damage - base_resilience

        if wounds_dealt < 0: wounds_dealt = 0

        wounds_remaining = wounds - wounds_dealt

        if wounds_remaining < 0: wounds_remaining = 0

        # print("Resilience: ", resilience)
        # print("Armour: ", armour)
        # print("Wounds: ", wounds)
        # print("Wounds Remaining: ", wounds_remaining)
        wound_spread.append(wounds_remaining)


    # print("Final Results")
    # print(wound_spread)

    df_spread = pd.DataFrame(data=wound_spread, columns=['Result'])

    # print(df_spread)

    figure_out=px.histogram(data_frame=df_spread, x='Result', template="ggplot2")
    figure_out.update_xaxes(tick0=1.0, dtick=1.0)
    return(figure_out)

def combat_simulator2(attackpool, base_damage, base_extra_damage, ap):
    
    print(attackpool)
    print(base_damage)
    print(base_extra_damage)
    print(ap)
    
    return "Test"











