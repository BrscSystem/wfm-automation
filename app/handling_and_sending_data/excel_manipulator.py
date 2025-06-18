import json
import os
import re
import time

import pandas as pd


class ExcelManipulator:
    TIMEOUT = 600
    MAX_AGE_SECONDS = 600
    FILENAME_SUBSTRING = "EXPORT"

    def __init__(self):
        self.start_time = None
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        self.df = pd.DataFrame()
        self.json_result = None
        self.latest_file = None

    def process_tasks(self):
        self.wait_for_downloads()

        self.treating_dataframe()

        self.dataframe_to_json()

        print("-------- Processed Data - OK --------")

    def wait_for_downloads(self):
        self.start_time = time.time()

        while True:
            files = os.listdir(self.download_path)

            matching_files = [
                f
                for f in files
                if self.FILENAME_SUBSTRING in f and f.endswith(".xlsx")
            ]

            if matching_files:
                latest_file = max(
                    [
                        os.path.join(self.download_path, f)
                        for f in matching_files
                    ],
                    key=os.path.getctime,
                )

                file_creation_time = os.path.getctime(latest_file)
                file_time = time.time() - file_creation_time

                if (
                    not latest_file.endswith(".crdownload")
                    and file_time <= self.MAX_AGE_SECONDS
                ):
                    self.latest_file = latest_file
                    return

            if time.time() - self.start_time > self.TIMEOUT:
                raise Exception("Downloading the file was not completed")

            time.sleep(1)

    def treating_dataframe(self):
        self.df = pd.read_excel(self.latest_file)

        self.df = self.df.replace({float("nan"): None})

        self.df = self.df[
            (self.df["Region"] == "Latin America Region")
            & (self.df["Rep Office"] == "Brazil Rep Office")
            & (
                self.df["Task Type"]
                == "Network Operation - Change Implementation"
            )
        ]

        self.df.rename(
            columns=lambda col: self.format_column_name(col), inplace=True
        )

        self.df.replace(
            {"yes": True, "no": False, "Yes": True, "No": False}, inplace=True
        )

        columns_to_convert = ["planned_number_of_nes", "risk_level_score"]

        for col in columns_to_convert:
            self.df[col] = (
                pd.to_numeric(self.df[col], errors="coerce")
                .fillna(0)
                .astype(int)
            )

    @staticmethod
    def format_column_name(text):
        text = (
            text.strip()
            .replace(" ", "_")
            .replace("-", "_")
            .replace(".", "")
            .replace("'", "")
        )

        text = re.sub(r"(?<![A-Z])(?=[A-Z])", "_", text)
        text = re.sub(r"_{2,}", "_", text)

        if text[0] == "_":
            text = text[1:]

        text = text.lower()

        if text == "operation":
            return "task_operation"

        elif text == "whether_to_use_one_check_one_step":
            return "whether_to_use_one_check"

        return text

    def dataframe_to_json(self):
        json_data = self.df.to_dict(orient="records")

        for record in json_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None

        self.json_result = json.dumps(
            json_data,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
            allow_nan=True,
        )

        try:
            os.remove(self.latest_file)
        except PermissionError:
            pass
