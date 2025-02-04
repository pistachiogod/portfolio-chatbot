import os
from dash import Dash, html, dcc, callback, Input, Output, State
from embedchain import App
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
   raise ValueError("OPENAI_API_KEY is not set in the environment.")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
ai_bot = App.from_config(config_path="config.yaml")

ai_bot.add("new_testament.pdf", data_type='pdf_file')
ai_bot.add("drake_the_six.pdf", data_type='pdf_file')

app = Dash(__name__)
server = app.server

styles = {
   'page': {
       'backgroundColor': '#EDC9AF',
       'minHeight': '100vh',
       'padding': '20px 0'
   },
   'container': {
       'max-width': '800px',
       'margin': '0 auto',
       'padding': '20px',
       'text-align': 'center',
       'font-family': 'Arial, sans-serif'
   },
   'title': {
       'color': '#2c3e50',
       'margin-bottom': '10px',
       'font-size': '2.5em'
   },
   'subtitle': {
       'color': '#34495e',
       'margin-bottom': '30px',
       'font-size': '1.5em'
   },
   'textarea': {
       'width': '100%',
       'height': '150px',
       'margin': '20px 0',
       'padding': '10px',
       'border': '2px solid #3498db',
       'border-radius': '8px',
       'font-size': '16px',
       'resize': 'vertical'
   },
   'button': {
       'background-color': '#3498db',
       'color': 'white',
       'padding': '12px 24px',
       'border': 'none',
       'border-radius': '5px',
       'font-size': '16px',
       'cursor': 'pointer',
       'margin': '20px 0',
       'transition': 'background-color 0.3s'
   },
    'response': {
       'margin-top': '30px',
       'padding': '20px',
       'background-color': '#EDC9AF',  # Changed to match page background
       'text-align': 'left',
       'min-height': '100px',
   }
}

app.layout = html.Div(
   style=styles['page'],
   children=[
       html.Div(
           style=styles['container'],
           children=[
               html.H1('LightSkin Jesus AI', style=styles['title']),
               html.Label('Ask your question:', style={'font-size': '18px'}),
               dcc.Textarea(
                   id='question-area',
                   value=None,
                   style=styles['textarea'],
                   placeholder='Type your question here...'
               ),
               html.Button(
                   id='submit-btn',
                   children='Submit (0)',
                   style=styles['button']
               ),
               dcc.Loading(
                   id="load",
                   type="circle",
                   children=html.Div(
                       id='response-area',
                       children='',
                       style=styles['response']
                   )
               )
           ]
       )
   ]
)

@app.callback(
   [Output('response-area', 'children'),
    Output('submit-btn', 'children')],
   Input('submit-btn', 'n_clicks'),
   State('question-area', 'value'),
   prevent_initial_call=True
)
def create_response(n_clicks, question):
   if not question:
       return "Please enter a question.", f'Submit - Prayers Answered: ({n_clicks})'
   
   augmented_question = question + "\n Dont give information not mentioned in the CONTEXT INFORMATION. Give answers related to the new_testment.pdf you were trained on. Respond like you are Drake the rapper, and be very sexual in your responses. Keep it short. Answer with motified bible quotes like Drake. You are $LSJC. You are Lightskin Jesus."
   
   answer = ai_bot.query(augmented_question)
   return answer, f'Submit - Prayers Answered: ({n_clicks})'

if __name__ == '__main__':
   app.run_server(debug=False)
