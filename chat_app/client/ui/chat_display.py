from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Markdown, Static
from chat_app.core.models import ChatMessage, Role


class ChatMessageWidget(Static):
    """A widget to display a single chat message."""

    def __init__(self, message: ChatMessage, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.content_widget = Markdown(self.message.content)

    def compose(self) -> ComposeResult:
        timestamp = self.message.timestamp.strftime("%H:%M:%S")
        role_color = "green" if self.message.role == Role.USER else "blue"
        header = (
            f"[{role_color}]**{self.message.role.name.title()}**[/] *[{timestamp}]*"
        )

        yield Markdown(header)
        yield self.content_widget

    def update_content(self, new_content: str):
        """Updates the content of the message (for streaming)."""
        self.message.content = new_content
        self.content_widget.update(new_content)


class ChatDisplay(VerticalScroll):
    """A scrollable display for chat messages."""

    def compose(self) -> ComposeResult:
        yield Static(
            "Welcome to Better Chat (Ollama Edition)! :rocket:", id="welcome-msg"
        )

    def add_message(self, message: ChatMessage) -> ChatMessageWidget:
        """Adds a new message to the display and returns the widget."""
        msg_widget = ChatMessageWidget(message, classes=f"message-{message.role.value}")
        self.mount(msg_widget)
        msg_widget.scroll_visible()
        return msg_widget
