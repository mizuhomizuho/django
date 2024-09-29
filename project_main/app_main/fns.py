
def print_to_string(*args, **kwargs):
    import io
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

def sql_pretty():
    import sqlparse
    from django.db import connection
    out = ''
    for item in connection.queries:
        out += ('\n\n' if out != '' else '') + sqlparse.format(item['sql'], reindent=True, keyword_case='upper')
    return out