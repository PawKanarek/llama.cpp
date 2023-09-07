from time import monotonic
from subprocess import Popen, PIPE
from textual import events
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static, RichLog, Log
from textual.reactive import reactive

def appendPrompt(new_question: str) -> str:
    # https://huggingface.co/blog/codellama#conversational-instructions
    # <s>[INST] <<SYS>>
    # {{ system_prompt }}
    # <</SYS>>

    # {{ user_msg_1 }} [/INST] {{ model_answer_1 }} </s><s>[INST] {{ user_msg_2 }} [/INST]
    sys = "Write code only in python. Give hints how to refactor existing code"
    question = """Please write continuation to this code:
[PYTHON]
def run_llama():
    args = ['./main', 
        '--model', './models/CodeLlama-34b-Instruct/ggml-model-q4_0.gguf',
        '--n-predict', '-1',
        '--ctx-size', '4096',
        '--prompt', prompt]
    output = start(args)
    save("_session.txt", output)
[/PYTHON]
    """
    response = """Sure, here's a continuation of your code. I assume you want to define the missing `start()` and `save()` functions. Additionally, I noticed that you haven't defined the `prompt` variable. You should define it before calling the run_llama() function.
```
from subprocess import Popen, PIPE

prompt = "Your prompt goes here."

def run_llama():
    args = ['./main', 
        '--model', './models/CodeLlama-34b-Instruct/ggml-model-q4_0.gguf',
        '--n-predict', '-1',
        '--ctx-size', '4096',
        '--prompt', prompt]
    output = start(args)
    save("_session.txt", output)

def start(args: []) -> list[str]():
    output = []
    with Popen(args, stdout=PIPE, universal_newlines=True) as p:
        for line in p.stdout:
            output.append(line)
            log(line, end='')
    return output

def save(filename, content):
    try:
        with open(filename, "w") as file:
            file.write(content)
        log(f"Saved to {filename}")
    except Exception as e:
        log(f"An error occurred while saving to {filename}: {str(e)}")
```"""
    #prompt = f'{s_b}{INST_b}\n{sys_prompt.strip()}\n{SYS_e}\\n{prompt_init.strip()}\n{INST_e}'
    p  = f"<<SYS>>\\n{sys}\\n<</SYS>>\\n\\n{question}"
    p  = f"<s>[INST] {p.strip()} [/INST] {response.strip()} </s>"
    p += f"<s>[INST] {new_question.strip()} [/INST]"
    return p

class TimeDisplay(Static):
    """A widget to display elapsed time."""

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update time to current."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self):
        """Method to reset the time display to zero."""
        self.total = 0
        self.time = 0

class Stopwatch(Static):
    """A stopwatch widget."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Add", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay()

class Output(RichLog):
    def on_key(self, event: events.Key) -> None:
        self.write(event)

class CodeLlamaApp(App):
    """A Textual app to manage CodeLLama."""

    new_prompt = """Write graphical UI in python using textual. Create window that have 3 buttons from left and a text output window from right"""

    def run_llama(self):
        args = ['./main', 
            '--model', './models/CodeLlama-34b-Instruct/ggml-model-q4_0.gguf',
            '--n-predict', '-1',
            '--ctx-size', '4096',
            '--prompt', appendPrompt(self.new_prompt)]
        output = self.start(args)
        self.save("_session.txt", output)
    
    def start(self, args: []) -> list[str]:
        output = []
        with Popen(args, stdout=PIPE, universal_newlines=True) as p:
            for line in p.stdout:
                output.append(line)
                self.query_one(Output).write(line)

        return output

    def save(self, filename: str, content: list[str]):
        try:
            with open(filename, "w") as file:
                file.write(content)
            log(f"Saved to {filename}")
        except Exception as e:
            log(f"An error occurred while saving to {filename}: {str(e)}")


    CSS_PATH = "_app.tcss"

    BINDINGS = [
        ("r", "run_llama", "Run"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield Output()
        yield Button("Run llama")
        yield ScrollableContainer(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")

    def action_run_llama(self) -> None:
        """An action to run ra Llama"""
        new_stopwatch = Stopwatch()
        self.run_llama()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()


def main():
    app = CodeLlamaApp()
    app.run()
if __name__ == "__main__":
    main()