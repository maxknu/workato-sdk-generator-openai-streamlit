import openai
import streamlit as st
from streamlit_pills import pills

openai.api_key = st.secrets['api_secret']

st.subheader("Workato `SDK` Connector generator")

# You can also use radio buttons instead
selected = pills("", ["SDK Code"], [""])

prePrompt2 = "Example of Workato Connector SDK code for Star Wars API\n{\n  title: 'Star Wars API',\n\n  connection: {\n    fields: [\n      { name: 'API_KEY', type: 'string' }\n    ],\n\n    authorization: {\n      type: \"custom_auth\",\n\n      apply: lambda do |connection|\n        headers(\"Authorization\": \"Bearer \" + connection[\"API_KEY\"])\n      end\n    },\n\n    base_uri: lambda do\n      \"https://swapi.dev\"\n    end\n  },\n\n  test: lambda do |connection|\n    response = get(\"/api/people/1\").\n      after_error_response(/.*/) do |_, body, _, message|\n        error(\"Error connecting to SWAPI: #{message}: #{body}\")\n      end\n  end,\n\n  actions: {\n    get_person_by_id: { \n      title: \"Get person\",\n      subtitle: \"Get person by Id from Swapi API\",\n      input_fields: lambda do\n        [\n          { name: 'id', label: 'Person ID', type: 'integer' }\n        ]\n      end,\n      execute: lambda do |connection, input|\n        response = get(\"/api/people/#{input[\"id\"]}/\")\n      end,\n      output_fields: lambda do\n        [\n          { name: \"name\", label: \"Person name\", type: \"string\" },\n          { name: \"height\", label: \"Person height\", type: \"string\" },\n          { name: \"mass\", label: \"Person mass\", type: \"string\" }\n        ]\n      end,\n      sample_output: lambda do |_connection, _input|\n        { \"name\": \"Luke Skywalker\", \"height\": \"172\", \"mass\": \"77\" }\n      end\n    }\n  },\n  \n  triggers: {\n    new_person_polled_trigger: {\n    title: \"New/Updated person\",\n    subtitle: \"Triggers when a new person is added or updated in SWAPI\",\n    input_fields: lambda do |object_definitions|\n        [\n          { name: 'since',  type: 'timestamp', optional: true, sticky: true }\n        ]\n    end,\n    \n    poll: lambda do |connection, input, closure, _eis, _eos|\n      closure = {} unless closure.present?\n      page_size = 100\n      updated_since = (closure['cursor'] || input['since'] || Time.now ).to_time.utc.iso8601\n      response = get(\"/api/people/\")\n      people = response.dig(\"results\")\n      closure['cursor'] = people.last['edited'] unless people.blank?\n      \n      { events: people, next_poll: closure, can_poll_more: people.length >= page_size }\n    end,\n      \n    dedup: lambda do |record|\n        \"#{record['name']}@#{record['edited']}\"\n    end,\n    \n    output_fields: lambda do\n      [\n        { control_type: \"text\", label: \"Name\", type: \"string\", name: \"name\" },\n        { control_type: \"text\", label: \"Height\", type: \"string\", name: \"height\" }\n      ]\n    end,\n    sample_output: lambda do\n      { \"name\": \"R5-D4\", \"height\": \"97\", }\n    end\n  }\n}\n}"
  
appname = st.text_input("App Name", placeholder = "Stripe", key="appname")
actions = st.text_input("Action Name", placeholder = "Create a product", key="actions")
triggers = st.text_input("Trigger(s) name", placeholder = "On new/updated customer", key="triggers")
auth = st.text_input("Auth", placeholder = "API-KEY", key="auth")
base_uri = st.text_input("Base URL", placeholder = "https://api.stripe.com", key="base_uri")

prompt = f'Generate Workato Connector SDK for {appname} API. With Action(s) {actions} and Trigger(s) {triggers} and base_uri {base_uri} and authorization using {base_uri}'

if st.button("Submit", type="primary"):
    st.markdown("----")
    res_box = st.empty()
    
    if selected == "SDK Code":
        report = []
        # Looping over the response
        for resp in openai.ChatCompletion.create(
                                            model='gpt-3.5-turbo',
                                            messages=[{"role": "system", "content": prePrompt2},
                                                      {"role": "user", "content": prompt}],
                                            max_tokens=1600, 
                                            temperature = 0.1,
                                            stream = True):
            # Example on how to print delta to log https://til.simonwillison.net/gpt3/python-chatgpt-streaming-api
            #  for chunk in response:
            #    content = chunk["choices"][0].get("delta", {}).get("content")
            #      if content is not None:
            #        print(content, end='')

            content = resp["choices"][0].get("delta", {}).get("content")
            if content is not None:
                report.append(content)
                result = "".join(report)      
                res_box.code(result, language='ruby')
st.markdown("----")