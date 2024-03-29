import os
from dash import Dash, html, dcc, callback, Input, Output, State
from embedchain import App
from dotenv import load_dotenv
# pip install -r requirements.txt

load_dotenv()
# Create a bot instance
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
ai_bot = App.from_config(config_path="config.yaml")

# Embed resources: websites, PDFs, videos
ai_bot.add("will_info.pdf", data_type='pdf_file')
ai_bot.add("Blumrosen_resume2024.pdf", data_type='pdf_file')

app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1('Will Blumrosen ChatBot'),
    html.H3('This AI chatbot was trained on files about Will Blumrosen. Please ask it any questions regarding Will Blumrosen. For example, what are his favorite movies? What are his hobbies? Where has he traveled? What jobs has he had? '),
    html.Label('Ask your question:'),
    html.Br(),
    dcc.Textarea(id='question-area', value=None, style={'width': '25%', 'height': 100}),
    html.Br(),
    html.Button(id='submit-btn', children='Submit'),
    dcc.Loading(id="load", children=html.Div(id='response-area', children='')),
])

@callback(
    Output('response-area', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('question-area', 'value'),
    prevent_initial_call=True
)
def create_response(_, question):
    # Construct augmented question with prompts
    augmented_question = question + "\n Dont give information not mentioned in the CONTEXT INFORMATION. Give information related to Will Blumrosen ONLY. If the answer is NO, respond with 'I don't know'"

    answer = ai_bot.query(augmented_question)
    return answer


if __name__ == '__main__':
    app.run_server(debug=False)
