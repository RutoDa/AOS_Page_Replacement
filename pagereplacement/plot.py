import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, results):
        self.results = results
        self.data = dict()

    def plot(self, title, algorithm_name, path, filenames):
        for index, result in enumerate(self.results):
            self.data[algorithm_name[index]] = dict()
            self.data[algorithm_name[index]]["frame_count"] = list(result.index)
            self.data[algorithm_name[index]]["page_faults"] = list(
                result["Page Faults"]
            )
            self.data[algorithm_name[index]]["interrupts"] = list(result["Interrupts"])
            self.data[algorithm_name[index]]["disk_writes"] = list(
                result["Disk Writes"]
            )
        # print(self.data)

        frame_count = self.data[algorithm_name[0]]["frame_count"]

        # cmap = plt.get_cmap("tab10")
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
        markers = ["o", "s", "D", "^", "v"]
        line_styles = ["-.", "--", "-"]

        plt.figure(figsize=(10, 6))
        for index, algo in enumerate(algorithm_name):
            plt.plot(
                frame_count,
                self.data[algo]["page_faults"],
                label=algo,
                color=colors[index % len(colors)],
                marker=markers[index % len(markers)],
                linestyle=line_styles[index % len(line_styles)],
                alpha=0.8,
            )
        plt.xlabel("Number of frames", fontsize=14, fontname="Times New Roman")
        plt.ylabel("Number of page faults", fontsize=14, fontname="Times New Roman")
        plt.title(title, fontsize=32, fontname="Times New Roman", weight="bold")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{path}/{filenames[0]}")

        plt.figure(figsize=(10, 6))
        for index, algo in enumerate(algorithm_name):
            plt.plot(
                frame_count,
                self.data[algo]["interrupts"],
                label=algo,
                color=colors[index % len(colors)],
                marker=markers[index % len(markers)],
                linestyle=line_styles[index % len(line_styles)],
                alpha=0.8,
            )
        plt.xlabel("Number of frames", fontsize=14, fontname="Times New Roman")
        plt.ylabel("Number of interrupts", fontsize=14, fontname="Times New Roman")
        plt.title(title, fontsize=32, fontname="Times New Roman", weight="bold")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{path}/{filenames[1]}")

        plt.figure(figsize=(10, 6))
        for index, algo in enumerate(algorithm_name):
            plt.plot(
                frame_count,
                self.data[algo]["disk_writes"],
                label=algo,
                color=colors[index % len(colors)],
                marker=markers[index % len(markers)],
                linestyle=line_styles[index % len(line_styles)],
                alpha=0.8,
            )
        plt.xlabel("Number of frames", fontsize=14, fontname="Times New Roman")
        plt.ylabel("Number of disk writes", fontsize=14, fontname="Times New Roman")
        plt.title(title, fontsize=32, fontname="Times New Roman", weight="bold")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{path}/{filenames[2]}")
