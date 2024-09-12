"""
File: dropdown_rating.py
Author: Dmitry Ryumin
Description: Event handler for Gradio app to dropdown rating.
License: MIT License
"""

# Importing necessary components for the Gradio app
from app.config import config_data
from app.components import (
    button,
    html_message,
)


def event_handler_dropdown_rating(dropdown_rating_a, dropdown_rating_b):
    if not dropdown_rating_a and not dropdown_rating_b:
        return (
            button(
                value=config_data.OtherMessages_CALCULATE_RATING,
                interactive=False,
                scale=1,
                icon=config_data.StaticPaths_IMAGES + "calculate_rating.ico",
                visible=True,
                elem_classes="calculate_rating",
            ),
            html_message(
                message=config_data.InformationMessages_NOTI_CALCULATE_RATING[0],
                error=True,
                visible=True,
            ),
        )
    elif not dropdown_rating_a and dropdown_rating_b:
        return (
            button(
                value=config_data.OtherMessages_CALCULATE_RATING,
                interactive=False,
                scale=1,
                icon=config_data.StaticPaths_IMAGES + "calculate_rating.ico",
                visible=True,
                elem_classes="calculate_rating",
            ),
            html_message(
                message=config_data.InformationMessages_NOTI_CALCULATE_RATING[1],
                error=True,
                visible=True,
            ),
        )
    elif dropdown_rating_a and not dropdown_rating_b:
        return (
            button(
                value=config_data.OtherMessages_CALCULATE_RATING,
                interactive=False,
                scale=1,
                icon=config_data.StaticPaths_IMAGES + "calculate_rating.ico",
                visible=True,
                elem_classes="calculate_rating",
            ),
            html_message(
                message=config_data.InformationMessages_NOTI_CALCULATE_RATING[2],
                error=True,
                visible=True,
            ),
        )
    else:
        return (
            button(
                value=config_data.OtherMessages_CALCULATE_RATING,
                interactive=True,
                scale=1,
                icon=config_data.StaticPaths_IMAGES + "calculate_rating.ico",
                visible=True,
                elem_classes="calculate_rating",
            ),
            html_message(
                message=config_data.InformationMessages_NOTI_CALCULATE_RATING[3],
                error=True,
                visible=False,
            ),
        )
