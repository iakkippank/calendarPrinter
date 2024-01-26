import inquirer
from data.Event import Event


def show_selection_prompt(event_list: list[Event]) -> list[Event]:
    # Convert events list to a tupel list
    event_choices = [(event.format_event_to_readable_string(), event) for event in event_list]

    # Prompt user to select events
    questions = [
        inquirer.Checkbox(
            "Events",
            message="Welche sind wichtig?",
            choices=event_choices,
            default=event_list
        ),
    ]
    answers = inquirer.prompt(questions)["Events"]

    select_labels = [str(answer) for answer in answers]
    print("---------------------------------\n\nAusgewählte Events:")
    for label in select_labels:
        print(label)

    selection = [answer.tag for answer in answers]

    return selection
