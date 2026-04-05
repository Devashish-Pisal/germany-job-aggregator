from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


class ValidateConfig(BaseModel):
    country:List[str]
    city:List[str]
    distance: int = Field(gt=0)
    remote: bool
    full_time: bool
    part_time: bool
    search_keywords: List[str]
    page_number: int = Field(gt=0)
    results_per_page: int = Field(gt=0)
    max_pages: int = Field(gt=0)
    output_filename: str = Field(pattern=r"\.csv$")
    use_adzuna_api: bool
    use_arbeitsamt_api: bool
    use_arbeitsnow_api: bool
    output_format: Literal[".csv"]


    @field_validator("country", "city", "search_keywords", mode="before")
    @classmethod
    def lower_list_items(cls, v):
        """
        Normalizes the user inputs field.
        :param v: country, city, search_keyword user input field
        :return: Normalized (without extra spaces and in lower case) inputs
        """
        if isinstance(v, str):
            return [v.strip().lower()]
        if isinstance(v, list):
            return [v_item.strip().lower() if isinstance(v_item, str) else v_item for v_item in v]
        return v


    def validate_adzuna_api_prerequisite(self):
        """
        TODO
        :return:
        """
        pass

    def validate_arbeitsamt_api_prerequisite(self):
        """
        TODO
        :return:
        """
        pass

    def validate_arbeitsnow_api_prerequisite(self):
        """
        TODO
        :return:
        """
        pass




