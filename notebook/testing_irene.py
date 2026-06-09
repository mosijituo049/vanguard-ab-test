# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: venv
#     language: python
#     name: venv
# ---

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# %matplotlib inline


# %%
test=pd.read_csv('../data/raw/df_final_experiment_clients.txt')
test.head()

# %%
test.isna().sum()

# %%
test.duplicated().sum()

# %%
customer=pd.read_csv('../data/raw/df_final_demo.txt')
customer.head()

# %%
web1=pd.read_csv('../data/raw/df_final_web_data_pt_1.txt')
web1.head()

# %%
web2=pd.read_csv('../data/raw/df_final_web_data_pt_2.txt')
web2.head()

# %%
web_df=pd.concat([web1, web2])
web_df.duplicated().sum()

# %%
web_df.head()

# %%
web_df.shape

# %%
web_df=web_df.drop_duplicates()

# %%
web_df.isna().sum()

# %%
web_df.duplicated().sum()

# %%
web_df.shape

# %%
customer.shape

# %%
test.shape

# %%
customer_test= pd.merge(customer, test, on='client_id')
customer_test.head()

# %%
customer_test.duplicated().sum()

# %%
customer_test.isna().sum()

# %%
customer_test.client_id.nunique()

# %%
customer_test.loc[customer_test.isna().any(axis=1)]

# %%
experiment=pd.merge(web_df,customer_test, on='client_id', how='left')
experiment.head()

# %% [markdown]
# # TEST CLIENTS KPI ANALYSIS

# %%

test_df=experiment[experiment['Variation'] == 'Test']

# %%
test_df.head(10)

# %%
test_df.isna().sum()

# %% [markdown]
# 1. univariate: clients using customer df. Analyze age and other identifiers in clients. build a profile
# 2. test_df proportion of confirm 

# %% [markdown]
# ## Univariate analysis: Client behavior analysis

# %% [markdown]
# Answer the following questions about demographics:
#
# - Who are the primary clients using this online process?
# - Are the primary clients younger or older, new or long-standing?

# %%
client_test = test_df.loc[test_df["Variation"] == "Test"]
client_test.client_id.nunique()

# %%
client_test.describe()

# %%
# gender analysis
gender_freq=client_test.gendr.value_counts()
gender_prop=client_test.gendr.value_counts(normalize=True)

display(gender_freq, gender_prop)

# %%

# %%
# Age analysis: 
mean_age = client_test['clnt_age'].mean()
median_age = client_test['clnt_age'].median()
mode_age = client_test['clnt_age'].mode()[0]
var_age = client_test['clnt_age'].var()
std_age = client_test['clnt_age'].std()
min_age = client_test['clnt_age'].min()
max_age = client_test['clnt_age'].max()
range_age = max_age - min_age
quantiles_age = client_test['clnt_age'].quantile([0.25, 0.5, 0.75])

mean_age, median_age,mode_age, var_age, std_age, range_age, quantiles_age

# %% [markdown]
# The Test group is mainly composed of middle-aged clients. The average and median ages are both around 47, indicating a balanced distribution centered in the late 40s. Although the most common age is 29.5, most clients fall between 33.5 and 59.5 years old, suggesting the primary client profile is not especially young but rather adult to older-middle-aged.

# %%
skewness_age = client_test['clnt_age'].skew()
kurtosis_age = client_test['clnt_age'].kurtosis()

skewness_age, kurtosis_age

# %% [markdown]
# The Test group’s age distribution is approximately symmetric, with only a very slight skew toward older clients. The negative kurtosis suggests that ages are relatively spread out across the sample, rather than heavily concentrated around one specific age. This supports the idea that the Test group is broadly middle-aged, with a wide age range.

# %%
fig, axes = plt.subplots()
sns.histplot(client_test['clnt_age'], kde=True, bins=30, color="blue", ax=axes);
plt.show()

# %%
sns.boxplot(x = client_test['clnt_age'], color="lightblue");

# %% [markdown]
# This visualization confirms that there are indeed no outliers in the age. 

