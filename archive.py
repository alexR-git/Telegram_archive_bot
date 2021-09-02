from telegram import Update, InputMediaDocument, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext, PrefixHandler, ConversationHandler

import Responses as Rp
import Token as btoken

token = btoken.token

print('Bot iniciado...')

# States
ONE = range(2)  # Conversación para configurar nombre e email

def documents(update: Update, context: CallbackContext):

    user_name = update.message.from_user.first_name

    # Creación de los botones
    # Formato: lista de listas. Lista interior: columnas; lista exterior: filas
    buttons = [[
        KeyboardButton('Último informe'),
        KeyboardButton('Archivo'),
    ]]

    # teclado de respuesta: ajusta el tamaño al texto, cuando el usuario pincha desaparece y solo le sale al usuario que está interactuando con el bot.
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )

    update.message.reply_text(f'Hola, {user_name}, ¿a qué quieres acceder?', reply_markup=reply_keyboard)

    return ONE


def one_callback(update: Update, context: CallbackContext):

    user_text = update.message.text
    user_text = user_text.lower()

    update.message.reply_text(f"Has elegido acceder al {user_text}")

    if user_text == 'último informe':
        update.message.reply_document(
            document=open(
                'C:\\Users\\lapap\\OneDrive\\Python\\Telegram\\moderatorBot\\files\\Overview of neural networks.pdf',
                'rb'),
            caption='Aquí lo tienes:',
            thumb=open('C:\\Users\\lapap\\OneDrive\\Python\\Telegram\\moderatorBot\\img\\thumb last publish.jpg', 'rb')
        )
    if user_text == 'archivo':

        update.message.reply_text('Aquí tienes:')

        journal_1 = InputMediaDocument(
            media=open('[ruta del primer documento]', 'rb'),
            caption='[caption del primer documento]',
            thumb=open('[ruta de la miniatura del primer documento]', 'rb')
        )

        journal_2 = InputMediaDocument(
            media=open('[ruta del segundo documento]', 'rb'),
            caption='[caption del segundo documento]',
            thumb=open('[ruta de la miniatura del segundo documento]', 'rb')
        )

        journal_3 = InputMediaDocument(
            media=open('[ruta del tercer documento]', 'rb'),
            caption='[caption del tercer documento]',
            thumb=open('[ruta de la miniatura del tercer documento]', 'rb')
        )

        journal_4 = InputMediaDocument(
            media=open('[ruta del cuarto documento]', 'rb'),
            caption='[caption del cuarto documento]',
            thumb=open('[ruta de la miniatura del cuarto documento]', 'rb')
        )

        update.message.reply_media_group(
            media=[
                journal_1,
                journal_2,
                journal_3,
                journal_4
            ]
        )

        return ConversationHandler.END    # finaliza la conversación


def fallback_callback(update: Update, context: CallbackContext):

    update.message.reply_text("Disculpa, no te entiendo. Responde correctamente, por favor.")


def error(update: Update, context: CallbackContext) -> None:    #devuelve None

    """ Método de error """

    print(f'Update {update} caused error {context.error}')


def main():

    updater = Updater(token)                        # objeto Updater: interfaz con el bot: nos permite interactuar con él
    print('updater creado')
    #updater = Updater(token, use_context=True)
    dp = updater.dispatcher                         # objeto dispatcher: hacia donde se va a despachar todas las actualizaciones de mensajes que haga un usuario hacia nosotros
    print('dispatcher creado')

    # CONVERSATIONHANDLER

    entry_point = [CommandHandler("documents", documents)]  # comando + función de callback

    states = {
        ONE: [MessageHandler(filters=Filters.text, callback=one_callback)]
    }  # regex típico de un email. ^ = inicio; $ = fin.

    fallbacks = [MessageHandler(filters=Filters.all, callback=fallback_callback)]

    # entry points: comandos de entrada; states: estados de la conversación; fallbacks: callbacks de error;
    # allow_reentry: permitir o no recomienzo de la conversación (en cualquier momento de esta) al volver a enviar el comando de inicio.
    dp.add_handler(ConversationHandler(
        entry_points=entry_point,
        states=states,
        fallbacks=fallbacks,
        allow_reentry=True
    ))


    # Añadimos un handler de tipo error_handler: será llamado cuando ocurra un error
    dp.add_error_handler(error)  # le especificamos que invoque el método error



    updater.start_polling(5)  # que el bot esté listo para escuchar de nuevo cada 5 segundos
    updater.idle()  # método para que el bot se quede escuchando


main()