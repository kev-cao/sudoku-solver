import re

if __name__ == "__main__":
    try:
        old_results = open("old_stats.txt", "r")
        new_results = open("improved_stats.txt", "r")

        old_lines = old_results.readlines()
        new_lines = new_results.readlines()

        assert len(old_lines) == len(new_lines), "Both stat files should have same number of lines."

        name_pattern = re.compile('Test: (.+)')
        total_pattern = re.compile('Total:.+Average: (\d+\.\d+) ms')
        min_pattern = re.compile('Min:.+Average: (\d+\.\d+) ms')
        max_pattern = re.compile('Max:.+Average: (\d+\.\d+) ms')
        mean_pattern = re.compile('Mean:.+Average: (\d+\.\d+) ms')
        median_pattern = re.compile('Median:.+Average: (\d+\.\d+) ms')

        for line_num in range(len(old_lines)):
            old_current_line = old_lines[line_num]
            new_current_line = new_lines[line_num]

            if old_match := name_pattern.match(old_current_line):
                print("Comparative Results for Test '%s'" % old_match.group(1))

            elif old_match := total_pattern.match(old_current_line):
                old_total = float(old_match.group(1))
                new_total = float(total_pattern.match(new_current_line).group(1))

                print("Total: %.2f%% time taken." % (new_total / old_total))

            elif old_match := min_pattern.match(old_current_line):
                old_min = float(old_match.group(1))
                new_min = float(min_pattern.match(new_current_line).group(1))

                print("Min: %.2f%% time taken." % (new_min / old_min))

            elif old_match := max_pattern.match(old_current_line):
                old_max = float(old_match.group(1))
                new_max = float(max_pattern.match(new_current_line).group(1))

                print("Max: %.2f%% time taken." % (new_max / old_max))

            elif old_match := mean_pattern.match(old_current_line):
                old_mean = float(old_match.group(1))
                new_mean = float(mean_pattern.match(new_current_line).group(1))

                print("Mean: %.2f%% time taken." % (new_mean / old_mean))

            elif old_match := median_pattern.match(old_current_line):
                old_median = float(old_match.group(1))
                new_median = float(median_pattern.match(new_current_line).group(1))

                print("Median: %.2f%% time taken.\n\n" % (new_median / old_median))

    except IOError:
        print("Did not have both improved_stats.txt and old_stats.txt")
