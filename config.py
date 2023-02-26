from environs import Env

env = Env()
env.read_env()

TESSDATA_DIR = env.str("TESSDATA_DIR", "./tessdata")