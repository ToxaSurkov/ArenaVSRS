"""
File: calculate_rating.py
Author: Dmitry Ryumin
Description: Event handler for Gradio app to calculate rating.
License: MIT License
"""

import time
import math
import pandas as pd
from pathlib import Path
import gradio as gr

# Importing necessary components for the Gradio app
from app.config import config_data
from app.data_init import csv_vsa_files, xlsx_unique_subjects
from app.rating_utils import get_rows_to_evaluate
from app.utils import (
    get_csv_files,
    parse_course_data,
    randomize_results,
    wrap_subjects,
)
from app.components import (
    dataframe,
    textbox_create_ui,
    dropdown_create_ui,
    button,
    html_message,
)


def event_handler_calculate_rating(
    surname: str,
    username: str,
    dropdown_user: str,
    csv_vsa_file: str,
    vacancy_id: int,
    dropdown_rating_a: int,
    dropdown_rating_b: int,
):
    """
    Обработчик события, который сохраняет рейтинг в CSV файл

    Args:
        surname (str): Имя
        username (str): Фамилия
        dropdown_user (str): Принадлежность
        csv_vsa_file (str): Путь к CSV файлу с названием группы вакансий
        vacancy_id (int): ID вакансии, которая оценивается
        dropdown_rating_a (int): Оценка для первой метрики
        dropdown_rating_b (int): Оценка для второй метрики
    """

    output_dir_path = Path(config_data.StaticPaths_ARENA)
    csv_vsa_path = Path(csv_vsa_file)

    filename = csv_vsa_path.name

    output_file_path = output_dir_path / filename

    output_dir_path.mkdir(parents=True, exist_ok=True)

    new_data = {
        "ID": [vacancy_id],
        "SURNAME": [surname],
        "USERNAME": [username],
        "AFFILIATION": [dropdown_user],
        "SBERT": [dropdown_rating_a],
        "SBERT_LLM": [dropdown_rating_b],
    }

    new_df = pd.DataFrame(new_data)

    if output_file_path.exists():
        new_df.to_csv(
            output_file_path,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8-sig",
            sep=";",
        )
    else:
        new_df.to_csv(
            output_file_path,
            mode="w",
            header=True,
            index=False,
            encoding="utf-8-sig",
            sep=";",
        )

    start_time = time.time()
    ratings_files = get_csv_files(config_data.StaticPaths_ARENA)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения 1: {execution_time:.3f} секунд")

    rows_to_evaluate = get_rows_to_evaluate(
        csv_vsa_files,
        ratings_files,
        config_data.Settings_EVALUATE_LIMIT,
        surname,
        username,
        dropdown_user,
    )

    if rows_to_evaluate:
        next_row_to_evaluate = rows_to_evaluate[0]
        next_vsa_dataframe_headers = list(next_row_to_evaluate.keys())
        next_vsa_row = pd.Series(next_row_to_evaluate)

        state = {
            "random_order": None,
            "dataframe_a": wrap_subjects(
                parse_course_data(next_vsa_row[next_vsa_dataframe_headers[7]], [2, 3]),
                xlsx_unique_subjects,
            ),
            "dataframe_b": wrap_subjects(
                parse_course_data(
                    next_vsa_row[next_vsa_dataframe_headers[6]], None, True
                ),
                xlsx_unique_subjects,
            ),
        }

        parsed_next_dataframe_a, headers_a, parsed_next_dataframe_b, headers_b = (
            randomize_results(config_data, state)
        )

        if isinstance(next_vsa_row["KeySkills"], str):
            key_skills = [
                item.strip()
                for item in next_vsa_row["KeySkills"].split(",")
                if item.strip()
            ]
            noti_keyskills_visible = False
        elif math.isnan(next_vsa_row["KeySkills"]):
            key_skills = None
            noti_keyskills_visible = True

        return (
            textbox_create_ui(
                value=next_row_to_evaluate["source_file"],
                type="text",
                label=None,
                placeholder=None,
                info=None,
                max_lines=1,
                show_label=False,
                interactive=False,
                visible=False,
                show_copy_button=False,
                scale=1,
                container=False,
            ),
            textbox_create_ui(
                value=next_vsa_row["ID"],
                type="text",
                label=None,
                placeholder=None,
                info=None,
                max_lines=1,
                show_label=False,
                interactive=False,
                visible=False,
                show_copy_button=False,
                scale=1,
                container=False,
            ),
            textbox_create_ui(
                value=next_vsa_row["Name"],
                type="text",
                label=None,
                placeholder=None,
                info=None,
                max_lines=1,
                show_label=False,
                interactive=False,
                visible=True,
                show_copy_button=False,
                scale=1,
                container=False,
            ),
            gr.HTML(
                value=next_vsa_row["Description"], elem_classes="vacancy_description"
            ),
            dropdown_create_ui(
                label=config_data.Labels_DROPDOWN_KEYSKILLS,
                info=config_data.InformationMessages_DROPDOWN_KEYSKILLS,
                choices=key_skills,
                value=key_skills,
                multiselect=True,
                interactive=False,
                visible=not noti_keyskills_visible,
                elem_classes="dropdown-keyskills",
            ),
            html_message(
                message=config_data.InformationMessages_NOTI_KEYSKILLS,
                error=True,
                visible=noti_keyskills_visible,
            ),
            dataframe(
                headers=headers_a,
                values=parsed_next_dataframe_a,
                label=config_data.Labels_RESULT_A,
                show_label=True,
                visible=True,
            ),
            dataframe(
                headers=headers_b,
                values=parsed_next_dataframe_b,
                label=config_data.Labels_RESULT_B,
                show_label=True,
                visible=True,
            ),
            dropdown_create_ui(
                label=f"{config_data.Labels_DROPDOWN_RATING} {config_data.Settings_RATING_SCALE}",
                info=config_data.InformationMessages_DROPDOWN_RATING_INFO,
                choices=range(1, config_data.Settings_RATING_SCALE + 1),
                value=None,
                visible=True,
                elem_classes="dropdown-container",
            ),
            dropdown_create_ui(
                label=f"{config_data.Labels_DROPDOWN_RATING} {config_data.Settings_RATING_SCALE}",
                info=config_data.InformationMessages_DROPDOWN_RATING_INFO,
                choices=range(1, config_data.Settings_RATING_SCALE + 1),
                value=None,
                visible=True,
                elem_classes="dropdown-container",
            ),
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
