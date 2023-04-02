# Workato SDK Connector code generator @gpt-3.5-turbo 
This will generate a new Workato SDK Connector code based on user input via 
gpt-3.5-turbo [Chat Completion API](https://platform.openai.com/docs/api-reference/chat/create)

## Running Locally
### Create new python environment (OPTIONAL)
```bash
python -m venv venv
```

### Activate the python environment (WINDOWS)
```bash
venv/Scripts/activate
```

### Activate the python environment (Linux/Mac)
```bash
source venv/bin/activate
```
### Install openai and streamlit libraries with PIP
```bash
pip install openai streamlit streamlit_pills
```

create a new file under .streamlit/secrets.toml add a new line for your Open AI API Key [OpenAI](https://beta.openai.com/account/api-keys)

```yaml
api_secret = "sk-lköaskjhlhhaskjgaskjgadskgdasgkadsgkasd"
```

Run the app locally
```yaml
streamlit run .\streamlit_app.py
```