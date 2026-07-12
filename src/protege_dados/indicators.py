from __future__ import annotations
import pandas as pd
import numpy as np

def minmax(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    lo, hi = x.min(), x.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        return pd.Series(np.zeros(len(x)), index=x.index, dtype=float)
    return 100 * (x - lo) / (hi - lo)

def build_uf_indicators(ibge, inep, anatel, ondh, weights: dict) -> pd.DataFrame:
    pop = ibge.groupby("uf", as_index=False)["population"].sum()

    sch = inep.groupby("uf").agg(
        schools=("internet", "size"),
        schools_internet=("internet", "sum"),
        schools_broadband=("broadband", "sum")
    ).reset_index()
    sch["school_no_internet"] = 100 * (1 - sch["schools_internet"] / sch["schools"])
    sch["school_no_broadband"] = 100 * (1 - sch["schools_broadband"] / sch["schools"])

    tel = anatel.groupby("uf", as_index=False)["accesses"].sum()
    tel = tel.merge(pop, on="uf", how="left")
    tel["blf_density"] = 100 * tel["accesses"] / tel["population"]
    tel["low_blf_density"] = 100 - minmax(tel["blf_density"])

    vio = ondh.groupby("uf", as_index=False)["violations"].sum()
    vio = vio.merge(pop, on="uf", how="left")
    vio["violation_rate"] = 100000 * vio["violations"] / vio["population"]

    out = pop.merge(sch, on="uf", how="left").merge(
        tel[["uf","accesses","blf_density","low_blf_density"]], on="uf", how="left"
    ).merge(
        vio[["uf","violations","violation_rate"]], on="uf", how="left"
    )

    out["n_violation_rate"] = minmax(out["violation_rate"])
    out["n_school_no_internet"] = minmax(out["school_no_internet"])
    out["n_school_no_broadband"] = minmax(out["school_no_broadband"])
    out["n_low_blf_density"] = minmax(out["low_blf_density"])

    out["vulnerability_axis"] = (
        weights["violation_rate"] * out["n_violation_rate"] +
        weights["school_no_internet"] * out["n_school_no_internet"] +
        weights["school_no_broadband"] * out["n_school_no_broadband"] +
        weights["low_blf_density"] * out["n_low_blf_density"]
    )

    out["protection_axis"] = pd.NA
    out["status_protection_axis"] = "Em desenvolvimento: sem variável pública comparável validada."
    return out.sort_values("uf")
