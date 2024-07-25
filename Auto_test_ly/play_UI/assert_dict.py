from playwright import sync_api
from playwright.sync_api import expect

def login_sh(page: sync_api.Page):
    expect("Response").to_be_ok()