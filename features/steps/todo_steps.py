import requests
from behave import given, when, then

BASE_URL = "http://127.0.0.1:8000"

@given("the API is running")
def step_api_running(context):
    # simple health check - if you have /health use it, otherwise just set base url
    context.base_url = BASE_URL

@when('I register with email "{email}" and password "{password}"')
def step_register(context, email, password):
    url = f"{context.base_url}/auth/register"
    context.response = requests.post(url, json={"email": email, "password": password})

@when('I login with email "{email}" and password "{password}"')
def step_login(context, email, password):
    url = f"{context.base_url}/auth/login-json"
    context.response = requests.post(url, json={"email": email, "password": password})

@then('the response status should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code, context.response.text


@then("I should receive a token")
def step_token(context):
    data = context.response.json()
    assert "access_token" in data or "token" in data, data
    context.token = data.get("access_token") or data.get("token")

@given('I am logged in as "{email}" with password "{password}"')
def step_logged_in(context, email, password):
    url = f"{context.base_url}/auth/login-json"
    res = requests.post(url, json={"email": email, "password": password})
    assert res.status_code == 200, res.text
    data = res.json()
    context.token = data.get("access_token") or data.get("token")
    assert context.token is not None, data

@when('I create a todo with title "{title}"')
def step_create_todo(context, title):
    url = f"{context.base_url}/todos"
    headers = {"Authorization": f"Bearer {context.token}"}
    context.response = requests.post(url, json={"title": title, "completed": False}, headers=headers)

@then('the response should contain "id"')
def step_impl(context):
    data = context.response.json()
    assert "id" in data, data