# %%
# new or long standing clients: 
mean_seniority = client_test['clnt_tenure_mnth'].mean()
median_seniority = client_test['clnt_tenure_mnth'].median()
mode_seniority = client_test['clnt_tenure_mnth'].mode()[0]
var_seniority = client_test['clnt_tenure_mnth'].var()
std_seniority = client_test['clnt_tenure_mnth'].std()
min_seniority = client_test['clnt_tenure_mnth'].min()
max_seniority = client_test['clnt_tenure_mnth'].max()
range_seniority = max_seniority - min_seniority
quantiles_seniority = client_test['clnt_tenure_mnth'].quantile([0.25, 0.5, 0.75])

mean_seniority, median_seniority,mode_seniority, var_seniority, std_seniority, range_seniority, quantiles_seniority

# %% [markdown]
# The Test group is mainly composed of long-standing clients. The average tenure is around 150 months, or 12.5 years, and the median is around 134 months, or 11.2 years. Since 75% of clients have been with the company for up to nearly 16 years, and even the first quartile is close to 7 years, this group appears to be mostly established rather than new customers.

# %%
skewness_seniority = client_test['clnt_tenure_mnth'].skew()
kurtosis_seniority = client_test['clnt_tenure_mnth'].kurtosis()

skewness_seniority, kurtosis_seniority

# %% [markdown]
# A positive skew above 1 means there are some clients with very long tenure pulling the average upward. That explains why the mean tenure, about 150 months, is higher than the median, 134 months.
# Positive kurtosis means the distribution has more extreme values than a normal distribution. In this case, there are some unusually long-standing clients.

# %%
fig, axes = plt.subplots()
sns.histplot(client_test['clnt_tenure_mnth'], kde=True, bins=30, color="blue", ax=axes);
plt.show()

# %% [markdown]
# The histogram shows a right-skewed, with three visible peaks around 75, 175, and 260 months. This suggests the client base isn't uniform there are distinct "waves" of clients who joined at different periods.

# %%
sns.boxplot(x = client_test['clnt_tenure_mnth'], color="lightblue");

# %% [markdown]
# The boxplot makes it clear there's a long right tail with many outliers beyond 350 months, going up to 670 months (56 years). These are very long-standing clients but relatively few in number.

# %% [markdown]
# **New vs. Long-standing?**
# These are predominantly long-standing clients. A seniority of 134 months median means the typical client has been with Vanguard for nearly a decade. Very few clients are new, the left tail starts around 50–60 months (4-5 years minimum in the test group).

# %% [markdown]
# ## 1. COMPLETION RATE: The proportion of users who reach the final 'confirm' step.

# %%
test_df.columns=[str(col).lower()for col in test_df.columns]
test_df.columns

# %%
test_df.to_csv('../data/test_clients.csv')

# %%
test_df.process_step.value_counts()

# %%
# This is showing the percentage out of the total number of transactions how many were 'confirm' but this doesn't equate the proportion
# of clients who reached this step as there are more steps done than unique client_ids' (clients do more than one step).
test_df.process_step.value_counts(normalize=True)

# %% [markdown]
# ### 1.1. Completion rate by client_id

# %%
test_df.shape

# %%
# Number of clients who participated in the test meassured through unique client_id:
total_clients=test_df.client_id.nunique()
total_clients

# %%
# Number of clients who reached 'confirm' through unique client id:
completed_clients=test_df.loc[test_df['process_step'] == 'confirm','client_id'].nunique()
completed_clients

# %%
#  Proportion of clients who reach the final 'confirm' step.
completion_rate= completed_clients/total_clients
print(f'The percentage of clients in the test that completed the process was: {round(completion_rate*100,2)}% .')

# %%
# Has any client completed the process more than once, so they have 'confirm' twice??
confirm_counts = (test_df[test_df['process_step'] == 'confirm'].groupby('client_id').size().sort_values(ascending=False))

confirm_counts.head(10)

