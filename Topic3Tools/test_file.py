import ast


expr = "2 + 8"
p = ast.parse(expr)
print("Parse:", p)
result = ast.literal_eval(p)
print("Result:", result)
