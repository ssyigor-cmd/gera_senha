import pyttsx3
import threading
import time
import logging

logger = logging.getLogger(__name__)

def falar(texto):
    """Fala o texto usando pyttsx3, recriando a engine a cada chamada."""
    def _falar():
        engine = None
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            try:
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'brazil' in voice.name.lower() or 'portuguese' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        logger.info(f"Voz selecionada: {voice.name}")
                        break
            except Exception as e:
                logger.warning(f"Não foi possível configurar voz em português: {e}")
            
            engine.say(texto)
            engine.runAndWait()
            time.sleep(0.1)
            logger.info(f"TTS executado com sucesso: '{texto}'")
            
        except Exception as e:

            logger.exception(f"Falha ao reproduzir TTS para o texto: '{texto}'. Erro: {e}")
        finally:
            if engine:
                try:
                    engine.stop()
                except Exception as e:
                    logger.warning(f"Erro ao parar engine de TTS: {e}")
    
    thread = threading.Thread(target=_falar)
    thread.daemon = True
    thread.start()