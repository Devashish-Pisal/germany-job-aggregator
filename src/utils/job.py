

class Job:
    def __init__(
            self,
            # Required parameters
            job_title:str,
            company_name:str,
            location:str,
            description:str,
            job_posting_url:str,
            job_posting_platform:str,

            # Optional parameters
            type_of_work:str="N/A", # e.g full-time, part-time, freelance, etc.
            home_office_possible:bool=False,
            salary:str="N/A",
    ):
        pass


    @staticmethod
    def normalize_job_title(job_title:str):
        pass

    @staticmethod
    def normalize_company_name(company_name:str):
        pass

    @staticmethod
    def normalize_location(location:str):
        pass

    @staticmethod
    def normalize_description(description:str):
        pass

    @staticmethod
    def normalize_job_posting_url(url:str):
        pass


