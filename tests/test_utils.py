import pandas as pd
from protege_dados.utils import normalize_ibge_code, normalize_uf

def test_normalize_ibge_code():
    s=pd.Series([1100015, "1200401", 5300108.0])
    assert normalize_ibge_code(s).tolist()==["1100015","1200401","5300108"]

def test_normalize_uf():
    s=pd.Series([" df ","sp","Ba"])
    assert normalize_uf(s).tolist()==["DF","SP","BA"]
