# Multi-Source Job Aggregator – Python API & Data Pipeline Project ![Status](https://img.shields.io/badge/status-under--development-red)

This project is a modular Python-based job aggregator that integrates multiple public APIs to collect, normalize, and deduplicate job listings into a unified dataset.
It demonstrates practical skills in API integration, data processing, and building simple data pipelines with clean architecture.

## Project Pipeline

<p align="center">
  <img src="assets/multi-source-job-aggregation_high-level-pipeline.png" width="700">
</p>


### Project tries to solve following 2 central problems
- No need to repeat the same tasks on different job boards. Just edit the config once and then let project do job board hopping on the behalf of user.
- No need to search for different synonymes keywords (e.g python entwickler, python developer, python software developer, etc.) on the same job board website, just list all synonyms at once in the keywords list and project will iterate through all of them.


## Config Support Documentation
| Config Key      | Value Type  | JobSpy | Arbeitsamt | Adzuna | Arbeitnow | Jooble | Findwork | Notes |
|-----------------|-------------|--------|------------|--------|-----------|--------|----------|-------|
| country         | `list[str]` |        |            |        |           |        |          |       |
| city            | `list[str]` |        |            |        |           |        |          |       |
| distance (km)   | `int`       |        |            |        |           |        |          |       |
| remote          | `bool`      |        |            |        |           |        |          |       |
| full_time       | `bool`      |        |            |        |           |        |          |       |
| part_time       | `bool`      |        |            |        |           |        |          |       |
| search_keywords | `list[str]` |        |            |        |           |        |          |       |
| output_filename | `str`       |        |            |        |           |        |          |       |


## Project Extension Ideas
- TODO


## TODO

> **Project Status:** Work in progress — ongoing development.
