from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IPC_DATA_PATH = "../dataset/crime_2001_2013.csv"
CYBER_DATA_PATH = "../dataset/cyber_attacks.csv"

ipc_df = None
cyber_df = None


def load_datasets():
    global ipc_df, cyber_df

    try:
        ipc_df = pd.read_csv(IPC_DATA_PATH)
        cyber_df = pd.read_csv(CYBER_DATA_PATH)

        print("Datasets loaded successfully.")
    except Exception as e:
        print("Error loading datasets:", e)

load_datasets()

def to_json(df):
    return df.to_dict(orient="records")


@app.get("/")
def home():
    return {"message": "CrimeSight API is live"}


@app.get("/ipc/states")
def get_states():
    try:
        raw_states = ipc_df["STATE/UT"].astype(str).unique()
        cleaned_states = []

        for s in raw_states:
            x = s.strip().lower()
            x = x.replace("&", " & ")
            x = " ".join(x.split())
            x = x.title()
            cleaned_states.append(x)

        final_states = sorted(set(cleaned_states))
        return {"states": final_states}

    except Exception as e:
        return {"error": str(e)}


@app.get("/ipc/years")
def get_years():
    try:
        years = sorted(ipc_df["YEAR"].astype(int).unique().tolist())
        return {"years": [int(y) for y in years]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ipc/state-summary")
def state_summary(state: str, year: int):
    try:
        df = ipc_df.copy()

        df["STATE/UT_CLEAN"] = (
            df["STATE/UT"]
            .astype(str)
            .str.lower()
            .str.replace("&", " & ")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        state_clean = (
            state
            .lower()
            .replace("&", " & ")
            .strip()
        )
        state_clean = " ".join(state_clean.split())

        filtered = df[
            (df["STATE/UT_CLEAN"] == state_clean) &
            (df["YEAR"].astype(int) == year)
        ]

        if filtered.empty:
            return {"error": "No data found for this state and year"}

        filtered = filtered.drop(columns=["STATE/UT_CLEAN"])

        rows = []
        for _, row in filtered.iterrows():
            row_dict = row.to_dict()
            cleaned_row = {k: v for k, v in row_dict.items()
                           if k in ["STATE/UT", "DISTRICT", "YEAR"] or v != 0}
            rows.append(cleaned_row)

        return {"year" : year ,"data": rows}
    except Exception as e:
        return {"error": str(e)}


@app.get("/ipc/districts")
def get_districts(state: str):
    try:
        df = ipc_df.copy()

        df["STATE/UT_CLEAN"] = (
            df["STATE/UT"]
            .astype(str)
            .str.lower()
            .str.replace("&", " & ")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        state_clean = (
            state
            .lower()
            .replace("&", " & ")
            .strip()
        )
        state_clean = " ".join(state_clean.split())

        filtered = df[df["STATE/UT_CLEAN"] == state_clean]
        if filtered.empty:
            return {"error": "No districts found for this state"}

        districts = sorted(filtered["DISTRICT"].astype(str).unique())

        return {"districts": districts}
    except Exception as e:
        return {"error": str(e)}
        

@app.get("/ipc/crimes")
def get_crimes():
    try:
        df = ipc_df.copy()
        cols = df.columns.tolist()

        ignore_cols = ["STATE/UT", "DISTRICT", "YEAR"]

        crime_cols = [c for c in cols if c not in ignore_cols]

        crime_list = sorted([c.title() for c in crime_cols])

        return {"crimes": crime_list}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ipc/crime-trend")
def state_trend(state: str, crime: str, district: str = None):
    try:
        df = ipc_df.copy()

        df["STATE_CLEAN"] = (
            df["STATE/UT"]
            .astype(str).str.lower()
            .str.replace("&", " & ")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        state_clean = (
            state.lower()
            .replace("&", " & ")
            .strip()
        )
        state_clean = " ".join(state_clean.split())

        crime_col = crime.upper()
        if crime_col not in df.columns:
            return {"error": "Invalid crime name"}

        state_df = df[df["STATE_CLEAN"] == state_clean]
        if state_df.empty:
            return {"error": "State not found"}

        if district:
            district_clean = district.lower().strip()
            state_df["DISTRICT_CLEAN"] = (
                state_df["DISTRICT"].astype(str).str.lower().str.strip()
            )

            dist_df = state_df[state_df["DISTRICT_CLEAN"] == district_clean]

            if dist_df.empty:
                return {"error": "District not found in this state"}

            dist_df = dist_df[["YEAR", crime_col]]
            dist_df["YEAR"] = dist_df["YEAR"].astype(int)
            dist_df = dist_df.sort_values(by="YEAR")

            trend = [
                {"year": int(r["YEAR"]), "value": int(r[crime_col])}
                for _, r in dist_df.iterrows()
                if r[crime_col] != 0
            ]

            return {
                "state": state.title(),
                "district": district.title(),
                "crime": crime.title(),
                "trend": trend
            }

        state_df = state_df.groupby("YEAR")[crime_col].sum().reset_index()
        state_df["YEAR"] = state_df["YEAR"].astype(int)
        state_df = state_df.sort_values(by="YEAR")

        trend = [
            {"year": int(r["YEAR"]), "value": int(r[crime_col])}
            for _, r in state_df.iterrows()
            if r[crime_col] != 0
        ]

        return {
            "state": state.title(),
            "crime": crime.title(),
            "trend": trend
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/ipc/top-states")
def top_states(crime: str, year: int, n: int = 10):
    try:
        df = ipc_df.copy()

        crime_col = crime.upper()
        if crime_col not in df.columns:
            return {"error": "Invalid crime name"}

        df = df[df["YEAR"].astype(int) == year]
        if df.empty:
            return {"error": "No data found for this year"}

        grouped = (
            df.groupby("STATE/UT")[crime_col]
            .sum()
            .reset_index()
        )

        grouped = grouped[grouped[crime_col] != 0]
        grouped = grouped.sort_values(by=crime_col, ascending=False)
        grouped = grouped.head(n)

        result = [
            {
                "state": row["STATE/UT"].title(),
                "value": int(row[crime_col])
            }
            for _, row in grouped.iterrows()
        ]

        return {
            "crime": crime.title(),
            "year": year,
            "top_states": result
        }

    except Exception as e:
        return {"error": str(e)}
    

@app.get("/ipc/district-ranking")
def district_ranking(state: str, crime: str, year: int):
    try:
        df = ipc_df.copy()

        df["STATE_CLEAN"] = (
            df["STATE/UT"]
            .astype(str).str.lower()
            .str.replace("&", " & ")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        state_clean = (
            state.lower()
            .replace("&", " & ")
            .strip()
        )
        state_clean = " ".join(state_clean.split())

        crime_col = crime.upper()
        if crime_col not in df.columns:
            return {"error": "Invalid crime name"}

        df = df[
            (df["STATE_CLEAN"] == state_clean) &
            (df["YEAR"].astype(int) == year)
        ]

        if df.empty:
            return {"error": "No data found"}

        df = df[df["DISTRICT"].str.upper() != "TOTAL"]

        grouped = (
            df.groupby("DISTRICT")[crime_col]
            .sum()
            .reset_index()
        )

        grouped = grouped[grouped[crime_col] != 0]
        grouped = grouped.sort_values(by=crime_col, ascending=False)

        result = [
            {
                "district": row["DISTRICT"].title(),
                "value": int(row[crime_col])
            }
            for _, row in grouped.iterrows()
        ]

        return {
            "state": state.title(),
            "crime": crime.title(),
            "year": year,
            "districts": result
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/ipc/state-map")
def state_map(year: int):
    try:
        df = ipc_df.copy()

        df = df[df["YEAR"].astype(int) == year]
        if df.empty:
            return {"error": "No data found for this year"}

        grouped = (
            df.groupby("STATE/UT")["TOTAL IPC CRIMES"]
            .sum()
            .reset_index()
        )

        grouped = grouped[grouped["TOTAL IPC CRIMES"] != 0]

        result = [
            {
                "state": row["STATE/UT"].title(),
                "value": int(row["TOTAL IPC CRIMES"])
            }
            for _, row in grouped.iterrows()
        ]

        return {
            "year": year,
            "states": result
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/cyber/attack-types")
def attack_types():
    try:
        df = cyber_df.copy()

        attack_types = (
            df["attack_type"]
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )
        
        attack_types = sorted(attack_types)
        
        return {"attack_types": attack_types}

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/industries")
def get_industries():
    try:
        df = cyber_df.copy()

        industries = (
            df["industry"]
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )
        
        industries = sorted(industries)
        
        return {"industries": industries}

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/cyber/locations")
def get_locations():
    try:
        df = cyber_df.copy()

        locations = (
            df["location"]
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        locations = sorted(locations)

        return {"locations": locations}

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/years")
def get_cyber_years():
    try:
        df = cyber_df.copy()

        df["year"] = pd.to_datetime(df["timestamp"], errors="coerce").dt.year

        years = (
            df["year"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

        years = sorted(years)

        return {"years": years}

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/hours")
def get_attack_hours():
    try:
        df = cyber_df.copy()

        df["hour"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        ).dt.hour

        hours = (
            df["hour"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

        hours = sorted(hours)

        return {"hours": hours}

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/targets")
def target_systems(attack: str, hour: int):
    try:
        df = cyber_df.copy()

        df["hour"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        ).dt.hour

        df["attack_type_clean"] = df["attack_type"].astype(str).str.lower().str.strip()
        attack_clean = attack.lower().strip()

        filtered = df[
            (df["attack_type_clean"] == attack_clean) &
            (df["hour"] == hour)
        ]

        if filtered.empty:
            return {"error": "No data found"}

        grouped = (
            filtered.groupby("target_system")
            .size()
            .reset_index(name="count")
            .sort_values(by="count", ascending=False)
        )

        result = [
            {
                "target system": row["target_system"],
                "count": int(row["count"])
            }
            for _, row in grouped.iterrows()
        ]

        return {
            "attack_type": attack,
            "hour": hour,
            "targets": result
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/outcome")
def outcome_rate(attack: str, year: int):
    try:
        df = cyber_df.copy()

        df["year"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        ).dt.year

        df["attack_type_clean"] = df["attack_type"].astype(str).str.lower().str.strip()
        attack_clean = attack.lower().strip()

        filtered = df[
            (df["attack_type_clean"] == attack_clean) &
            (df["year"] == year)
        ]

        if filtered.empty:
            return {"error": "No data found"}

        total = len(filtered)

        outcome_counts = (
            filtered["outcome"]
            .astype(str)
            .str.lower()
            .value_counts()
        )

        success = int(outcome_counts.get("success", 0))
        failure = int(outcome_counts.get("failure", 0))

        return {
            "attack_type": attack,
            "year": year,
            "success_percent": round((success / total) * 100, 2),
            "failure_percent": round((failure / total) * 100, 2)
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/cyber/attack-trend")
def attack_trend(attack: str = None):
    try:
        df = cyber_df.copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["year"] = df["timestamp"].dt.year

        if attack:
            df["attack_type_clean"] = (
                df["attack_type"]
                .astype(str)
                .str.lower()
                .str.strip()
            )
            attack_clean = attack.lower().strip()
            df = df[df["attack_type_clean"] == attack_clean]

        if df.empty:
            return {"error": "No data found"}

        trend = (
            df.groupby("year")
            .size()
            .reset_index(name="count")
            .sort_values("year")
        )

        result = [
            {
                "year": int(row["year"]),
                "count": int(row["count"])
            }
            for _, row in trend.iterrows()
        ]

        if attack:
            response = {
                "attack_type": attack,
                "trend": result
            }
        else:
            response = {
                "trend": result
            }

        return response

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/industry-impact")
def industry_impact(year: int, attack: str = None):
    try:
        df = cyber_df.copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["year"] = df["timestamp"].dt.year

        df = df[df["year"] == year]

        if attack:
            df["attack_type_clean"] = (
                df["attack_type"]
                .astype(str)
                .str.lower()
                .str.strip()
            )
            attack_clean = attack.lower().strip()
            df = df[df["attack_type_clean"] == attack_clean]

        if df.empty:
            return {"error": "No data found"}

        grouped = (
            df.groupby("industry")
            .size()
            .reset_index(name="count")
            .sort_values(by="count", ascending=False)
        )

        result = [
            {
                "industry": row["industry"],
                "count": int(row["count"])
            }
            for _, row in grouped.iterrows()
        ]

        if attack:
            response = {
                "attack_type" : attack,
                "year": year ,
                "industries" : result
                }

        else: 
            response = {
                "year": year, 
                "industries" : result
                }

        return response

    except Exception as e:
        return {"error": str(e)}


@app.get("/cyber/data-loss")
def data_loss_trend( industry: str = None):
    try:
        df = cyber_df.copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["year"] = df["timestamp"].dt.year
       
        if industry:
            df["industry_clean"] = (
                df["industry"]
                .astype(str)
                .str.lower()
                .str.strip()
            )
            industry_clean = industry.lower().strip()
            df = df[df["industry_clean"] == industry_clean]

        if df.empty:
            return {"error": "No data found"}

        grouped = (
            df.groupby("year")["data_compromised_GB"]
            .sum()
            .reset_index()
            .sort_values("year")
        )

        result = [
            {
                "year": int(row["year"]),
                "data_loss_gb": round(float(row["data_compromised_GB"]), 2)
            }
            for _, row in grouped.iterrows()
        ]

        if industry:
            response = {
                "industry" : industry ,
                "trend": result
            }
        
        else: 
            response = {
                "trend" : result
            }
        
        return response

    except Exception as e:
        return {"error": str(e)}


@app.get("/cyber/severity-summary")
def severity_summary(year: int , attack: str= None):
    try:
        df = cyber_df.copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["year"] = df["timestamp"].dt.year
        df = df[df["year"] == year]

        if attack:
            df["attack_type_clean"] = (
                df["attack_type"]
                .astype(str)
                .str.lower()
                .str.strip()
            )
            attack_clean = attack.lower().strip()
            df = df[df["attack_type_clean"] == attack_clean]

        if df.empty:
            return {"error": "No data found"}

        def map_severity(val):
            if val <= 3:
                return "Low"
            elif val <= 6:
                return "Medium"
            else:
                return "High"

        df["severity_level"] = df["attack_severity"].apply(map_severity)

        grouped = (
            df.groupby("severity_level")
            .size()
            .reset_index(name="count")
        )

        result = [
            {
                "severity": row["severity_level"],
                "count": int(row["count"])
            }
            for _, row in grouped.iterrows()
        ]

        if attack:
             response = {
                "attack_type" : attack ,
                "year" : year ,
                "severity_distribution": result
            }
        else: 
            response = {
                "year" : year ,
                "severity_distribution": result
            }
        return response

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/mitigation")
def mitigation_effectiveness(year: int, attack: str):
    try:
        df = cyber_df.copy()

        df["year"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        ).dt.year

        df["attack_type_clean"] = (
            df["attack_type"]
            .astype(str)
            .str.lower()
            .str.strip()
        )
        attack_clean = attack.lower().strip()

        df = df[
            (df["year"] == year) &
            (df["attack_type_clean"] == attack_clean)
        ]

        if df.empty:
            return {"error": "No data found"}

        grouped = (
            df.groupby("mitigation_method")
            .size()
            .reset_index(name="count")
            .sort_values(by="count", ascending=False)
        )

        result = [
            {
                "mitigation_method": row["mitigation_method"],
                "count": int(row["count"])
            }
            for _, row in grouped.iterrows()
        ]

        return {
            "year": year,
            "attack_type": attack,
            "mitigations": result
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/cyber/duration-vs-severity")
def attack_duration_vs_severity(year: int, attack: str = None):
    try:
        df = cyber_df.copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["year"] = df["timestamp"].dt.year
        df = df[df["year"] == year]

        if attack:
            df["attack_type_clean"] = (
                df["attack_type"]
                .astype(str)
                .str.lower()
                .str.strip()
            )
            attack_clean = attack.lower().strip()
            df = df[df["attack_type_clean"] == attack_clean]

        if df.empty:
            return {"error": "No data found"}

        def map_severity(val):
            if val <= 3:
                return "Low"
            elif val <= 6:
                return "Medium"
            else:
                return "High"

        df["severity_level"] = df["attack_severity"].apply(map_severity)

        grouped = (
            df.groupby("severity_level")["attack_duration_min"]
            .mean()
            .reset_index()
        )

        result = [
            {
                "severity": row["severity_level"],
                "avg_duration_min": round(float(row["attack_duration_min"]), 2)
            }
            for _, row in grouped.iterrows()
        ]

        if attack:
            response = {
                "attack_type": attack,
                "year": year,
                "severity_duration": result
            }
        else:
            response = {
                "year": year,
                "severity_duration": result
            }

        return response

    except Exception as e:
        return {"error": str(e)}
