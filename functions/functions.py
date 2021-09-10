def row_to_dict(description, row):
    if row is None:
        return None
    d = {}
    for i in range(0, len(row)):
        value = row[i]
        key = description[i][0]
        try:
            d[key] = value
        except NameError:
            print("Variable x is not defined")
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result



def tuple_to_dict(description, row):
    if row is None or row == []:
        return None
    d = {}
    for i in range(0, len(row[0])):
        value = row[0][i]
        key = description[i][0]
        try:
            d[key] = value
        except NameError:
            print("Variable x is not defined")
    return d



