from aiogram import Router, types


echo_router = Router()

@echo_router.message()
async def echo(message: types.Message):
    kb = types.ReplyKeyboardRemove()
    # logging.info(message)
    mes = message.text
    mes_list = mes.split()
    mes_list.reverse()
    prob = ' '
    mes3 = prob.join(mes_list)
    await message.answer(mes3, reply_markup=kb)