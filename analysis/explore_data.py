'''
This project constists of a SAS portfolio redone in python and is meant to showcase statistical data analytics as well as use of sql and web development. 
Here is the analysis portion of the project. 
'''
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

def load_table(table_name, db_path="../data/portfolio.db"):
    """
    Helper Function that loads tables from the SQLite db into a Pandas DataFrame
    """
    engine = create_engine(f"sqlite:///{db_path}")
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df

'''
One theory about the cause of schizophrenia involves a change in the activity of a substance called dopamine in the central nervous system. To test this theory, dopamine activity was measured for samples of psychotic and non-psychotic patients
'''
schizo = load_table("Schizo")
psychotic = schizo.loc[schizo["Status"] == "P", "Dopamine"]
nonpsychotic = schizo.loc[schizo["Status"] =="N", "Dopamine"]
print("Schizo Dataset:")
print(schizo.head())
print(schizo.tail(), "\n")

# Boxplot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Status', y='Dopamine', data=schizo)

plt.title('Dopamine Activity in Psychotic vs Non-Psychotic Patients', fontsize=16)
plt.xlabel('Patient Status', fontsize=14)
plt.ylabel('Dopamine Activity', fontsize=14)

plt.savefig("schizo_box.png")
plt.close()

# Equality of Variance
t_stat, p_value = stats.levene(psychotic, nonpsychotic,center="mean", proportiontocut=0.1)
print("Equality of Variance")
print("t-statistic: ", t_stat)
print("p-value: ", p_value)
del t_stat, p_value 
# Equality of Means
t_stat, p_value = stats.ttest_ind(psychotic, nonpsychotic, equal_var=True)
print("\nEquality of Means")
print("t-statistic: ", t_stat)
print("p-value: ", p_value)
del t_stat, p_value
'''
Equality of variance: 
    H0: Null Hypothesis assumes the variance is equal
    H1: Alternative Hypothesis assumes the variance is not equal

t-statistic:  0.024354255947852118
p-value:  0.8773485696953314

Since the p-value is greater than the alpha (.10), we fail to reject the H0.
Therefore the variance between the populations are not significantly different than each other and the assumption of homogeneity is met.


Equality of means:
    H0: Null Hypothesis assumes the means are equal. 
    H1: Alternative Hypothesis assumes the means are not equal.

t-statistic:  3.936422120611183
p-value:  0.000658676096416126

Since the p-value is less than the alpha (.05), we reject the null hypothesis and conclude that the means between the groups are not equal. 


Conclusion:
    The equal variance and the unequal means support the theory that the change in dopamine has an affect on the causation of schizophrenia.
'''


'''
A landscaper took pH measurements on 50 soil samples from ground next to a new building. The results are in the data set soil.txt, which only has one variable. Based on the soil composition in the general area, the pH should be less than 6.5. 
'''
print("\n\nSoil Dataset:")
soil = load_table("Soil")
ph = soil["Ph"]
ph_mean = ph.mean()
ph_std = ph.std()
n = len(ph)
confidence_level = 0.99
df = n - 1
t_critical = stats.t.ppf((1 + confidence_level) / 2, df)

margin_of_error = t_critical * (ph_std / (n ** 0.5))
confidence_interval = (ph_mean - margin_of_error, ph_mean + margin_of_error)
print(f"99% Confidence Interval: ({confidence_interval[0]:.3f}, {confidence_interval[1]:.3f})")

mu = 6.5
# Since we are testing if mean < 6.5, it's a left-tailed test
t_stat, p_value = stats.ttest_1samp(ph, mu, alternative='less')
print("t-statistic: ", t_stat)
print("One-sided p-value: ", p_value)
del t_stat, p_value 
'''
99% Confidence Interval: (5.998, 6.596)

One-sided left-tail t-test:
    H0: assumes mean is equal to 6.5 
    h1: assumes mean is less than 6.5

t-statistic:  -1.821434153378776
one-sided p-value:  0.03732426732414688

Conclusion: 
    Since the p-value is less than 0.05, we can reject the null hypothesis.
    This indicates the mean is less than 6.5 at the 5% significance level. 
    This conclusion is consistent with the 99% confidence interval, which does not include 6.5.
'''


'''
The Lamb dataset gives the pulmonary vascular resistance (PVR) in eight lambs before and after infusion of the drug histamine. Determine if histamine increases mean PVR
'''
print("\n\nLamb Dataset")
lamb = load_table("lamb")
print(lamb.head())

