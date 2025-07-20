import time
import threading
import os
import dearpygui.dearpygui as dpg

FILE_PATH = r"YOUR LOG FILE HERE"
FILTER_STRING = "MessageReceived Status: Success Text"

def read_filtered_file():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()

        filtered_lines = []
        for line in lines:
            if FILTER_STRING in line:
                idx = line.find(FILTER_STRING)
                if idx != -1:
                    clean_line = line[idx:].strip()
                    filtered_lines.append(clean_line)

        return "\n".join(filtered_lines) if filtered_lines else "No matching lines found."

    except Exception as e:
        return f"Error reading file: {e}"

def update_text(sender=None, app_data=None):
    content = read_filtered_file()
    dpg.set_value("text_display", content)

def monitor_file_changes():
    last_mtime = None
    while dpg.is_dearpygui_running():
        try:
            mtime = os.path.getmtime(FILE_PATH)
            if last_mtime is None:
                last_mtime = mtime
                update_text()
            elif mtime != last_mtime:
                last_mtime = mtime
                update_text()
        except Exception as e:
            dpg.set_value("text_display", f"Error monitoring file: {e}")
        time.sleep(0.2)

def main():
    dpg.create_context()
    dpg.create_viewport(title='debug390)', width=800, height=600)

    with dpg.window(label="debug v390"):
        dpg.add_button(label="Manual Refresh", callback=update_text)
        dpg.add_input_text(multiline=True, readonly=True, width=780, height=550, tag="text_display")

    threading.Thread(target=monitor_file_changes, daemon=True).start()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
