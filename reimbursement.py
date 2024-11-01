from dataclasses import dataclass
from datetime import date, datetime
import re
from typing import Literal


def parse_date(s: str):
    return datetime.strptime(s, "%m/%d/%y").date()


@dataclass
class Project:
    city_category: Literal["low", "high"]
    start_date: date
    end_date: date

    @classmethod
    def from_string(cls, s: str):
        match = re.match(
            "Project \d+: (?P<cost>\w+) Cost City Start Date: (?P<start>(\d|/)+) End Date: (?P<end>(\d|/)+)",
            s,
        )
        assert match, f'Failed to match: "{s}"'
        return cls(
            city_category=match.group("cost").lower(),
            start_date=parse_date(match.group("start")),
            end_date=parse_date(match.group("end")),
        )


if __name__ == "__main__":
    set1 = ["Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15"]

    set2 = [
        "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
        "Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15",
        "Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15",
    ]

    set3 = [
        "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15",
        "Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15",
        "Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15",
    ]

    set4 = [
        "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
        "Project 2: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
        "Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15",
        "Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15",
    ]

    for i, setI in enumerate([set1, set2, set3, set4]):
        print(f"Set {i + 1}:")
        for project_str in setI:
            print(Project.from_string(project_str))
        print()
