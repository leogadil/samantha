import importlib
import os

from .action import Action, ActionManager
from .intent import Recognizer, Trainer
from .smalltalk import SmallTalk
from .speechrecognition import SpeechRecognition

from .helper import import_actions

import_actions()
    