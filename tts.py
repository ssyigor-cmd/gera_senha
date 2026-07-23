# tts.py
import pyttsx3
import threading
import logging

logger = logging.getLogger(__name__)

# Cache da voz (busca apenas uma vez)
_voice_id = None
_rate = 150
_volume = 0.9

def _get_voice_id():
    """Retorna o ID da voz em português (cache)."""
    global _voice_id
    if _voice_id is None:
        try:
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            for voice in voices:
                if 'brazil' in voice.name.lower() or 'portuguese' in voice.name.lower():
                    _voice_id = voice.id
                    logger.info(f"Voz TTS selecionada: {voice.name}")
                    break
            temp_engine.stop()
        except Exception as e:
            logger.warning(f"Erro ao buscar vozes: {e}")
    return _voice_id

def falar(texto):
    """Fala o texto usando uma nova engine a cada chamada."""
    def _falar():
        engine = None
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', _rate)
            engine.setProperty('volume', _volume)
            
            voice_id = _get_voice_id()
            if voice_id:
                engine.setProperty('voice', voice_id)
            
            engine.say(texto)
            engine.runAndWait()
            logger.info(f"TTS executado: '{texto}'")
            
        except Exception as e:
            logger.exception(f"Erro ao reproduzir TTS: {e}")
        finally:
            if engine:
                try:
                    engine.stop()
                except:
                    pass

    thread = threading.Thread(target=_falar)
    thread.daemon = True
    thread.start()

def encerrar_tts():
    """Função vazia para compatibilidade."""
    pass