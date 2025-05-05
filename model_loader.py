import os
from sentence_transformers import SentenceTransformer
import torch
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    _model = None
    _lock = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_model(cls, model_name=None):
        if cls._model is None and not cls._lock:
            try:
                cls._lock = True
                start_time = time.time()
                
                model_name = model_name or os.getenv('MODEL_NAME', 'sentence-transformers/all-MiniLM-L6-v2')
                cache_dir = os.getenv('MODEL_CACHE_DIR', 'model_cache')
                
                logger.info(f"Starting model load: {model_name}")
                logger.info(f"Cache directory: {os.path.abspath(cache_dir)}")
                
                # Ensure cache directory exists
                os.makedirs(cache_dir, exist_ok=True)
                
                # Check if model is already cached
                model_path = os.path.join(cache_dir, model_name.replace('/', '_'))
                if os.path.exists(model_path):
                    logger.info("Using cached model")
                    cls._model = SentenceTransformer(
                        model_path,
                        cache_folder=cache_dir,
                        device='cuda' if torch.cuda.is_available() else 'cpu'
                    )
                else:
                    logger.info("Downloading and caching model")
                    cls._model = SentenceTransformer(
                        model_name,
                        cache_folder=cache_dir,
                        device='cuda' if torch.cuda.is_available() else 'cpu'
                    )
                
                load_time = time.time() - start_time
                logger.info(f"Model loaded successfully in {load_time:.2f} seconds")
                logger.info(f"Device: {cls._model.device}")
                
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise
            finally:
                cls._lock = False
        
        return cls._model

# Pre-load the model when the module is imported
try:
    model = ModelLoader.get_model()
except Exception as e:
    logger.error(f"Failed to pre-load model: {e}")
    model = None 