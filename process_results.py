from sys import stdin
import sys
import re

class Test_Result:
    def __init__(self, name):
        self.name = name
        self.total_times = []
        self.min_times = []
        self.max_times = []
        self.mean_times = []
        self.median_times = []

    def add_total(self, total_time):
        self.total_times.append(total_time)

    def add_min(self, min_time):
        self.min_times.append(min_time)

    def add_max(self, max_time):
        self.max_times.append(max_time)

    def add_mean(self, mean_time):
        self.mean_times.append(mean_time)

    def add_median(self, median_time):
        self.median_times.append(median_time)

    def average_total(self):
        return sum(self.total_times) / len(self.total_times)

    def average_min(self):
        return sum(self.min_times) / len(self.min_times)

    def average_max(self):
        return sum(self.max_times) / len(self.max_times)

    def average_mean(self):
        return sum(self.mean_times) / len(self.mean_times)

    def average_median(self):
        return sum(self.median_times) / len(self.median_times)

    def __str__(self):
        ret = "Test: %s\nTotal:" % self.name

        for time in self.total_times:
            ret += " %d" % time

        ret += " | Average: %.2f ms\nMin:" % self.average_total()

        for time in self.min_times:
            ret += " %d" % time

        ret += " | Average: %.2f ms\nMax:" % self.average_min()

        for time in self.max_times:
            ret += " %d" % time

        ret += " | Average: %.2f ms\nMean:" % self.average_max()

        for time in self.mean_times:
            ret += " %d" % time

        ret += " | Average: %.2f ms\nMedian:" % self.average_mean()

        for time in self.median_times:
            ret += " %d" % time

        ret += " | Average: %.2f ms\n\n" % self.average_median()

        return ret

if __name__ == "__main__":
    test_results_map = {}

    if len(sys.argv) != 2:
        raise Exception("Provide the file name to read/write to as an argument.")

    filename = sys.argv[1]

    try:
        save_file = open("filename", "r")

        lines = save_file.readlines()

        test_result = None

        name_pattern = re.compile('Test: (.+)')
        total_pattern = re.compile('Total: ([\d ]+) |')
        min_pattern = re.compile('Min: ([\d ]+) |')
        max_pattern = re.compile('Max: ([\d ]+) |')
        mean_pattern = re.compile('Mean: ([\d ]+) |')
        median_pattern = re.compile('Median: ([\d ]+) |')

        for line in lines:
            if match := name_pattern.match(line):
                if test_result is not None:
                    test_results_map[test_result.name] = test_result

                test_result = Test_Result(match.group(1))

            elif match := total_pattern.match(line):
                total_times = [int(d) for d in match.group(1).split(' ')]
                test_result.total_times = total_times

            elif match := min_pattern.match(line):
                min_times = [int(d) for d in match.group(1).split(' ')]
                test_result.min_times = min_times

            elif match := max_pattern.match(line):
                max_times = [int(d) for d in match.group(1).split(' ')]
                test_result.max_times = max_times

            elif match := mean_pattern.match(line):
                mean_times = [int(d) for d in match.group(1).split(' ')]
                test_result.mean_times = mean_times

            elif match := median_pattern.match(line):
                median_times = [int(d) for d in match.group(1).split(' ')]
                test_result.median_times = median_times

        if test_result is not None:
            test_results_map[test_result.name] = test_result

        save_file.close()
    except IOError:
        print("Creating new %s." % filename)

    save_file = open("filename", "w")

    name_pattern = re.compile('.*Test: (.+)')
    total_pattern = re.compile('.*Total:[^\d]*(\d+)')
    min_pattern = re.compile('.*Min:[^\d]*(\d+)')
    max_pattern = re.compile('.*Max:[^\d]*(\d+)')
    mean_pattern = re.compile('.*Mean:[^\d]*(\d+)')
    median_pattern = re.compile('.*Median:[^\d]*(\d+)')

    current_test = None

    for line in stdin:
        if match := name_pattern.match(line):
            name = match.group(1)
            if name in test_results_map:
                current_test = test_results_map[name]
            else:
                current_test = Test_Result(name)
                test_results_map[name] = current_test

        elif match := total_pattern.match(line):
            total_time = int(match.group(1))
            current_test.add_total(total_time)

        elif match := min_pattern.match(line):
            min_time = int(match.group(1))
            current_test.add_min(min_time)

        elif match := max_pattern.match(line):
            max_time = int(match.group(1))
            current_test.add_max(max_time)

        elif match := mean_pattern.match(line):
            mean_time = int(match.group(1))
            current_test.add_mean(mean_time)

        elif match := median_pattern.match(line):
            median_time = int(match.group(1))
            current_test.add_median(median_time)

    for test_result in test_results_map.values():
        save_file.write(str(test_result))

    save_file.close()
