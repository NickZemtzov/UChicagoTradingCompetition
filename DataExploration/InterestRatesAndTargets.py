#put this in the data for case 1 folder
import pandas as pd
import plotly.graph_objects as go


df_target = pd.read_csv("announcements.csv")
df_real = pd.read_csv("interest_rates.csv")

HAPtarget = []
RORtarget = []
USDtarget = []
HAPreal = df_real["HAP"].values.tolist()
RORreal = df_real["ROR"].values.tolist()
USDreal = df_real["USD"].values.tolist()
for i in range(59):
    while len(HAPtarget) < df_target["Time"].values.tolist()[i+1]:
        HAPtarget.append(df_target["RateTarget"].values.tolist()[i])
while len(HAPtarget) < 2520:
    HAPtarget.append(df_target["RateTarget"].values.tolist()[59])

for i in range(60, 109):
    while len(RORtarget) < df_target["Time"].values.tolist()[i+1]:
        RORtarget.append(df_target["RateTarget"].values.tolist()[i])
while len(RORtarget) < 2520:
    RORtarget.append(df_target["RateTarget"].values.tolist()[109])

for i in range(110, 189):
    while len(USDtarget) < df_target["Time"].values.tolist()[i+1]:
        USDtarget.append(df_target["RateTarget"].values.tolist()[i])
while len(USDtarget) < 2520:
    USDtarget.append(df_target["RateTarget"].values.tolist()[189])




df_net = pd.DataFrame()#columns = ['HAPtarget', 'HAPreal','RORtarget', 'RORreal','USDtarget', 'USDreal']) 
df_net["HAPtarget"] = HAPtarget
df_net["HAPreal"] = HAPreal
df_net["RORtarget"] = RORtarget
df_net["RORreal"] = RORreal
df_net["USDtarget"] = USDtarget
df_net["USDreal"] = USDreal



fig = go.Figure()
fig.add_trace(go.Scatter(x=df_net.index, y=df_net["HAPtarget"], name='HAPtarget', line=dict(color='black', width=1)))
fig.add_trace(go.Scatter(x=df_net.index, y=df_net["HAPreal"], name='HAPreal', line=dict(color='firebrick', width=2)))
fig.add_trace(go.Scatter(x=df_net.index, y=df_net["RORtarget"], name='RORtarget', line=dict(color='black', width=1)))
fig.add_trace(go.Scatter(x=df_net.index, y=df_net["RORreal"], name='RORreal', line=dict(color='green', width=2)))
fig.add_trace(go.Scatter(x=df_net.index, y=df_net["USDtarget"], name='USDtarget', line=dict(color='black', width=1)))
fig.add_trace(go.Scatter(x=df_net.index, y=df_net["USDreal"], name='USDreal', line=dict(color='blue', width=2)))

fig.show()