# %%
# Number of clients who completed the process more than once:
multiple_clients=(confirm_counts > 1).sum()
multiple_clients

# %%
# proportion of clients who comleted the process more than once:
multiple_compl_rate= multiple_clients/total_clients
print(f'The percentage of clients who finished the process more than once was: {round(multiple_compl_rate*100,2)}% .')

# %% [markdown]
# ### 1.2. Completion rate by visit_id

# %%
# Number of users who participated in the test meassured through unique visit_id:
total_users=test_df.visit_id.nunique()
total_users

# %%
# Number of users who reached 'confirm' through unique visit_id:
completed_users=test_df.loc[test_df['process_step'] == 'confirm','visit_id'].nunique()
completed_users

# %%
#  Proportion of users who reach the final 'confirm' step.
completion_rate_user= completed_users/total_users
print(f'The percentage of users in the test that completed the process was: {round(completion_rate_user*100,2)}% .')

# %%
# Has any user completed the process more than once, so they have 'confirm' twice??
confirm_counts_user = (test_df[test_df['process_step'] == 'confirm'].groupby('visit_id').size().sort_values(ascending=False))

confirm_counts_user.head(10)

# %%
# Number of users who completed the process more than once:
multiple_users=(confirm_counts_user > 1).sum()
multiple_users

# %%
# proportion of users who comleted the process more than once:
users_multicompl_rate= multiple_users/total_users
print(f'The percentage of users who finished the process more than once was: {round(users_multicompl_rate*100,2)}% .')

# %% [markdown]
# ## 2. Errors:  users go back to a previous step

# %%
test_df.dtypes

# %%
test_df.date_time=pd.to_datetime(test_df['date_time'])
test_df.date_time

# %%
test_date=test_df.date_time.loc[0]-test_df.date_time.loc[1]
test_date

# %%
test_df.process_step.value_counts()

# %%
# Convert categorical values to numerical in 'process_step' column:
steps_map={'start':0, 'step_1':1, 'step_2':2, 'step_3':3, 'confirm':4}

test_df['step_num']= test_df['process_step'].map(steps_map)

test_df.step_num.value_counts()

# %%
test_df.head()

# %%
# keep only relevant column for checking error and sort by visit and date so the steps are supposed to be sequential:
test_error= test_df[['visit_id', 'process_step','step_num','date_time']]
test_error=test_error.sort_values(['visit_id', 'date_time'], ascending=True)
test_error.head(20)
test_error.info()


# %%
# function to identify errors:

def bool_error(series):
    return (series.diff() <= 0) #only < if we don't consider repeating a step an error, <= if repeating a step means there's an error


# %%
# new column with errors in boolean form:
test_error["error"] = test_error.groupby("visit_id")["step_num"].transform(bool_error)
test_error.head(20)
test_error.info()

# %%
test_error['error']=test_error.error.astype(int)
test_error.head(20)
test_error['date_time'].isna().sum()

# %%
n_test_error=test_error.error.sum()
n_test_error

# %%
pct_error_test=n_test_error/len(test_error)
print(f'The percentage of actions in the process that were errors was: {round(pct_error_test*100,2)}% . ')

# %% [markdown]
# ## 3. Duration: average time users take to finish a step
test_error['date_time'] = pd.to_datetime(
    test_error['date_time']
)

# %%
test_error['duration']=test_error.groupby("visit_id").date_time.diff()
test_error['duration_sec'] = test_error['duration'].dt.total_seconds()

test_error.head(20)

# %%
(len(test_error) - test_error['visit_id'].nunique()) == test_error['duration_sec'].count()
print(len(test_error))
print(test_error['visit_id'].nunique())
print(test_error['duration_sec'].count())

# %%
test_error.info()
test_error[
    test_error.duplicated(
        ['visit_id','date_time'],
        keep=False
    )
].shape

# %%
step_avg=test_error.groupby('step_num').duration_sec.mean()

# %%
step_avg

# %%
step_error=test_error[test_error['error']==0].groupby('step_num').duration.mean()

# %%
step_error

