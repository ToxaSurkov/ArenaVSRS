"""
File: components.py
Author: Dmitry Ryumin
Description: Utility functions for creating Gradio components.
License: MIT License
"""

import gradio as gr
from typing import List, Literal, Optional

# Importing necessary components for the Gradio app


def html_message(
    message: str = "", error: bool = True, visible: bool = True
) -> gr.HTML:
    css_class = "noti_err" if error else "noti_true"

    return gr.HTML(value=f"<h3 class='{css_class}'>{message}</h3>", visible=visible)


def dataframe(
    headers: Optional[List] = None,
    values: Optional[List] = None,
    label: Optional[str] = None,
    show_label: bool = True,
    height: int = 500,
    wrap: bool = True,
    visible: bool = True,
    interactive: bool = False,
    elem_classes: Optional[str] = "dataframe",
) -> gr.Dataframe:
    if headers is None or values is None:
        datatype = "str"
    else:
        datatype = ["markdown"] * len(headers)

    return gr.Dataframe(
        value=values,
        headers=headers,
        datatype=datatype,
        label=label,
        show_label=show_label,
        height=height,
        wrap=wrap,
        visible=visible,
        interactive=interactive,
        elem_classes=elem_classes,
    )


def textbox_create_ui(
    value: Optional[str] = None,
    type: Literal["text", "password", "email"] = "text",
    label: Optional[str] = None,
    placeholder: Optional[str] = None,
    info: Optional[str] = None,
    max_lines: int = 1,
    show_label: bool = True,
    interactive: bool = True,
    visible: bool = True,
    show_copy_button: bool = True,
    scale: int = 1,
    container: bool = False,
):
    return gr.Textbox(
        value=value,
        type=type,
        label=label,
        placeholder=placeholder,
        info=info,
        max_lines=max_lines,
        show_label=show_label,
        interactive=interactive,
        visible=visible,
        show_copy_button=show_copy_button,
        scale=scale,
        container=container,
    )


def dropdown_create_ui(
    label: Optional[str] = None,
    info: Optional[str] = None,
    choices: Optional[List[str]] = None,
    value: Optional[List[str]] = None,
    multiselect: bool = False,
    show_label: bool = True,
    interactive: bool = True,
    visible: bool = True,
    render: bool = True,
    elem_classes: Optional[str] = None,
) -> gr.Dropdown:
    return gr.Dropdown(
        choices=choices,
        value=value,
        multiselect=multiselect,
        label=label,
        info=info,
        show_label=show_label,
        interactive=interactive,
        visible=visible,
        render=render,
        elem_classes=elem_classes,
    )


def button(
    value: str = "",
    interactive: bool = True,
    scale: int = 1,
    icon: Optional[str] = None,
    visible: bool = True,
    elem_classes: Optional[str] = None,
) -> gr.Button:
    return gr.Button(
        value=value,
        interactive=interactive,
        scale=scale,
        icon=icon,
        visible=visible,
        elem_classes=elem_classes,
    )
