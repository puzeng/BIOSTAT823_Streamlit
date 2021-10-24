import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.title("""
Visualization Dashborad:\n 
Is there a life after graduate school?\n
Data Visualizations based on National Science Foundation of Science and Engineering Doctorates[1].
""")

st.subheader("""
Sex vs Major Field of Study
""")
sex_field_study = pd.read_csv('sex_field_study_phd.csv')
#sex_field_study = sex_field_study.melt(id_vars = ['Major field of study', 'Sex'], 
                                        #var_name = 'Year', 
                                        #value_name = 'Number of ppl')
st.text("""
We first look into the gender distribution for each type of the major field of study
in the degree of doctorates.\n
The table below showed the number of PhD candidates in each major feild of study
stratified by genders from year 2008 to 2017.
""")
st.table(sex_field_study.head())

st.text("""
In this section, we are going to take a look of how the number of PhD candidates 
is ditributed from year 2008 to 2017.

By default, we will select the Life sciences and you are free to unselect this study.
""")
#Drop column represents the change % between 2008 to 2017
remained_cols = list(range(len(sex_field_study.columns) - 2)) + [len(sex_field_study.columns)-1]
sex_field_study = sex_field_study.iloc[:, remained_cols]


selected_study = st.multiselect(
    "Select the major field(s) of study",
    sex_field_study['Major field of study'].unique().tolist(),
    default = 'Life sciences'
)

sex_combined = sex_field_study.melt(id_vars = ['Major field of study', 'Sex'],
                                    var_name = 'Year', 
                                    value_name = 'Number of ppl')

#convert from object dtype to int64 dtype for column, number of ppl

sex_combined['Number of ppl'] = sex_combined['Number of ppl'].str.replace(',', '')
sex_combined = sex_combined.dropna()

sex_combined['Number of ppl'] = sex_combined['Number of ppl'].astype(int)

sex_all = sex_combined[sex_combined.Sex == 'All']
female = sex_combined[sex_combined.Sex == 'Female']
male = sex_combined[sex_combined.Sex == 'Male']

if st.button("Click me if you want to see data distrubution for all gender."):
    plot_df = sex_all[sex_combined['Major field of study'].isin(selected_study)]


    fig = px.bar(
        plot_df, 
        x = 'Year', 
        y = 'Number of ppl',
        color = 'Major field of study',
        barmode = 'group'
    )

    fig.update_layout(
        showlegend = True, 
        title = "Number of people in the major field of study from year 2008 tp 2017",
        title_x = 0.5,
        xaxis_title = 'Number of people',
        yaxis_title = 'Year'
    )

    st.plotly_chart(fig)

if st.button("Click me if you want to see data distrubution for males."):
    plot_df = male[sex_combined['Major field of study'].isin(selected_study)]


    fig = px.bar(
        plot_df, 
        x = 'Year', 
        y = 'Number of ppl',
        color = 'Major field of study',
        barmode = 'group'
    )

    fig.update_layout(
        showlegend = True, 
        title = "Number of males in the major field of study from year 2008 tp 2017",
        title_x = 0.5,
        xaxis_title = 'Number of people',
        yaxis_title = 'Year'
    )

    st.plotly_chart(fig)

if st.button("Click me if you want to see data distrubution for female."):
    plot_df = female[sex_combined['Major field of study'].isin(selected_study)]


    fig = px.bar(
        plot_df, 
        x = 'Year', 
        y = 'Number of ppl',
        color = 'Major field of study',
        barmode = 'group'
    )

    fig.update_layout(
        showlegend = True, 
        title = "Number of females in the major field of study from year 2008 tp 2017",
        title_x = 0.5,
        xaxis_title = 'Number of people',
        yaxis_title = 'Year'
    )

    st.plotly_chart(fig)

st.text("""
Then, we would like to perform the comparison of number of people in some certain fields by gender.
""")

selected_df = sex_combined[sex_combined['Major field of study'].isin(selected_study)]
sex_combined_fig = px.bar(
        selected_df[selected_df.Year == '2017'], 
        x = 'Sex', 
        y = 'Number of ppl',
        color = 'Major field of study',
        barmode = 'group'
    )

sex_combined_fig.update_layout(
        showlegend = True, 
        title = """
        Comparison between males and females in year 2017
        """,
        title_x = 0.5,
        xaxis_title = 'Gender',
        yaxis_title = 'Number of people'
    )

st.plotly_chart(sex_combined_fig)


st.subheader("""
Race vs Major Field of Study vs Employment Types vs Debt Level
""")

