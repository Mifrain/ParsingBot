from aiogram.fsm.state import StatesGroup, State

class UploadFileState(StatesGroup):
    get_file = State()
