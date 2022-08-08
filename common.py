from collections import namedtuple
from typing import Iterator, Optional


# Types
Breed = namedtuple("Breed", ["name", "group"])


def print_results(breeds: Iterator[Breed], outfile: Optional[str]) -> None:
    # Report results
    header = "Name, Group\n"
    format_gen = (f"{b.name}, {b.group}\n" for b in sorted(breeds))

    if outfile is None:
        print(header, end="")
        for l in format_gen:
            print(l, end="")
    else:
        with open(outfile, "w") as f:
            f.write(header)
            f.writelines(format_gen)
            print(f"Results written to {outfile}")
