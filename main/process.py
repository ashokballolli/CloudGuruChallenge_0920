
import classes
import extract
import load
import transform

if __name__ == "__main__":

    # -----------------------------------------------------
    # EXTRACT

    # define ny_dataset
    ny_dataset = classes.Dataset("ny_dataset")
    ny_dataset.headers_all = ["date", "cases", "deaths"]
    ny_dataset.headers_key = ny_dataset.headers_all
    ny_dataset.match_field = "date"
    ny_dataset.source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"

    # extract and print ny_dataset
    ny_dataset.df = extract.extract(ny_dataset.source_url)
    print(f"'ny_dataset.df':\n{ny_dataset.df}")

    # define jh_dataset
    jh_dataset = classes.Dataset("jh_dataset")
    jh_dataset.headers_all = [
        "Date", "Country/Region", "Province/State", "Lat", "Long", "Confirmed", "Recovered", "Deaths"
    ]
    jh_dataset.headers_key = ["Date", "Country/Region", "Recovered"]
    jh_dataset.match_field = "Date"
    jh_dataset.source_url = \
        "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

    # extract and print jh_dataset
    jh_dataset.df = extract.extract(jh_dataset.source_url, jh_dataset.headers_key, "Country/Region", "US")
    print(f"'jh_dataset.df':\n{jh_dataset.df}")

    # -----------------------------------------------------
    # TRANSFORM

    # transform the datasets into CovidStat Instances
    covid_stats = transform.transform(ny_dataset, jh_dataset)

    # print CovidStats
    for stat in covid_stats:
        print(stat.to_string())

    # -----------------------------------------------------
    # LOAD

    # load CovidStat instances into the CovidStats DynamoDB table
    load.load_all("CovidStats", covid_stats, classes.CovidStat)
