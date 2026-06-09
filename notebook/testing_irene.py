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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest
import plotly.express as px

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
test_error= test_df[['client_id', 'visit_id', 'process_step','step_num','date_time']]
test_error=test_error.sort_values(['client_id','visit_id', 'date_time'], ascending=True)
test_error.head(20)
test_error.info()

# %%
# Visit ids suspected to not be unique, there could be a visit id asigned to more than one client:
visit_client_check = (test_df.groupby('visit_id')['client_id'].nunique().reset_index(name='n_clients'))

problem_visits = visit_client_check[visit_client_check['n_clients'] > 1]

problem_visits

# %%
# Checking to see examples of repeated visit ids for different clients:
error_rows = test_df[test_df['visit_id'].isin(problem_visits['visit_id'])]

error_rows = error_rows[['client_id', 'visit_id', 'process_step', 'step_num', 'date_time']].sort_values(['visit_id', 'client_id', 'date_time'])

error_rows.head(40)


# %%
# Create a function to identify the errors (we consider an error everytime the succesion of the client isn't from one step to the next):

def bool_error(series):
    return (series.diff() <= 0) # <= because repeating a step means there's an error


# %%
# Create new column with the errors in boolean form by using the previously defined function:
test_error['error'] = test_error.groupby(['client_id','visit_id'])['step_num'].transform(bool_error)
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
<<<<<<< HEAD
test_error['duration']=test_error.groupby("visit_id").date_time.diff()
test_error['duration_sec'] = test_error['duration'].dt.total_seconds()

=======
test_error['duration']=test_error.groupby(['client_id','visit_id']).date_time.diff()
>>>>>>> main
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
control_error=control_df[['client_id', 'visit_id', 'process_step','step_num','date_time']]
control_error=control_error.sort_values(['client_id','visit_id', 'date_time'], ascending=True)
control_error.head(20)

# %%
# Visit ids suspected to not be unique, there could be a visit id asigned to more than one client:
visit_client_ccheck = (control_error.groupby('visit_id')['client_id'].nunique().reset_index(name='n_clients'))

problem_visits_control = visit_client_ccheck[visit_client_ccheck['n_clients'] > 1]
display(problem_visits_control)
print(len(problem_visits_control))


# %%
# function to identify errors:

def bool_error(series):
    return (series.diff() <= 0) #only < if we don't consider repeating a step an error, <= if repeating a step means there's an error


# %%
# new column with errors in boolean form:
control_error['error'] = control_error.groupby(['client_id','visit_id'])['step_num'].transform(bool_error)
control_error.head(20)

# %%
control_error['error']=control_error.error.astype(int)
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
#visits_with_erors= 

# %% [markdown]
# ## 3. Duration

# %%
control_error['duration']=control_error.groupby((['client_id','visit_id'])).date_time.diff()
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

# %%
# Error rate (out of all transactions or visits?): 
print(f'The error rate per action in the website for the TEST group: {round(pct_error_test*100,2)}% . ')
print(f'The error rate per action in the website for the CONTROL group: {round(pct_error*100,2)}% . ')

# %% [markdown]
# h0=completion rate test group is 5% > completion rate control group
# h1=completion rate test group is 5% <= completion rate control group

# %% [markdown]
# statistic Z=p1-p2-d/sqrt
# p-value=
# a=0,05 IC=

# %% [markdown]
# hypothesis for completion rate
# hypotheis for mean duration (two samples t-test) 

# %% [markdown]
# # HYPOTHESIS TESTING

# %% [markdown]
# ## 1. Completion rate

# %% [markdown]
# **TEST 1: Difference in the completion rates** 
#
# We want to know whether the **TEST group has a higher completion rate than the CONTROL group**.
#
# We will perform a one tailed Z-test with the rejection area to the left:
#
# - H0: completion rate test group >= completion rate control group
# - H1: completion rate test group < completion rate control group
#
# alpha = 0.05

# %%
# H1: p1 > p2
alpha = 0.05
z_stat_sm, p_value_sm = proportions_ztest(count = [completed_clients, completed_cclients],nobs  = [total_clients, total_cclients]
, alternative='smaller')

print(f'Z-statistic: {z_stat_sm}')
print(f'p-value: {p_value_sm}')


# %% [markdown]
# **Conclusions:**
# After running a one-tailed two-proportion Z-test at α = 0.05:
# - The p-value was above 0.05, so we **accept H₀**:
# - The TEST group has a **statistically significantly higher** completion rate than the CONTROL group.

