Create a bar chart race visualization for a Lichess tournament.

[Video example](https://www.youtube.com/watch?v=dyEkDKnHb8I)

## Usage

1. Setup

    ```
    python -m pip install -r requirements.txt
    ```

1. Generate the csv

    ```
    python main.py
    ```

1. Upload to [Flourish](https://flourish.studio/) (free account is ok), using the "Bar chart race" template.

    Settings:
        - Colors: by bar
        - Labels: max size = .7, space = 8
        - Counter & totalizer: disable both
        - Timeline & animation: pause before loop = 10
        - Header: title = "..."
