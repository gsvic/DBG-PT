import streamlit as st

from dbgpt.utils import get_dbms_driver
from dbgpt.ui.prompts import prompt
from dbgpt.ui.display import split_commands, render_analysis_results


st.markdown("# Regression Debugger")
st.markdown("### Analyze and improve query regressions using Large Language Models (LLMs). ")

with st.sidebar:
    st.title('DBG-PT')
    st.write('LLM-Assisted Query Regression Debugger')

    st.subheader('Database Systems')
    selected_dbms = st.sidebar.selectbox('Choose a Database System', ['Postgres'], key='selected_dbms')
    db_name = st.sidebar.text_input('Database Name', value='tpch', key='db_name')

st.markdown(
        """
        <style>
            .reportview-container .main .block-container{
                max-width: 90%;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Fast Plan")
    st.markdown(f"#### Provide the fast query plan")
    plan_1 = st.text_area(label="plan1")

with col2:
    st.markdown("### Slow Plan")
    st.markdown(f"#### Provide the slow query plan")
    plan_2 = st.text_area(label="plan2")


analyze_button = st.button("Analyze")

if analyze_button:
    st.markdown("### Explanation")

    with st.status("Sending plans to the LLM") as status:
        try:
            data = prompt(plan_1, plan_2, selected_dbms, fake_it=False, temperature=0)

            status.update(
                label="Success!", state="complete", expanded=False
            )

            plan_diff = data['plan_diff']
            reasoning = data['reasoning']
            commands = data['commands']

        except Exception as e:
            status.update(label="Failed: {}".format(str(e)), state="error", expanded=False)
            plan_diff = None
            reasoning = None
            commands = list()

    system_commands, index_commands = split_commands(commands)

    render_analysis_results(plan_diff, reasoning, system_commands, index_commands)

    st.session_state["analyzed"] = True
    st.session_state["system_commands"] = system_commands
    st.session_state["index_commands"] = index_commands

if st.session_state.get("analyzed"):
    indexes = st.session_state["index_commands"]

    # Check if there are recommended index commands; If so, create the corresponding button
    if indexes:
        create_indexes = st.button("Create Indexes", help="Create the suggested indexes")

        if create_indexes:
            cursor = get_dbms_driver(selected_dbms.upper(), db=db_name).cursor

            with st.status("Creating indexes...") as status:
                for c in indexes:
                    try:
                        st.write("Executing index command: " + c)
                        cursor.execute(c)
                    except Exception as e:
                        st.error(e)

                status.update(
                    label="Indexes created successfully!", state="complete", expanded=False
                )
