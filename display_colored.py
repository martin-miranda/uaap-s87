import streamlit as st
import pandas as pd
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.display.float_format = "{:,.2f}".format

# Column Lists
with open('player_base_cols.txt', 'r') as file:
    pb_cols = [line.strip() for line in file]
with open('player_advanced_cols.txt', 'r') as file:
    pa_cols = [line.strip() for line in file]
with open('team_base_cols.txt', 'r') as file:
    tb_cols = [line.strip() for line in file]
with open('team_advanced_cols.txt', 'r') as file:
    ta_cols = [line.strip() for line in file]

teams={}
with open('team_colors.txt','r') as file:
    for line in file:
        line = line.rstrip('\n')
        if ':' in line:
            team, color = line.split(':',1)
            teams[team] = color

with open('title.txt', 'r') as file:
    title = [line.strip() for line in file]
st.title(title[0])
st.markdown('By Martin Miranda @mc_miranda34')
st.markdown('Raw Box Scores from Pong Ducanes: uaap.livestats.ph')
st.markdown('#### As of Game 34 - DLSU vs. UST')

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Player Per-Game Stats', 'Player Per-30 Stats', 'Player Advanced Stats', 'Team Per-Game Stats', 'Team Advanced Stats', 'Glossary'])
cm = sns.dark_palette("green", as_cmap=True)

with tab1:
    st.header('All Players', divider='gray')
    df = pd.read_csv('player_per_game.csv', index_col=['PLAYER','TEAM'])
    df = df[(df['MINS'] * df['GP']) >= df['GP'].max() * 8]
    df = df.reindex(columns=pb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider=color)
        df = pd.read_csv('./player_stats/{0}_per_game.csv'.format(team), index_col=['PLAYER', 'TEAM'])
        df = df.reindex(columns=pb_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).format("{:.2f}")
        st.write(df)

with tab2:
    st.header('All Players', divider='gray')
    df = pd.read_csv('player_per_30.csv', index_col=['PLAYER', 'TEAM'])
    df = df[(df['MINS'] * df['GP']) >= df['GP'].max() * 8]
    df = df.reindex(columns=pb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider=color)
        df = pd.read_csv('./player_stats/{0}_per_30.csv'.format(team), index_col=['PLAYER', 'TEAM'])
        df = df.reindex(columns=pb_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).format("{:.2f}")
        st.write(df)

with tab3:
    st.markdown('*Please note the discrepancies on the SP calculation at the bottom of the page.*')
    st.header('All Players', divider='gray')
    df = pd.read_csv('advanced_stats.csv', index_col=['PLAYER','TEAM'])
    df = df[(df['MPG'] * df['GP']) >= df['GP'].max() * 8]
    df = df.reindex(columns=pa_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider=color)
        df = pd.read_csv('./player_stats/{0}_advanced.csv'.format(team), index_col=['PLAYER', 'TEAM'])
        df = df.reindex(columns=pa_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).format("{:.2f}")
        st.write(df)

    st.write('---')
    st.markdown('There are slight discrepancies on the official SP calculations due to the bonus and penalties in the formula. This would not probably affect **rankings** unless adjacent players have very close SP.')
    st.markdown('The discrepancies are as follows:')
    st.markdown('1. Win bonuses are counted by team instead of by player for simplicity in coding. *For example, the missed win by JD Cagulangan is still included in his bonus.*')
    st.markdown('2. Penalties are not included at all due to lack of availability on technical and unsportsmanlike foul data.')

with tab4:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('team_per_game.csv', index_col=['TEAM'])
    df['W%'] = df['W'] / df['GP']
    df = df.reindex(columns=tb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).format("{:.2f}")
    st.write(df)

with tab5:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('team_advanced.csv', index_col=['TEAM'])
    df = df.reindex(columns=ta_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).format("{:.2f}")
    st.write(df)

with tab6:
    with open('Glossary.md','r') as f:
        markdown_content = f.read()
        st.markdown(markdown_content)
