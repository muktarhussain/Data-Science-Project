# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# load Base Data 
data = spacex_df

# create Marker List
Marker_List = {0:0,1000:1000,2000:2000,3000:3000,4000:4000,5000:5000,6000:6000,7000:7000,8000:8000,9000:9000,9600:9600}

#Convert site into list
Site_list = spacex_df.groupby(['Launch Site']).size().reset_index(name='class count')
Site_list = list(Site_list["Launch Site"])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                        id='site-dropdown',
                                        options=[{'label': 'ALL', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40','value':'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A','value':'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True),

                                    
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),                                
                                
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)                                
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks = Marker_List,
                                                value=[min_payload, max_payload]),
                                
                                
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                               ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def pie(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Succes count for all launch sites')
    else:
        title_pie = f"Success Launches for site {site_dropdown}"
        filtered_DD = spacex_df[spacex_df['Launch Site']==site_dropdown]
        filtered_LS = filtered_DD.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(filtered_LS, values='class count', names='class', title= title_pie)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])



def build_scatter(site,payload):
    low,high = (payload[0], payload[1])
    filtered_Spa = spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)]
    if site == 'ALL':
        title_sca = f"Success Launches for site {site}"
        fig = px.scatter(filtered_Spa,x="Payload Mass (kg)", y="class", color="Booster Version Category", title=title_sca)
    else:
        title_sca = f"Success Launches for site {site}"
        filtered_sit= filtered_Spa[filtered_Spa['Launch Site'] == site]
        fig = px.scatter(filtered_sit,x="Payload Mass (kg)", y="class", color="Booster Version Category", title=title_sca)
    return fig
 



    
if __name__ == '__main__':
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
    app.run_server( host="localhost",port=8030, debug=False, dev_tools_ui=False, dev_tools_props_check=False)
