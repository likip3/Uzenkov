import pandas

# vacancies_by_year.csv

filename = input('Введите название файла: ')
rC = pandas.read_csv(filename)
rC["year"] = rC["published_at"].apply(lambda x: x[:4])
rC = rC.groupby("year")

for y, info in rC:
    info[["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"]].to_csv(rf"uploadByYears\{y}.csv", index=False)