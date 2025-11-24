from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, OptionList
from textual.message import Message
from textual import on


class ModelList(Vertical):
    """Sidebar widget to list and filter models."""

    class Selected(Message):
        """Posted when a model is selected."""

        def __init__(self, model: str):
            self.model = model
            super().__init__()

    def __init__(self, models: list[str], **kwargs):
        super().__init__(**kwargs)
        self.all_models = models
        self.filtered_models = models

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search models...", id="model-search")
        yield OptionList(*self.all_models, id="model-options")

    @on(Input.Changed)
    def filter_models(self, event: Input.Changed) -> None:
        """Filter the list of models based on input."""
        query = event.value.lower()
        self.filtered_models = [m for m in self.all_models if query in m.lower()]

        option_list = self.query_one(OptionList)
        option_list.clear_options()
        option_list.add_options(self.filtered_models)

    @on(OptionList.OptionSelected)
    def on_model_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle model selection."""
        model = str(event.option.prompt)
        self.post_message(self.Selected(model))

    def update_models(self, models: list[str]) -> None:
        """Update the list of available models."""
        self.all_models = models
        self.filtered_models = models
        option_list = self.query_one(OptionList)
        option_list.clear_options()
        option_list.add_options(models)
