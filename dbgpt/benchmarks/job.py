from pkg_resources import resource_listdir, resource_filename


def get_job_queries():
    query_files = resource_listdir("dbgpt.benchmarks", "resources/queries/job")
    query_files = sorted(query_files, key=lambda x: (int(x.split(".sql")[0][:-1]), x.split(".sql")[0][-1]))

    queries = []
    for f in query_files:
        with open(resource_filename("dbgpt.benchmarks", f"resources/queries/job/{f}")) as fh:
            queries.append((f.split(".sql")[0], fh.read()))

    return queries