# %%
def show_statistical_test(statistic: float, alpha: float, n: int, distribution: str=["t-student","normal"], alternative: str=["two-sided","lower","greater"]):

    if distribution not in ["t-student","normal"]:
        raise TypeError("Sorry, only 't-student', and 'normal' distributions are acepted")

    if alternative not in ["two-sided","lower","greater"]:
        raise TypeError("Sorry, only 'two-sided', 'lower', and 'greated' are acepted valued for the alternative")

    if not isinstance(statistic, float):
        raise TypeError("Sorry, the data type for the statistic must be float")

    if not isinstance(alpha, float):
        raise TypeError("Sorry, the data type for alpha must be float")

    if not isinstance(n, int):
        raise TypeError("Sorry, the data type for n must be int")

    x_values = np.linspace(-3, 3)

    if distribution == "t-student":

        y_values = st.t.pdf(x_values, df=n-1)

        if alternative == "two-sided": # Computing the critical values

            lower_critical_value = st.t.ppf(alpha/2, df=n-1)
            upper_critical_value = st.t.ppf(1-(alpha/2), df=n-1)

            x_values1 = np.linspace(-3, lower_critical_value)
            y_values1 = st.t.pdf(x_values1, df=n-1)

            x_values2 = np.linspace(upper_critical_value, 3)
            y_values2 = st.t.pdf(x_values2, df=n-1)

        elif alternative == "lower":

            critical_value = st.t.ppf(alpha, df=n-1)

            x_values1 = np.linspace(-3, critical_value)
            y_values1 = st.t.pdf(x_values1, df=n-1)

        elif alternative == "greater":

            critical_value = st.t.ppf(1-alpha, df=n-1)

            x_values2 = np.linspace(critical_value, 3)
            y_values2 = st.t.pdf(x_values2, df=n-1)

    elif distribution == "normal":

        y_values = st.norm.pdf(x_values)

        if alternative == "two-sided": # Computing the critical values

            lower_critical_value = st.norm.ppf(alpha/2)
            upper_critical_value = st.norm.ppf(1-(alpha/2))

            x_values1 = np.linspace(-3, lower_critical_value)
            y_values1 = st.norm.pdf(x_values1)

            x_values2 = np.linspace(upper_critical_value, 3)
            y_values2 = st.norm.pdf(x_values2)

        elif alternative == "lower":

            critical_value = st.norm.ppf(alpha)

            x_values1 = np.linspace(-3, critical_value)
            y_values1 = st.norm.pdf(x_values1)

        elif alternative == "greater":

            critical_value = st.norm.ppf(1-alpha)

            x_values2 = np.linspace(critical_value, 3)
            y_values2 = st.norm.pdf(x_values2)

    df = pd.DataFrame({"x": x_values, "pdf": y_values})

    title = f"{distribution} Probability Density Function"

    fig = px.line(df, x="x", y="pdf", title=title)

    if alternative == "two-sided":

        fig.add_vline(x=lower_critical_value, line_color="red")
        fig.add_vline(x=upper_critical_value, line_color="red")

        fig.add_annotation(x=lower_critical_value,y=0,text=f"Lower critical value {lower_critical_value: .2f}",xref="x",yref="paper",yanchor="bottom")
        fig.add_annotation(x=upper_critical_value,y=0,text=f"Upper critical value {upper_critical_value: .2f}",xref="x",yref="paper",yanchor="bottom")

        fig.add_scatter(x=x_values1, y=y_values1,fill='tozeroy', mode='none' , fillcolor='red')
        fig.add_scatter(x=x_values2, y=y_values2,fill='tozeroy', mode='none' , fillcolor='red')

    elif alternative == "lower":

        fig.add_vline(x=critical_value, line_color="red")
        fig.add_annotation(x=critical_value,y=0,text=f"Critical value {critical_value: .2f}",xref="x",yref="paper",yanchor="bottom")

        fig.add_scatter(x=x_values1, y=y_values1,fill='tozeroy', mode='none' , fillcolor='red')

    elif alternative == "greater":

        fig.add_vline(x=critical_value, line_color="red")
        fig.add_annotation(x=critical_value,y=0,text=f"Critical value {critical_value: .2f}",xref="x",yref="paper",yanchor="bottom")

        fig.add_scatter(x=x_values2, y=y_values2,fill='tozeroy', mode='none' , fillcolor='red')

    fig.add_vline(x=statistic)
    fig.add_annotation(x=statistic,y=0,text=f"Statistic {statistic: .2f}",xref="x",yref="paper",yanchor="bottom")

    fig.update_layout(title_text=f'{distribution} Probability Density Function', title_x=0.5)

    fig.update_layout(showlegend=False)

    fig.show()


# %%
show_statistical_test(
    statistic=float(z_stat_sm),
    alpha=0.05,
    n=int(total_clients + total_cclients),
    distribution="normal",
    alternative="lower"
)

# %% [markdown]
# **TEST 2: the difference in completion rates is above 0.05**
#
# Now we will be testing whether the observed difference between the completion rates of the control and test group **meets a minimum  threshold** where **∂=0.05**. We are running a one-tailed two-proportion Z-test with the rejection area to the right. 
#
# - H0 = completion rate test group - completion rate control group <= 0.05
# - H1 = completion rate test group - completion rate control group > 0.05
#
# alpha= 0.05
# group_1=test_group
# group_2=control_group
#

# %%
p1=completion_rate_user
p2=completion_rate_cuser
n1=total_clients
n2=total_cclients
p=(completed_clients+completed_cclients)/(n1+n2)
print(p)

# %%
# Calculate the statistic Z manually using formula:
alpha=0.05
delta=0.05
Z=((p1-p2)-delta)/ np.sqrt(p * (1 - p) * ((1 / n1) + (1 / n2)))
print(f'Z={Z}')

# %%
# get the critical value using scipy stats:
df=n1+n2-2
cv=st.t.ppf(alpha,df)
print(f'CV={cv}')


# %%
def h0_test(z,cv):
    if z<cv:
        print('Reject H0')
    else:
        print('Accept H0')



# %%
h0_test(Z,cv)

# %%
show_statistical_test(Z, alpha, df, distribution="normal", alternative="greater")

# %%
