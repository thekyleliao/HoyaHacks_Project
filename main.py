# Imports stuff
import taipy as tp
from taipy import Config, Core, Gui


# Function that builds a message from input
def build_message(age):
    return f"You are {age} years old!"


# Config stuff
input_name_data_node_cfg = Config.configure_data_node(id="input_name")
message_data_node_cfg = Config.configure_data_node(id="age")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_name_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

# Variables
input_name = "18"
age = None


# no clue what this does
def submit_scenario(state):
    state.scenario.input_name.write(state.input_name)
    state.scenario.submit()
    state.age = scenario.age.read()

# Formats the page
page = """
Enter your age: <|{input_name}|input|>

<|Click|button|on_action=submit_scenario|>

Message: <|{age}|text|>
"""

# Runs the application
if __name__ == "__main__":
    Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    Gui(page).run()
