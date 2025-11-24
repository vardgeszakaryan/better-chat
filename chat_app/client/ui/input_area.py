from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Input
from textual.message import Message


class InputArea(Container):
    """Input area for typing messages."""

    class Submitted(Message):
        """Posted when the user submits a message."""

        def __init__(self, value: str):
            self.value = value
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type a message...", id="message-input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.value.strip():
            self.post_message(self.Submitted(event.value))
            event.input.value = ""
