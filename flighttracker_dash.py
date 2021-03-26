import dash
# from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from GrapherV3 import ResultReader

## ------------------------------------- ##
Reader = ResultReader()
output = Reader.output()

data = []
for i in range(len(output.keys())):
    data.append({'x':output[i][0], 'y':output[i][1], 'type':'line', 'name':Reader.dates[i]})

## ------------------------------------- ##

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Flight Tracker: Air Canada | 12:05 | London -> Toronto',
                        className='nine columns',
                        style={'fontSize':20, 'font-family':'sans-serif'}),
                html.Img(
                    src="https://upload.wikimedia.org/wikipedia/commons/2/24/Air_Canada_Logo.svg",
                    className='three columns',
                    style={
                        'height': '15%',
                        'width': '15%',
                        'float': 'right',
                        'position': 'relative'
                    },
                ),
                html.Div(children='''
                        Jack Walsh - June 2020
                        ''',
                        className='nine columns',
                        style={'marginLeft': '8.5em'}
                )
            ], className="row",
               style={
            'marginLeft': '1.5em',
            'marginTop': '2em'
            }
        ),

        html.Div(
            [
            html.Div([
                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': data,
                        'layout': {
                            'title': ' ',
                            'xaxis' : dict(
                                title='Date',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=15,
                                color='#2b2728'
                            )),
                            'yaxis' : dict(
                                title='Price',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=15,
                                color='#2b2728'
                            ))
                        }
                    }
                )
                ], className= 'twelve columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)

if __name__ == '__main__':
    app.run_server(debug=True)