import json

from dbgpt.llm import get_response


def add_line_ids_in_plan(plan: str):
    lines = plan.split("\n")
    lines = [f"{i+1}: {line}" for i, line in enumerate(lines)]
    return "\n".join(lines)


def prompt(plan_1: str, plan_2: str, system: str, temperature: float = 0.35, fake_it: bool = False):
    plan_1 = add_line_ids_in_plan(plan_1)
    plan_2 = add_line_ids_in_plan(plan_2)

    text = ("These are two plans for the same query."
            "Plan 1: \n"
            f"{plan_1}\n"
            "Plan 2: \n"
            f"{plan_2}\n"
            "Plan 1 is faster than Plan 2."
            f"The database system is {system}."
            f"Suggest configuration changes to speed up Plan 2, or, revert it to Plan 1 if possible."
            f"If both plans are the same, try to improve the performance further."
            f"Your response should strictly consist of a list of SQL commands compatible with {system}, and no additional text."
            "Your response should strictly follow the following JSON schema:\n"
            "{plan_diff: explain the plan differences, "
            "diff_map: [list of differences. each line in the provided plans has a unique id. map the differences of the two plans using the line ids],"
            "reasoning: explain your reasoning about the recommened parameters,"
            "commands: [list of SQL commands]}"
            )

    if fake_it:
        return {
            "plan_diff": "The main difference between the two plans is the use of Nested Loop in Plan 1 and Hash Join in Plan 2. Nested Loop is generally faster for smaller data sets, while Hash Join can be more efficient for larger data sets. In Plan 1, the system uses an Index Scan on 'lineitem' table which is faster than the Sequential Scan used in Plan 2. However, Plan 2 tries to parallelize the Sequential Scan on 'part' table to speed up the process.",
            "reasoning": "To speed up Plan 2, we can try to increase the cost limit for using a Sequential Scan, which might make the planner choose an Index Scan instead. Also, increasing the work_mem might make the Hash Join more efficient. If these changes don't improve the performance significantly, we can consider reverting to Plan 1 by decreasing the enable_hashjoin parameter.",
            "commands": [
            "SET seq_page_cost = 10;",
            "SET random_page_cost = 4;",
            "SET cpu_tuple_cost = 0.01;",
            "SET cpu_index_tuple_cost = 0.005;",
            "SET cpu_operator_cost = 0.0025;",
            "SET work_mem = '2GB';",
            "SET enable_hashjoin = off;"
            ]
            }

    data = get_response(text, temperature)

    return json.loads(data.choices[0].message.content)

def prompt_single_plan(plan_1: str, system: str, temperature: float = 0):
    plan_1 = add_line_ids_in_plan(plan_1)

    text = ("The following plan is very slow:"
            f"{plan_1}\n"
            f"The database system is {system}."
            f"Suggest configuration changes (including index recommendations for all seq scans) to speed it up. "
            f"Your response should strictly consist of a list of SQL commands compatible with {system}, and no additional text."
            "Your response should strictly follow the following JSON schema:\n"
            "{plan_diff: explain the possible issues, "
            "reasoning: explain your reasoning about the recommened parameters,"
            "commands: [list of SQL commands]}"
            )

    data = get_response(text, temperature)

    return json.loads(data.choices[0].message.content)
