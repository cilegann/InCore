from params import params
from service.dataService.utils import getFileInfo,getDf,getColType
from utils import sql
import logging
import json
import numpy as np
import pandas as import pd

class preprocess():
    def __init__(self,fid):
        self.params=params
        self.fid=fid