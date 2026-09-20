
def format_message(*dicts):
    msg = ""
    for d in dicts:
        for k, v in d.items():
            msg += f"{k}: {v} \n"
    return msg

def bytes_to_mib(*args, decimal_places=2):
    return round(sum(args) / 1024 / 1024, decimal_places)
