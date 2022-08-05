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

def combat_simulator():

    wound_spread = []

    for a in range(100):

        result = random.choice(d6)

        ballistics = 5
        defence = 2

        results = []

        for i in range(ballistics):
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
                    print("Shifting")
                    shifted = shifted + len(results)
                    break
                else:
                    if score == 6:
                        successes += 2
                        results.pop(i)

        # print("Successes: ", successes)
        # print("Shifted: ", shifted)

        ### Damage 

        base_damage = 7
        base_extra_damage = 1

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

        ap = 0

        resilience = 7
        armour = 3

        base_resilience = resilience - armour

        wounds = 5

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


    print("Final Results")
    print(wound_spread)

    df_spread = pd.DataFrame(data=wound_spread, columns=['Result'])

    print(df_spread)

    figure_out=px.histogram(data_frame=df_spread, x='Result', template="ggplot2")

    return(figure_out)









