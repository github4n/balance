import sys
import importlib

sys.path.append("/home/balance")
importlib.reload(sys)
from codegen.generator import write

write("enc", '../tokens/Token.py')