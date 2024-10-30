import streamlit as st
import pandas as pd
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
pd.options.display.float_format = "{:,.2f}".format

ts = pd.read_json('team_aggregate.json',orient='index')
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

st.set_page_config(
    page_title='{0}'.format(title[0]),
    page_icon=':basketball:',
    layout='wide'
)

st.title(title[0])
carl = "https://twitter.com/mc_miranda34"
pong = "https://twitter.com/ompongski"
st.link_button(label='By Carl Miranda (@mc_miranda34)', url=carl, type='primary', icon=':material/person:')
st.link_button(label='Raw Box Scores from Pong Ducanes (@ompongski)', url=pong, type='primary', icon=':material/insert_chart:')
with open('as_of.md','r') as f:
    markdown_content = f.read()
    st.markdown(markdown_content)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['Player Per-Game Stats', 'Player Per-30 Minute Stats', 'Player Advanced Stats', 'Player Comparison', 'Team Per-Game Stats', 'Opponent Per-Game Stats', 'Team Advanced Stats', 'Glossary'])
cm = sns.dark_palette("green", as_cmap=True)
r_cm = sns.dark_palette("green", as_cmap=True, reverse=True)

with tab1:
    st.header('All Players', divider='gray')
    df = pd.read_csv('player_per_game.csv', index_col=['PLAYER','TEAM'])
    ts_merge = df.merge(ts, left_on='TEAM', right_index=True, suffixes=['_P','_T'])
    df['QMINS'] = ts_merge['GP_T'] * 8
    df = df[(df['MINS'] * df['GP']) >= df['QMINS']]
    df = df.drop(labels='QMINS', axis=1)
    df = df.reindex(columns=pb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider='grey')
        df = pd.read_csv('./player_stats/{0}_per_game.csv'.format(team), index_col=['PLAYER', 'TEAM'])
        df = df.reindex(columns=pb_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        r_tcm = sns.dark_palette(color, as_cmap=True, reverse=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).background_gradient(cmap=r_tcm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(df)

with tab2:
    st.header('All Players', divider='gray')
    df = pd.read_csv('player_per_30.csv', index_col=['PLAYER', 'TEAM'])
    ts_merge = df.merge(ts, left_on='TEAM', right_index=True, suffixes=['_P','_T'])
    df['QMINS'] = ts_merge['GP_T'] * 8
    df = df[(df['MINS'] * df['GP']) >= df['QMINS']]
    df = df.drop(labels='QMINS', axis=1)
    df = df.reindex(columns=pb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider='gray')
        df = pd.read_csv('./player_stats/{0}_per_30.csv'.format(team), index_col=['PLAYER', 'TEAM'])
        df = df.reindex(columns=pb_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        r_tcm = sns.dark_palette(color, as_cmap=True, reverse=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).background_gradient(cmap=r_tcm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(df)

with tab3:
    st.markdown('*Note for SP: Penalties are not included due to inavailability of data.*')
    st.markdown('*Note for WS: Values are re-normalized every after game. This should not affect rankings.*')
    st.header('All Players', divider='gray')
    df = pd.read_csv('advanced_stats.csv', index_col=['PLAYER','TEAM'])
    ts_merge = df.merge(ts, left_on='TEAM', right_index=True, suffixes=['_P','_T'])
    df['QMINS'] = ts_merge['GP_T'] * 8
    df = df[(df['MPG'] * df['GP']) >= df['QMINS']]
    df = df.drop(labels='QMINS', axis=1)
    df = df.reindex(columns=pa_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TOR','DRtg']).format("{:.2f}")
    st.write(df)
    st.markdown('*Note: Only qualified players are displayed, which requires an average of at least 8 MPG in all team games played.*')

    for team, color in teams.items():
        st.header('{0}'.format(team), divider='gray')
        df = pd.read_csv('./player_stats/{0}_advanced.csv'.format(team), index_col=['PLAYER', 'TEAM'])
        df = df.reindex(columns=pa_cols)
        tcm = sns.dark_palette(color, as_cmap=True)
        r_tcm = sns.dark_palette(color, as_cmap=True, reverse=True)
        df = df.style.background_gradient(cmap=tcm, axis=0).background_gradient(cmap=r_tcm, axis=0, subset=['TOR','DRtg']).format("{:.2f}")
        st.write(df)

with tab4:
    st.header('Player Comparison', divider='gray')
    st.markdown('Use this tab to compare two or more players more easily. You may search for your chosen players by typing their last name or team below.')
    st.markdown('*This page uses the same data as in other tabs. Refer to notes in other tabs if necessary.*')
    df1 = pd.read_csv('player_per_game.csv', index_col=['PLAYER','TEAM'])
    df2 = pd.read_csv('player_per_30.csv', index_col=['PLAYER','TEAM'])
    df3 = pd.read_csv('advanced_stats.csv', index_col=['PLAYER','TEAM'])

    row_indices = st.multiselect(
        "Select Players:",
        options=df3.index.tolist(),
        default=[]
    )

    if row_indices:
        st.header("Player Per-Game Stats")
        frozen_df1 = df1.loc[row_indices]
        frozen_df1 = frozen_df1.reindex(columns=pb_cols)
        frozen_df1 = frozen_df1.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(frozen_df1)
        st.header("Player Per-30 Stats")
        frozen_df2 = df2.loc[row_indices]
        frozen_df2 = frozen_df2.reindex(columns=pb_cols)
        frozen_df2 = frozen_df2.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TO','PF']).format("{:.2f}")
        st.write(frozen_df2)
        st.header("Player Advanced Stats")
        frozen_df3 = df3.loc[row_indices]
        frozen_df3 = frozen_df3.reindex(columns=pa_cols)
        frozen_df3 = frozen_df3.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['TOR','DRtg']).format("{:.2f}")
        st.write(frozen_df3)


with tab5:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('team_per_game.csv', index_col=['TEAM'])
    df = df.reindex(columns=tb_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['L','TO','PF']).format("{:.2f}")
    st.write(df)

with tab6:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('opp_per_game.csv', index_col=['TEAM'])
    df = df.reindex(columns=tb_cols)
    df = df.drop(labels=['W','L','W%','MINS'], axis=1)
    df = df.style.background_gradient(cmap=r_cm, axis=0).background_gradient(cmap=cm, axis=0, subset=['TO','PF']).format("{:.2f}")
    st.write(df)

with tab7:
    st.header('All Teams', divider='gray')
    df = pd.read_csv('team_advanced.csv', index_col=['TEAM'])
    df = df.reindex(columns=ta_cols)
    df = df.style.background_gradient(cmap=cm, axis=0).background_gradient(cmap=r_cm, axis=0, subset=['DEF','TO','HHI','Py-L']).format("{:.2f}")
    st.write(df)

with tab8:
    with open('Glossary.md','r') as f:
        markdown_content = f.read()
        st.markdown(markdown_content)