# %% [markdown]
# # CONTROL CLIENTS KPI ANALYSIS 

# %%
control_df=experiment[experiment['Variation'] == 'Control']
control_df.head()

# %%
control_df.shape

# %%
control_df.isna().sum()

# %%
control_df.duplicated().sum()

# %% [markdown]
# ## 1. Completion rate

# %% [markdown]
# ### 1.1.Completion rate by client_id

# %%
total_cclients=control_df.client_id.nunique()
total_cclients

# %%
# Number of clients who reached 'confirm' through unique client id:
completed_cclients=control_df.loc[control_df['process_step'] == 'confirm','client_id'].nunique()
completed_cclients

# %%
#  Proportion of clients who reach the final 'confirm' step.
ccompletion_rate= completed_cclients/total_cclients
print(f'The percentage of clients in the control that completed the process was: {round(ccompletion_rate*100,2)}% .')

# %% [markdown]
# ### 1.2. Completion rate by visit_id

# %%
# Number of users who participated in the test meassured through unique visit_id:
total_cusers=control_df.visit_id.nunique()
total_cusers

# %%
# Number of users who reached 'confirm' through unique visit_id:
completed_cusers=test_df.loc[test_df['process_step'] == 'confirm','visit_id'].nunique()
completed_cusers

# %%
#  Proportion of users who reach the final 'confirm' step.
completion_rate_cuser= completed_cusers/total_cusers
print(f'The percentage of users in the control that completed the process was: {round(completion_rate_cuser*100,2)}% .')

# %% [markdown]
# ## 2. Errors:  users go back to a previous step

# %%
control_df.date_time=pd.to_datetime(control_df['date_time'])
control_df.date_time

# %%
control_df.process_step.value_counts()

# %%
# Convert categorical values to numerical in 'process_step' column:
steps_map={'start':0, 'step_1':1, 'step_2':2, 'step_3':3, 'confirm':4}

control_df['step_num']= control_df['process_step'].map(steps_map)

control_df.step_num.value_counts()

# %%
# keep only relevant column for checking error and sort by visit and date so the steps are supposed to be sequential:
control_error=control_df[['visit_id', 'process_step','step_num','date_time']]
control_error=control_error.sort_values(['visit_id', 'date_time'], ascending=True)
control_error.head(20)


# %%
# function to identify errors:

def bool_error(series):
    return (series.diff() <= 0) #only < if we don't consider repeating a step an error, <= if repeating a step means there's an error


# %%
# new column with errors in boolean form:
control_error["error"] = control_error.groupby("visit_id")["step_num"].transform(bool_error)
control_error.head(20)

# %%
control_error["error"]=control_error.error.astype(int)
control_error.head(20)

# %%
n_control_errors= control_error.error.sum()
n_control_errors

# %%
pct_error=n_control_errors/len(control_error)
print(f'The percentage of actions in the process that were errors was: {round(pct_error*100,2)}% . ')

# %%
# Counting how many visits had errors:
total_visits_control=control_error.visit_id.nunique
print(total_visits_control)
visits_with_erors= 

# %% [markdown]
# ## 3. Duration

# %%
control_error['duration']=control_error.groupby("visit_id").date_time.diff()
control_error.head(20)

# %%
control_avg=control_error.groupby('step_num').duration.mean()
control_avg

# %%
control_noerror_avg=control_error[control_error['error']==0].groupby('step_num').duration.mean()
control_noerror_avg

# %% [markdown]
# # COMPARISON: test group vs control group

# %%
# Completion rate (out of client id or visit id):
print(f'The completion rate for clients in the TEST group: {round(completion_rate*100,2)}% .')
print(f'The completion rate for clients in the CONTROL group: {round(ccompletion_rate*100,2)}% .')

# %%
# Error rate (out of all transactions or visits?): 
print(f'The error rate per action in the website for the TEST group: {round(pct_error_test*100,2)}% . ')
print(f'The error rate per action in the website for the CONTROL group: {round(pct_error*100,2)}% . ')

# %%

# %%

# %%
