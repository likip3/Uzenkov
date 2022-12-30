import multiprocessing
import cProfile
import os
import pandas

headersRU = ['Динамика уровня зарплат по годам: ', 'Динамика количества вакансий по годам: ',
               'Динамика уровня зарплат по годам для выбранной профессии: ',
               'Динамика количества вакансий по годам для выбранной профессии: ',
               'Уровень зарплат по городам (в порядке убывания): ', 'Доля вакансий по городам (в порядке убывания): ']


class Multiproc:

    def __init__(self, path, vacancyName):
        self.path = path
        self.vacancyName = vacancyName
        self.salByYear = {}
        self.vacByYear = {}
        self.salByYearForVac = {}
        self.vacByYearForVac = {}
        self.salByCity = {}
        self.vacRateByCity = {}


    def get_statistic_by_year(self, file_csv):
        df = pandas.read_csv(file_csv)
        df["salary"] = df[["salary_from", "salary_to"]].mean(axis=1)
        df["published_at"] = df["published_at"].apply(lambda s: int(s[:4]))
        info_of_file_vacancy = df[df["name"].str.contains(self.vacancyName)]

        return df["published_at"].values[0], [int(df["salary"].mean()), len(df),
                                              int(info_of_file_vacancy["salary"].mean() if len(
                                                  info_of_file_vacancy) != 0 else 0), len(info_of_file_vacancy)]


    def get_stats_by_year_without_multiprocessing(self):
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


    def add_elements_to_stats(self, result):
        for y, data_stats in result:
            self.salByYear[y] = data_stats[0]
            self.vacByYear[y] = data_stats[1]
            self.salByYearForVac[y] = data_stats[2]
            self.vacByYearForVac[y] = data_stats[3]


if __name__ == '__main__':
    # solve = Solution(input("Введите название файла: "), input("Введите название профессии: "))
    solve = Multiproc("vacancies_by_year.csv", "Аналитик")

    # cProfile.run("solve.get_stats_by_year_without_multiprocessing()", sort="cumtime")
    cProfile.run("solve.get_stats_by_year_with_multiprocessing()", sort="cumtime")