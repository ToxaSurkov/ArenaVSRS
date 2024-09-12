"""
File: auth.py
Author: Dmitry Ryumin
Description: Event handler for Gradio app to change auth.
License: MIT License
"""

# Importing necessary components for the Gradio app
from app.config import config_data
from app.components import (
    button,
    html_message,
)


def event_handler_auth(surname, username, dropdown_user):
    surname = surname.strip()
    username = username.strip()

    if surname and username and dropdown_user:
        return (
            button(
                value=config_data.OtherMessages_AUTH,
                interactive=True,
                scale=1,
                icon=config_data.StaticPaths_IMAGES + "auth.ico",
                visible=True,
                elem_classes="auth",
            ),
            html_message(
                message=config_data.InformationMessages_NOTI_AUTH[1],
                error=False,
                visible=True,
            ),
        )
    else:
        return (
            button(
                value=config_data.OtherMessages_AUTH,
                interactive=False,
                scale=1,
                icon=config_data.StaticPaths_IMAGES + "auth.ico",
                visible=True,
                elem_classes="auth",
            ),
            html_message(
                message=config_data.InformationMessages_NOTI_AUTH[0],
                error=True,
                visible=True,
            ),
        )