st.text("""In this section, we want to focus on the relationship between
the race distribution in variables, major field of study, employment types, and the debt level.
We will fistly look at the race vs major field of study.
""")

race_df = pd.read_csv('race_phd_info.csv', low_memory = False)
race_df['Number of count'] = pd.to_numeric(race_df['Number of count'], errors='coerce')
race_df['value'] = pd.to_numeric(race_df['value'], errors='coerce')
race_df['Count'] = pd.to_numeric(race_df['Count'], errors='coerce')
race_df = race_df.dropna().reset_index(drop = True)

#since the dataset is too large (131072 rows × 7 columns), we randomly sample 2000 from it
#race_df = race_df.sample(1000).reset_index(drop = True)
st.dataframe(race_df.head())

st.text("""
Variable explainations:
Number of count: the number of people respect to the race.
value = the number of people respect to the race and employment types.
Count = the number of people raspect to the race and debt level.""")

selected_var = st.selectbox(
        "Select the variables you want to look at against the race info",
        ['Field of study', 'Employment Types', 'Debt level']
)

if selected_var == 'Field of study':
    st.subheader("""
        Race vs Major Field of Study
    """)
    selected_study_race = st.multiselect(
        "Select the major you want to see",
        race_df['Field of study'].unique().tolist(),
        default = 'All fields'
    )
    study_df = race_df.iloc[:, 0:2]
    study_df = race_df.iloc[:, [0,1,2]]
    study_df = study_df.dropna().drop_duplicates()

    study_df = study_df[study_df['Field of study'].isin(selected_study_race)]

    study_race_fig = px.bar(
        study_df, 
        x = 'Ethnicity status', 
        y = 'Number of count',
        color = 'Field of study',
        barmode = 'group'
    )

    study_race_fig.update_layout(
        showlegend = True, 
        title = """
        Comparison between ethnicity status in major field of study.
        """,
        title_x = 0.5,
        xaxis_title = 'Ethnicity status',
        yaxis_title = 'Number of people'
    )

    st.plotly_chart(study_race_fig)
    st.text(
        """
        *If the figure doesn't show the ethnicity status that you chosen,
        it probabily is because we don't have the related data.
        """
    )

if selected_var == 'Employment Types':

    employment_df = race_df.iloc[:, [1,3,4]]
    employment_df = employment_df.dropna()
    employment_df = employment_df.drop_duplicates().reset_index(drop = True)
    employment_df = employment_df[employment_df['Employment Types'] != 'All U.S. employment commitments (number)']

    st.subheader("""
        Race vs Employment Types
    """)
    selected_study_race = st.multiselect(
        "Please select the interested ethnicity status.",
        employment_df['Ethnicity status'].unique().tolist(),
        default = 'Asian' 
    )
    
    selected_employment_df = employment_df[employment_df['Ethnicity status'].isin(selected_study_race)].reset_index(drop = True)


    employment_fig = px.bar(
        selected_employment_df, 
        x = 'Employment Types', 
        y = 'value',
        color = 'Ethnicity status',
        barmode = 'group'
    )

    employment_fig.update_layout(
        showlegend = True, 
        title = """
        Comparison between ethnicity status in employment types.
        """,
        title_x = 0.5,
        xaxis_title = 'Employment Types',
        yaxis_title = 'proportion of people respect to total employment number'
    )

    st.plotly_chart(employment_fig)

    st.text(
        """
        *If the figure doesn't show the ethnicity status that you chosen,
        it probabily is because we don't have the related data.
        """
    )

if selected_var == 'Debt level':
    st.subheader("""
    Race vs Debt Level
    """)
    selected_debt = st.multiselect(
        "Select the debt level you want to see",
        race_df['Debt level'].unique().tolist(),
        default = 'No debt'
    )

    debt_df = race_df.iloc[:, [1,5,6]]
    debt_df = debt_df.dropna().reset_index(drop = True)
    debt_df = debt_df.drop_duplicates()

    debt_df = debt_df[debt_df['Debt level'].isin(selected_debt)]
    
    debt_race_fig = px.bar(
        debt_df, 
        x = 'Ethnicity status', 
        y = 'Count',
        color = 'Debt level',
        barmode = 'group'
    )

    debt_race_fig.update_layout(
        showlegend = True, 
        title = """
        Comparison between ethnicity status in debt level.
        """,
        title_x = 0.5,
        xaxis_title = 'Ethnicity status',
        yaxis_title = 'Number of people'
    )

    st.plotly_chart(debt_race_fig)

    st.text(
        """
        *If the figure doesn't show the ethnicity status that you chosen,
        it probabily is because we don't have the related data.
        """
    )
