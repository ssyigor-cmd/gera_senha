import pyttsx3
import threading
import time

def falar(texto):
    """Fala o texto usando pyttsx3, garantindo que funcione várias vezes."""
    def _falar():
        try:
            # Cria uma engine NOVA a cada chamada
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            # Configura voz em português (se disponível)
            try:
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'brazil' in voice.name.lower() or 'portuguese' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            except:
                pass  # Se falhar, usa a voz padrão
            
            # Fala e espera terminar
            engine.say(texto)
            engine.runAndWait()
            
            # Pequena pausa para garantir que a engine finalizou
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Erro no TTS: {e}")
    
    # Roda em uma thread separada para não travar a interface
    thread = threading.Thread(target=_falar)
    thread.daemon = True
    thread.start()