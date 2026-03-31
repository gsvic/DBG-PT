import streamlit as st


def split_commands(commands):
    system_commands = []
    index_commands = []
    for cmd in commands:
        if "CREATE INDEX" not in cmd.upper() and "statement_timeout" not in cmd:
            system_commands.append(cmd)
        else:
            index_commands.append(cmd)
    return system_commands, index_commands


def render_analysis_results(plan_diff, reasoning, system_commands, index_commands):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    st.markdown("""
            <style>
                .stBlock > div:first-child > div {
                    border-right: 2px solid #000;
                }
            </style>
            """, unsafe_allow_html=True)

    with col1:
        st.markdown("#### <u>Plan Differences</u>", unsafe_allow_html=True)
        st.write(plan_diff)
    with col2:
        st.markdown("#### <u>Reasoning</u>", unsafe_allow_html=True)
        st.write(reasoning)
    with col3:
        st.markdown("#### <u>Recommended Configuration</u>", unsafe_allow_html=True)
        st.write(system_commands)
    with col4:
        st.markdown("#### <u>Recommended Indexes</u>", unsafe_allow_html=True)
        st.write(index_commands)
