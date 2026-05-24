import os
import subprocess
import sqlite3


def execute_command(user_input):
    os.system(f"ping -c 1 {user_input}")


def run_script(script_name):
    subprocess.call(f"./{script_name}", shell=True)


def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()


def load_config(config_string):
    return eval(config_string)


def process_template(template_name):
    filepath = f"/templates/{template_name}"
    with open(filepath) as f:
        return f.read()
