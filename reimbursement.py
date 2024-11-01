from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pprint import pprint
import re
from typing import Literal


RATES = {
    "low": {
        "travel": 45,
        "full": 75,
    },
    "high": {
        "travel": 55,
        "full": 85,
    },
}


def parse_date(s: str):
    return datetime.strptime(s, "%m/%d/%y").date()


CityCategory = Literal["low", "high"]


@dataclass
class Project:
    city_category: CityCategory
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

    @classmethod
    def list_from_strings(cls, *strings: str):
        return [cls.from_string(s) for s in strings]


def iterate_dates_in_range(start: date, end: date) -> Iterator[date]:
    """Returns an iterator of dates in the range between the given start and end
    dates (inclusive)."""
    next = start
    while next <= end:
        yield next
        next += timedelta(days=1)


def calculate_reimbursement(projects: Iterable[Project]) -> int:
    """Calculates the reimbursement amount for the given set of projects."""
    # Build a mapping from date to the set of city categories for projects
    # scheduled that day
    project_date_map = defaultdict(set)
    for project in projects:
        for d in iterate_dates_in_range(project.start_date, project.end_date):
            project_date_map[d].add(project.city_category)

    amount = 0
    for d, city_categories in project_date_map.items():
        if city_categories == set(("low", "high")):
            # When the projects on the same day have different categories, use
            # "high" for reimbursement
            city_category = "high"
        else:
            # Only one category is scheduled for this day, so use that value
            assert len(city_categories) == 1
            city_category = next(iter(city_categories))

        # When the previous or next day has no projects scheduled, this day is
        # considered a travel day
        prev_day = project_date_map.get(d - timedelta(days=1))
        next_day = project_date_map.get(d + timedelta(days=1))
        if not prev_day or not next_day:
            day_category = "travel"
        else:
            day_category = "full"

        amount += RATES[city_category][day_category]

    return amount


if __name__ == "__main__":

    set1 = Project.list_from_strings(
        "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15"
    )

    set2 = Project.list_from_strings(
        "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
        "Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15",
        "Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15",
    )

    set3 = Project.list_from_strings(
        "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15",
        "Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15",
        "Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15",
    )

    set4 = Project.list_from_strings(
        "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
        "Project 2: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
        "Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15",
        "Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15",
    )

    for i, projects in enumerate([set1, set2, set3, set4]):
        print(f"Set {i + 1}:")
        pprint(projects)
        print(f"Reimbursement amount: ${calculate_reimbursement(projects)}")
        print()
