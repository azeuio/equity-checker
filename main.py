#!/usr/bin/env python3
import pandas as pd
import math
import scipy.stats as stats

# load the datasets
personalities = pd.read_csv("dataset/personnality.csv").drop_duplicates(subset=['uuid'], keep='last')
grid_france_culture = pd.read_csv("dataset/franceculture.csv").drop_duplicates(subset=['diffusion_id'], keep='last')
grid_france_info = pd.read_csv("dataset/franceinfo.csv").drop_duplicates(subset=['diffusion_id'], keep='last')
grid_france_inter = pd.read_csv("dataset/franceinter.csv").drop_duplicates(subset=['diffusion_id'], keep='last')

def split_column(grid: pd.DataFrame, column: str, separator_regex: str = r'\|| |- ') -> pd.DataFrame:
    grid[column] = grid[column].str.split(separator_regex)
    return grid
grid_france_culture = split_column(grid_france_culture, 'personality_ids')
grid_france_info = split_column(grid_france_info, 'personality_ids')
grid_france_inter = split_column(grid_france_inter, 'personality_ids')

def explode_column(grid: pd.DataFrame, column: str) -> pd.DataFrame:
    res = grid.explode(column)
    res.reset_index(drop=True, inplace=True)
    return res
grid_france_culture_exploded = explode_column(grid_france_culture, 'personality_ids')
grid_france_info_exploded = explode_column(grid_france_info, 'personality_ids')
grid_france_inter_exploded = explode_column(grid_france_inter, 'personality_ids')

# make gender a categorical variable
personalities.gender = personalities.gender.astype('category')

# create a new dataframe with only the people
people = personalities[-personalities.isOrganisation]
genders = people.gender.astype('category')
genders = (genders[genders.notna()])

# count the parity in the people dataframe
men = people[people.gender == 'man']
women = people[people.gender == 'woman']
other = people[-(people.gender == 'man')]
other = other[-(other.gender == 'woman')]

# print the results
percentage_of_men = len(men) / len(people)
percentage_of_women = len(women) / len(people)
percentage_of_other = len(other) / len(people)
print(f"Men represent {percentage_of_men * 100:.2f}% of the people in the dataset")
print(f"Women represent {percentage_of_women * 100:.2f}% of the people in the dataset")
print(f"Others represent {percentage_of_other * 100:.2f}% of the people in the dataset")

grid_france_culture_men = grid_france_culture_exploded.merge(men, left_on='personality_ids', right_on='uuid')
grid_france_info_men = grid_france_info_exploded.merge(men, left_on='personality_ids', right_on='uuid')
grid_france_inter_men = grid_france_inter_exploded.merge(men, left_on='personality_ids', right_on='uuid')

grid_france_culture_women = grid_france_culture_exploded.merge(women, left_on='personality_ids', right_on='uuid')
grid_france_info_women = grid_france_info_exploded.merge(women, left_on='personality_ids', right_on='uuid')
grid_france_inter_women = grid_france_inter_exploded.merge(women, left_on='personality_ids', right_on='uuid')

grid_france_culture_other = grid_france_culture_exploded.merge(other, left_on='personality_ids', right_on='uuid')
grid_france_info_other = grid_france_info_exploded.merge(other, left_on='personality_ids', right_on='uuid')
grid_france_inter_other = grid_france_inter_exploded.merge(other, left_on='personality_ids', right_on='uuid')

# print the resulting DataFrame
print(f"{grid_france_culture_men=}")


# get the average of time personalities reappeared in each radio
average_reappearance_france_culture = grid_france_culture_exploded['personality_ids'].value_counts().mean()
average_reappearance_france_info = grid_france_info['personality_ids'].value_counts().mean()
average_reappearance_france_inter = grid_france_inter['personality_ids'].value_counts().mean()

# get the average of time men reappeared in each radio
joined_df = pd.merge(grid_france_culture_exploded, men, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_man_reappearance_france_culture = value_counts.mean()
joined_df = pd.merge(grid_france_info_exploded, men, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_man_reappearance_france_info = value_counts.mean()
joined_df = pd.merge(grid_france_inter_exploded, men, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_man_reappearance_france_inter = value_counts.mean()

# get the average of time women reappeared in each radio
joined_df = pd.merge(grid_france_culture_exploded, women, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_woman_reappearance_france_culture = value_counts.mean()
joined_df = pd.merge(grid_france_info_exploded, women, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_woman_reappearance_france_info = value_counts.mean()
joined_df = pd.merge(grid_france_inter_exploded, women, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_woman_reappearance_france_inter = value_counts.mean()


# get the average of time other reappeared in each radio
joined_df = pd.merge(grid_france_culture_exploded, other, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_other_reappearance_france_culture = value_counts.mean()
joined_df = pd.merge(grid_france_info_exploded, other, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_other_reappearance_france_info = value_counts.mean()
joined_df = pd.merge(grid_france_inter_exploded, other, left_on='personality_ids', right_on='uuid')
value_counts = joined_df['personality_ids'].value_counts()
average_other_reappearance_france_inter = value_counts.mean()


# # print the results
print(f"Out of {grid_france_culture.diffusion_id.count()} emissions, {grid_france_culture_exploded.personality_ids.count()} personalities appeared in France Culture")
print(f"Out of {grid_france_info.diffusion_id.count()} emissions, {grid_france_info_exploded.personality_ids.count()} personalities appeared in France Info")
print(f"Out of {grid_france_inter.diffusion_id.count()} emissions, {grid_france_inter_exploded.personality_ids.count()} personalities appeared in France Inter")

print()
print(f"Average of time people reappeared in France Culture: {average_reappearance_france_culture:.0f}")
print(f"Average of time people reappeared in France Info: {average_reappearance_france_info:.0f}")
print(f"Average of time people reappeared in France Inter: {average_reappearance_france_inter:.0f}")

print()
print(f"Average of time men reappeared in France Culture : {average_man_reappearance_france_culture:.0f}")
print(f"Average of time men reappeared in France Info : {average_man_reappearance_france_info:.0f}")
print(f"Average of time men reappeared in France Inter : {average_man_reappearance_france_inter:.0f}")

print()
print(f"Average of time woman reappeared in France Culture : {average_woman_reappearance_france_culture:.0f}")
print(f"Average of time woman reappeared in France Info : {average_woman_reappearance_france_info:.0f}")
print(f"Average of time woman reappeared in France Inter : {average_woman_reappearance_france_inter:.0f}")

print()
print(f"Average of time other reappeared in France Culture : {average_other_reappearance_france_culture:.0f}")
print(f"Average of time other reappeared in France Info : {average_other_reappearance_france_info:.0f}")
print(f"Average of time other reappeared in France Inter : {average_other_reappearance_france_inter:.0f}")


def perform_normal_approximation_test(observed_percentage, total_simulations):
    expected_mean = 0.5 * total_simulations
    expected_std_dev = math.sqrt(total_simulations * 0.5 * 0.5)
    
    z_score = (observed_percentage * total_simulations - expected_mean) / expected_std_dev
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    return p_value

# perform the test
print()

print("Performing normal approximation test for Radio France")
p_all = perform_normal_approximation_test(percentage_of_men, grid_france_culture_exploded.personality_ids.count() - other.uuid.count())
# p_france_culture = perform_normal_approximation_test()
if p_all < 0.05:
    print("It is likely that equity is not respected in Radio France")
else:
    print("It is likely that equity is respected in Radio France")
