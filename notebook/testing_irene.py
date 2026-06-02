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
customer_test.loc[customer_test.isna().any(axis=1)]

# %%
experiment=pd.merge(web_df,customer_test, on='client_id', how='left')
experiment.head()

# %%

test_df=experiment[experiment['Variation'] == 'Test']

# %%
test_df.head()

# %%
test_df.process_step.value_counts()

# %%
test_df.process_step.value_counts(normalize=True)

# %% [markdown]
# 1. univariate: clients using customer df. Analyze age and other identifiers in clients. build a profile
# 2. test_df proportion of confirm 

# %%
test_df['duration']= 
