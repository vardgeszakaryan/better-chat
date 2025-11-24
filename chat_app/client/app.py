from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer
from chat_app.client.ui.chat_display import ChatDisplay
from chat_app.client.ui.input_area import InputArea
from chat_app.client.ui.model_list import ModelList
from chat_app.core.models import ChatMessage, ChatSession, Role
from chat_app.services.ollama import OllamaService


class BetterChatApp(App):
    """A Textual app for Ollama Chat."""

    CSS = """
    Screen {
        layout: vertical;
    }
    
    #main-container {
        layout: horizontal;
        height: 1fr;
    }

    ModelList {
        width: 30;
        border: round $primary;
        margin: 0 1 0 0;
        background: $surface;
    }
    
    #chat-container {
        layout: vertical;
        width: 1fr;
    }

    ChatDisplay {
        height: 1fr;
        border: round $primary;
        padding: 1;
    }
    
    InputArea {
        height: auto;
        border: round $secondary;
        padding: 1;
    }

    .message-user {
        background: $primary-background-darken-1;
        padding: 1;
        margin: 1;
        border: round $primary;
    }

    .message-assistant {
        background: $secondary-background-darken-1;
        padding: 1;
        margin: 1;
        border: round $secondary;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        super().__init__()
        self.base_url = base_url
        self.model_name = model
        self.session = ChatSession(model=model)
        self.service = OllamaService(base_url=base_url)
        self.title = "Better Chat"
        self.sub_title = f"Connected to {base_url} ({model})"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-container"):
            yield ModelList([], id="sidebar")
            with Container(id="chat-container"):
                yield ChatDisplay()
                yield InputArea()
        yield Footer()

    async def on_mount(self) -> None:
        """Load models on startup."""
        models = await self.service.get_models()
        self.query_one(ModelList).update_models(models)

    def on_model_list_selected(self, message: ModelList.Selected) -> None:
        """Handle model selection from sidebar."""
        self.model_name = message.model
        self.session.model = message.model
        self.sub_title = f"Connected to {self.base_url} ({self.model_name})"
        self.notify(f"Switched to model: {self.model_name}")

    async def on_input_area_submitted(self, message: InputArea.Submitted) -> None:
        """Handle a message submitted by the user."""
        chat_display = self.query_one(ChatDisplay)

        # 1. Create and display User message
        user_msg = ChatMessage(role=Role.USER, content=message.value)
        self.session.messages.append(user_msg)
        chat_display.add_message(user_msg)

        # 2. Create placeholder for Assistant message
        assistant_msg = ChatMessage(role=Role.ASSISTANT, content="...")
        msg_widget = chat_display.add_message(assistant_msg)

        # 3. Stream response
        full_response = ""
        try:
            async for chunk in self.service.stream_chat(self.session):
                if full_response == "":
                    full_response = chunk  # First chunk replaces "..."
                else:
                    full_response += chunk

                msg_widget.update_content(full_response)
                # Force a refresh to show streaming updates smoothly
                self.refresh()
        except Exception as e:
            msg_widget.update_content(f"Error: {e}")
            full_response = f"Error: {e}"

        # 4. Finalize Assistant message in session
        assistant_msg.content = full_response
        self.session.messages.append(assistant_msg)


if __name__ == "__main__":
    app = BetterChatApp()
    app.run()
