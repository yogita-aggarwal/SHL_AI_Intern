def compare_assessments(results):

    if len(results) < 2:

        return "I couldn't find enough assessments to compare."

    first = results[0]
    second = results[1]

    answer = f"""
Comparison

1. {first['name']}

Type:
{", ".join(first.get("keys", []))}

Description:
{first.get("description","")}


----------------------------

2. {second['name']}

Type:
{", ".join(second.get("keys", []))}

Description:
{second.get("description","")}
"""

    return answer