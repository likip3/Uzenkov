import multiprocessing
import cProfile
import os
import pandas
import concurrent.futures as con_fut

headersRU = ['Динамика уровня зарплат по годам: ', 'Динамика количества вакансий по годам: ',
             'Динамика уровня зарплат по годам для выбранной профессии: ',
             'Динамика количества вакансий по годам для выбранной профессии: ',
             'Уровень зарплат по городам (в порядке убывания): ', 'Доля вакансий по городам (в порядке убывания): ']


class Solution:
    def __init__(self, path, vacancyName):
        self.path = path
        self.vacancyName = vacancyName
        self.salByYear = {}
        self.vacByYear = {}
        self.salByYearForVac = {}
        self.vacByYearForVac = {}
        self.salByCity = {}
        self.vacRateByCity = {}

    def split_by_year(self):
        df = pandas.read_csv(self.path)
        df["year"] = df["published_at"].apply(lambda x: x[:4])
        df = df.groupby("year")
        for y, info in df:
            info[["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"]]. \
                to_csv(rf"uploadByYears\{y}.csv", index=False)

    def get_stats(self):
        self.get_stats_by_year_with_multiprocessing()
        self.get_stats_by_city()

    def get_statistic_by_year(self, file_csv):
        df = pandas.read_csv(file_csv)
        df["salary"] = df[["salary_from", "salary_to"]].mean(axis=1)
        df["published_at"] = df["published_at"].apply(lambda s: int(s[:4]))
        info_of_file_vacancy = df[df["name"].str.contains(self.vacancyName)]
        return df["published_at"].values[0], [int(df["salary"].mean()), len(df),
                                              int(info_of_file_vacancy["salary"].mean() if len(
                                                  info_of_file_vacancy) != 0 else 0), len(info_of_file_vacancy)]

    def add_elements_to_stats(self, result):
        for y, data_stats in result:
            self.salByYear[y] = data_stats[0]
            self.vacByYear[y] = data_stats[1]
            self.salByYearForVac[y] = data_stats[2]
            self.vacByYearForVac[y] = data_stats[3]

    def get_stats_by_year_not_with_multiprocessing(self):
        result = []
        for filename in os.listdir("uploadByYears"):
            with open(os.path.join("uploadByYears", filename), "r") as file_csv:
                result.append(self.get_statistic_by_year(file_csv.name))
        self.add_elements_to_stats(result)

    def get_stats_by_year_with_multiprocessing(self):
        files = [rf"uploadByYears\{file_name}" for file_name in os.listdir(rf"uploadByYears")]
        pool = multiprocessing.Pool(4)
        result = pool.starmap(self.get_statistic_by_year, [(file,) for file in files])
        pool.close()
        self.add_elements_to_stats(result)

    def get_stats_by_city(self):
        df = pandas.read_csv(self.path)
        total = len(df)
        df["salary"] = df[["salary_from", "salary_to"]].mean(axis=1)
        df["count"] = df.groupby("area_name")["area_name"].transform("count")
        df = df[df["count"] > total * 0.01]
        df = df.groupby("area_name", as_index=False)
        df = df[["salary", "count"]].mean().sort_values("salary", ascending=False)
        df["salary"] = df["salary"].apply(lambda s: int(s))
        self.salByCity = dict(zip(df.head(10)["area_name"], df.head(10)["salary"]))
        df = df.sort_values("count", ascending=False)
        df["count"] = round(df["count"] / total, 4)
        self.vacRateByCity = dict(zip(df.head(10)["area_name"], df.head(10)["count"]))

    def print_statistic(self):
        list_print2 = [self.salByYear, self.vacByYear, self.salByYearForVac, self.vacByYearForVac, self.salByCity,
                       self.vacRateByCity]
        for i in range(len(headersRU)):
            print(headersRU[i] + '{0}'.format(list_print2[i]))

    def get_stats_by_year_with_concurrent_futures(self):
        files = [rf"uploadByYears\{file_name}" for file_name in os.listdir("uploadByYears")]
        with con_fut.ProcessPoolExecutor(max_workers=4) as exec:
            res = exec.map(self.get_statistic_by_year, files)
        result = list(res)
        self.add_elements_to_stats(result)


if __name__ == '__main__':
    # solve = Solution(input("Введите название файла: "), input("Введите название профессии: "))
    solve = Solution("vacancies_by_year.csv", "Аналитик")
    solve.split_by_year()
    solve.get_stats()
    solve.print_statistic()

    # cProfile.run("solve.get_stats_by_year_not_with_multiprocessing()", sort="cumtime")
    # cProfile.run("solve.get_stats_by_year_with_multiprocessing()", sort="cumtime")
    cProfile.run("solve.get_stats_by_year_with_concurrent_futures()", sort="cumtime")
