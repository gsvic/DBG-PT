from pkg_resources import resource_listdir, resource_filename


def get_tpch_queries():
    query_files = resource_listdir("dbgpt.benchmarks", "resources/queries/tpch")

    queries = [(d.replace(".sql", ""), open(resource_filename("dbgpt.benchmarks", f"resources/queries/tpch/{d}")).read()) for d in query_files]
    queries = sorted(queries, key=lambda k: k[0])

    return queries
