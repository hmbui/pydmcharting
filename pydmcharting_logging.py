import logging

logging.basicConfig(level=logging.INFO, filename="logs/pydmcharting.log",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Override the basic configs for cleaner console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(message)s"))
logger = logging.getLogger('').addHandler(console_handler)
