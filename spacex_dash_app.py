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
dropdown_opt = spacex_df['Launch Site'].unique().tolist()
dropdown_opt.append('All sites')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(dropdown_opt, 'All sites', id='site-dropdown', placeholder='Select a launch site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(selected_site):
    if selected_site == 'All sites':
        fig = px.pie(spacex_df[spacex_df['class']==1], values='class', names='Launch Site', title='Total successful launches by site')
    else:
        fig = px.pie(spacex_df[spacex_df['Launch Site']==selected_site], names='class', title=f'Successful vs. failed launches for site {selected_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(selected_site, range):
    df = spacex_df[spacex_df['Payload Mass (kg)'].between(range[0], range[1])]
    if selected_site == 'All sites':
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Coorelation between payload and success')
    else:
        fig = px.scatter(df[df['Launch Site']==selected_site], x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Coorelation between payload and success for site {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
