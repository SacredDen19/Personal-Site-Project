import re

def error_parser(log):

    string_pattern = r"(?=\[\w{3} \w{3} \d{2} \d{2}:\d{2}\.\d+ \d{4}\])"

    log_entries = re.split(string_pattern, log)

    log_entries_formated = []
    for log_entry in log_entries:
        log_entry = log_entry.strip()
        if log_entry:
            log_entries_formated.append("[" + log_entry)

    return "\n".join(log_entries_formated)