t_stat, p_value = stats.ttest_rel(lamb["After"], lamb["Before"], alternative="greater")
print("t-statistic: ", t_stat)
print("One-sided p-value: ", p_value)
del t_stat, p_value
'''
T-test on two related samples:
    H0: the mean of the distribution underlying the two samples are equal
    H1: the mean of the distribution underlying the first sample is greater than the mean of the distribution underlying the second sample.

t-statistic:  1.8849213241837013
One-sided p-value:  0.050714844196921315

Conclusion:
At the significance level of α = 0.05, the p-value of 0.0507 slightly exceeds the threshold, leading us to fail to reject the null hypothesis. This suggests that there is insufficient statistical evidence to conclude that histamine increases mean PVR in lambs. 
However, the p-value is slightly above the significance level, indicating a trend that may warrant further investigation.
'''


'''
After rolling a die 150 times, the results are given in the Dice dataset. Perform a test to determine if all faces are equally likely. 
'''
print("\n\nDice Dataset:")
dice = load_table("Dice")
print(dice)
obs = dice["Frequency"].values
total = obs.sum()    # 150 
expected = np.full(shape=6, fill_value=total/6)
chi_stat, p_value = stats.chisquare(f_obs=obs, f_exp=expected)

print("Chi-square Statistic:", chi_stat)
print("p-value:", p_value)
del chi_stat, p_value

'''
Chi-square test for uniform distribution:
    H0: There's even probablity amongst each face
    H1: At least one face has a different probablity

Chi-square Statistic: 10.0
p-value: 0.07523524614651217

Conclusion:
    At a significance level of α = 0.05, the p-value is 0.0752, which excedes the alpha, so we fail to reject the null hypothesis.
    This suggests there is no statistical evidence that all faces are not equally likely.
'''

'''
A random sample of 156 mean and 144 women was randomly chosen.
Each individual was then classified according to Political Affiliation. 
Test whether or not gender and political affiliation are independent at the α = .10 significance level.
'''
print("\n\nPolitical Affiliation Dataset:")
pol_aff = load_table("Political_Affiliation")
contingency = pd.pivot_table(
    pol_aff, 
    values="Frequency", 
    index="Gender", 
    columns="Affiliation", 
    aggfunc="sum"
).fillna(0)
print(contingency)

chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
print("\nChi-square Statistic:", chi2)
print("p-value:", p_value)
print("Degrees of Freedom:", dof)
print("Expected Frequencies:\n", expected)
del chi2, p_value, dof, expected
'''
Chi-Square Test of Independence:
    H0: Gender and political affiliation are independent
    H1: They are not independent

Chi-square Statistic: 6.432856673241292
p-value: 0.040098019431676075
Degrees of Freedom: 2
Expected Frequencies:
 [[57.6  24.96 61.44]
 [62.4  27.04 66.56]]

Conclusion:
    At a significance level of α = .10, and a p-value of 0.0401, we reject the null hypothesis.
    Therefore, gender and political affiliation are significantly not 
    independent, and the probablity of one does not affect the other.
'''


'''
The dataset shows the relationship between hair color and eye color 
for 6800 randomly selected German men.
'''
print("\n\nHair/Eye Color Dataset:")
hair = load_table("Hair_Eye_Color")

contingency_hair = pd.pivot_table(
    hair,
    values="Frequency",
    index="EyeColor",
    columns="HairColor",
    aggfunc="sum"
).fillna(0)
print(contingency_hair)

chi2_hair, p_hair, dof_hair, expected_hair = stats.chi2_contingency(contingency_hair)
print("\nChi-square statistic:", chi2_hair)
print("p-value:", p_hair)
print("Degrees of Freedom:", dof_hair)
print("Expected Frequencies:\n", expected_hair)
'''
Chi-Square Test of Independence:
    H0: eye color and hair color are independent 
    H1: they are not independent

Chi-square statistic: 1073.507564281902
p-value: 1.124430788658892e-228
Degrees of Freedom: 6
Expected Frequencies:
 [[ 505.56661765 1169.45867647 1088.02235294   47.95235294]
 [ 154.13397059  356.53720588  331.70941176   14.61941176]
 [ 563.29941176 1303.00411765 1212.26823529   53.42823529]]

Conclusion:    
    At a significance level of α = 0.05, and a p-value of 1.12443, we fail to reject the null hypothesis.
    With a high p-value, there is significant evidence that hair color and eye color are very independent,
    and the probability of one can affect the probablity of the other. 
'''

