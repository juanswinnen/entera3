import pandas as pd

# Log de envío
dfLog = pd.DataFrame(columns=['Status', 'Name', 'Phone', 'Msg'])
new_row = {'Status': 'Enviado', 'Name': 'Mati', 'Phone': '33884747', 'Msg': 'Hola!'}
dfLog.append(new_row, ignore_index=True, inplace=True)

print(dfLog)