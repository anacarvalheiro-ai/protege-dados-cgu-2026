import pandas as pd
from protege_dados.indicators import build_uf_indicators

def test_build_indicators():
    ibge=pd.DataFrame({"uf":["DF","SP"],"population":[1000,2000]})
    inep=pd.DataFrame({"uf":["DF","DF","SP"],"internet":[1,0,1],"broadband":[1,0,1]})
    anatel=pd.DataFrame({"uf":["DF","SP"],"accesses":[500,1500]})
    ondh=pd.DataFrame({"uf":["DF","SP"],"violations":[10,20]})
    w={"violation_rate":.25,"school_no_internet":.25,"school_no_broadband":.20,"low_blf_density":.30}
    out=build_uf_indicators(ibge,inep,anatel,ondh,w)
    assert set(out["uf"])=={"DF","SP"}
    assert "vulnerability_axis" in out.columns
